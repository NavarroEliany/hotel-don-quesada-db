-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje
-- HOTEL: Don Quesada Hotel Boutique (Ocaña, Norte de Santander)
-- ARCHIVO: 04_triggers_business_rules.sql (Lógica de Negocio en la Base de Datos)
-- =============================================================================

-- =============================================================================
-- TRIGGER 1: Evitar reservas solapadas en la misma habitación
-- Reglas de Negocio 5, 12 y 21:
-- "Una habitación no puede ser asignada a dos reservas activas para el mismo período"
-- =============================================================================

CREATE OR REPLACE FUNCTION fn_validar_disponibilidad_habitacion()
RETURNS TRIGGER AS $$
DECLARE
    v_conflicto_id INTEGER;
    v_fecha_ini DATE;
    v_fecha_fin DATE;
BEGIN
    -- Solo aplica para reservas en estado activo (Pendiente o Confirmada)
    IF NEW.status IN ('Pendiente', 'Confirmada') THEN
        SELECT b.id_booking, b.check_in_date, b.check_out_date 
        INTO v_conflicto_id, v_fecha_ini, v_fecha_fin
        FROM booking b
        WHERE b.id_room = NEW.id_room
          AND b.status IN ('Pendiente', 'Confirmada')
          -- En actualizaciones, excluir la misma reserva que se está modificando
          AND (TG_OP = 'INSERT' OR b.id_booking <> NEW.id_booking)
          -- Condición de solapamiento de rangos de fechas:
          AND NOT (NEW.check_out_date <= b.check_in_date OR NEW.check_in_date >= b.check_out_date)
        LIMIT 1;

        -- Si encontró una reserva que se cruza, cancela la operación con un error claro
        IF v_conflicto_id IS NOT NULL THEN
            RAISE EXCEPTION 'REGLA DE NEGOCIO 12/21: La habitación ID % ya está ocupada/reservada del % al % (Reserva #%).',
                NEW.id_room, v_fecha_ini, v_fecha_fin, v_conflicto_id;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_validar_disponibilidad ON booking;

CREATE TRIGGER trg_validar_disponibilidad
BEFORE INSERT OR UPDATE OF id_room, check_in_date, check_out_date, status
ON booking
FOR EACH ROW
EXECUTE FUNCTION fn_validar_disponibilidad_habitacion();


-- =============================================================================
-- TRIGGER 2: Cálculo automático del total de la reserva según la tarifa base
-- Regla de Negocio 10:
-- "El valor cobrado por una reserva debe quedar registrado según la tarifa de la habitación"
-- =============================================================================

CREATE OR REPLACE FUNCTION fn_calcular_total_reserva()
RETURNS TRIGGER AS $$
DECLARE
    v_precio_noche NUMERIC(10, 2);
    v_dias INTEGER;
BEGIN
    -- Si el total viene en 0 o no se especificó, la BD lo calcula automáticamente
    IF NEW.total_amount IS NULL OR NEW.total_amount <= 0 THEN
        -- Obtener el precio base por noche del tipo de habitación asignada
        SELECT rt.base_price 
        INTO v_precio_noche
        FROM room r
        JOIN room_type rt ON r.id_room_type = rt.id_room_type
        WHERE r.id_room = NEW.id_room;

        -- Calcular número de noches
        v_dias := (NEW.check_out_date - NEW.check_in_date);

        IF v_dias <= 0 THEN
            RAISE EXCEPTION 'La fecha de salida debe ser posterior a la fecha de entrada.';
        END IF;

        -- Asignar el total calculado
        NEW.total_amount := v_dias * v_precio_noche;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_calcular_total_reserva ON booking;

CREATE TRIGGER trg_calcular_total_reserva
BEFORE INSERT ON booking
FOR EACH ROW
EXECUTE FUNCTION fn_calcular_total_reserva();


-- =============================================================================
-- TRIGGER 3: Actualizar automáticamente el estado de la habitación
-- Reglas de Negocio 6 y 14:
-- "Cuando se confirme una reserva o finalice la estadía, la habitación actualiza su estado"
-- =============================================================================

CREATE OR REPLACE FUNCTION fn_sincronizar_estado_habitacion()
RETURNS TRIGGER AS $$
BEGIN
    -- Si la reserva se confirma
    IF NEW.status = 'Confirmada' THEN
        -- Si la fecha de ingreso es hoy o anterior, está ocupada; si es a futuro, está reservada
        IF CURRENT_DATE >= NEW.check_in_date AND CURRENT_DATE < NEW.check_out_date THEN
            UPDATE room SET status = 'Ocupada' WHERE id_room = NEW.id_room;
        ELSE
            UPDATE room SET status = 'Reservada' WHERE id_room = NEW.id_room;
        END IF;

    -- Si la reserva se finaliza o cancela, la habitación vuelve a 'Disponible'
    ELSIF NEW.status IN ('Finalizada', 'Cancelada') THEN
        -- Solo poner disponible si no tiene otra reserva activa hoy
        IF NOT EXISTS (
            SELECT 1 FROM booking 
            WHERE id_room = NEW.id_room 
              AND status = 'Confirmada'
              AND CURRENT_DATE >= check_in_date AND CURRENT_DATE < check_out_date
              AND id_booking <> NEW.id_booking
        ) THEN
            UPDATE room SET status = 'Disponible' WHERE id_room = NEW.id_room;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_sincronizar_estado_habitacion ON booking;

CREATE TRIGGER trg_sincronizar_estado_habitacion
AFTER INSERT OR UPDATE OF status, check_in_date, check_out_date
ON booking
FOR EACH ROW
EXECUTE FUNCTION fn_sincronizar_estado_habitacion();
