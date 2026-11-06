-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje
-- HOTEL: Don Quesada Hotel Boutique (Ocaña, Norte de Santander)
-- ARCHIVO: 07_stored_procedures.sql (Procedimientos Almacenados Transaccionales)
-- =============================================================================

-- =============================================================================
-- PROCEDIMIENTO 1: Registrar una Reserva Completa de Forma Segura
-- Permite al recepcionista crear una reserva con cédula del huésped y número de cuarto
-- =============================================================================
CREATE OR REPLACE PROCEDURE sp_registrar_reserva(
    p_document_number   VARCHAR(30),
    p_room_number       VARCHAR(10),
    p_check_in          DATE,
    p_check_out         DATE,
    p_number_of_guests  INTEGER,
    p_id_employee       INTEGER,
    INOUT p_id_booking  INTEGER DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_guest INTEGER;
    v_id_room  INTEGER;
    v_capacidad INTEGER;
BEGIN
    -- 1. Buscar el ID del huésped a partir de su documento
    SELECT id_guest INTO v_id_guest 
    FROM guest 
    WHERE document_number = p_document_number;

    IF v_id_guest IS NULL THEN
        RAISE EXCEPTION 'No se encontró ningún huésped registrado con el documento: %', p_document_number;
    END IF;

    -- 2. Buscar el ID de la habitación a partir de su número
    SELECT r.id_room, rt.capacity INTO v_id_room, v_capacidad
    FROM room r
    JOIN room_type rt ON r.id_room_type = rt.id_room_type
    WHERE r.room_number = p_room_number;

    IF v_id_room IS NULL THEN
        RAISE EXCEPTION 'La habitación número % no existe en el hotel.', p_room_number;
    END IF;

    -- 3. Validar capacidad de la habitación
    IF p_number_of_guests > v_capacidad THEN
        RAISE EXCEPTION 'El número de huéspedes (%) excede la capacidad máxima de la habitación (%)', 
            p_number_of_guests, v_capacidad;
    END IF;

    -- 4. Insertar la reserva (los triggers validarán solapamiento y calcularán el precio automáticamente)
    INSERT INTO booking (
        check_in_date,
        check_out_date,
        number_of_guests,
        total_amount,
        status,
        id_guest,
        id_employee,
        id_room
    ) VALUES (
        p_check_in,
        p_check_out,
        p_number_of_guests::SMALLINT,
        0, -- El trigger trg_calcular_total_reserva calculará el valor real
        'Confirmada',
        v_id_guest,
        p_id_employee,
        v_id_room
    ) RETURNING id_booking INTO p_id_booking;

    RAISE NOTICE 'Reserva #% creada con éxito para el huésped con documento %', p_id_booking, p_document_number;
END;
$$;


-- =============================================================================
-- PROCEDIMIENTO 2: Cancelar una Reserva
-- Actualiza el estado a Cancelada y libera la habitación automáticamente
-- =============================================================================
CREATE OR REPLACE PROCEDURE sp_cancelar_reserva(
    p_id_booking INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_estado_actual VARCHAR(20);
BEGIN
    SELECT status INTO v_estado_actual 
    FROM booking 
    WHERE id_booking = p_id_booking;

    IF v_estado_actual IS NULL THEN
        RAISE EXCEPTION 'La reserva con ID % no existe.', p_id_booking;
    END IF;

    IF v_estado_actual = 'Cancelada' THEN
        RAISE NOTICE 'La reserva con ID % ya se encuentra cancelada.', p_id_booking;
        RETURN;
    END IF;

    IF v_estado_actual = 'Finalizada' THEN
        RAISE EXCEPTION 'No se puede cancelar una reserva que ya fue finalizada.';
    END IF;

    -- Actualizar a cancelada (el trigger trg_sincronizar_estado_habitacion la dejará disponible)
    UPDATE booking 
    SET status = 'Cancelada' 
    WHERE id_booking = p_id_booking;

    RAISE NOTICE 'Reserva #% cancelada correctamente y habitación liberada.', p_id_booking;
END;
$$;


-- =============================================================================
-- PROCEDIMIENTO 3: Agregar Servicio Adicional a una Reserva
-- Auto-incrementa la línea de detalle para esa reserva
-- =============================================================================
CREATE OR REPLACE PROCEDURE sp_agregar_servicio_reserva(
    p_id_booking INTEGER,
    p_id_service INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_siguiente_linea INTEGER;
    v_precio_servicio NUMERIC(10, 2);
BEGIN
    -- Validar que la reserva exista y no esté cancelada
    IF NOT EXISTS (SELECT 1 FROM booking WHERE id_booking = p_id_booking AND status <> 'Cancelada') THEN
        RAISE EXCEPTION 'La reserva #% no existe o está cancelada.', p_id_booking;
    END IF;

    -- Validar que el servicio exista
    SELECT price INTO v_precio_servicio FROM service WHERE id_service = p_id_service;
    IF v_precio_servicio IS NULL THEN
        RAISE EXCEPTION 'El servicio con ID % no existe.', p_id_service;
    END IF;

    -- Calcular siguiente número de línea
    SELECT COALESCE(MAX(line_booking), 0) + 1 
    INTO v_siguiente_linea
    FROM reservation_details
    WHERE id_booking = p_id_booking;

    -- Insertar el servicio
    INSERT INTO reservation_details (id_booking, line_booking, id_service)
    VALUES (p_id_booking, v_siguiente_linea, p_id_service);

    -- Sumar el valor del servicio adicional al total de la reserva (si tiene costo)
    IF v_precio_servicio > 0 THEN
        UPDATE booking 
        SET total_amount = total_amount + v_precio_servicio 
        WHERE id_booking = p_id_booking;
    END IF;

    RAISE NOTICE 'Servicio #% agregado con éxito a la reserva #% (Línea %).', 
        p_id_service, p_id_booking, v_siguiente_linea;
END;
$$;
