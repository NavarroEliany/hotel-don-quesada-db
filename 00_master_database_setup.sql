-- =============================================================================
-- SISTEMA DE GESTIÓN DE RESERVAS Y HOSPEDAJE
-- HOTEL DON QUESADA BOUTIQUE - OCAÑA, NORTE DE SANTANDER
-- MODELO FINAL AJUSTADO SEGÚN REVISIÓN DOCENTE
-- DOCENTE: Byron Cuesta Quintero | UNIVERSIDAD FRANCISCO DE PAULA SANTANDER
-- ESTUDIANTES: Eliany Liseth Navarro Barbosa (0192234)
--              Agna Sharik Vega León (0192289)
-- MOTOR: PostgreSQL 14+
-- ARCHIVO MAESTRO DE INSTALACIÓN COMPLETA (MODELO FINAL)
-- =============================================================================

-- =============================================================================
-- 1. DDL: ELIMINACIÓN PREVIA (LIMPIEZA ORDENADA)
-- =============================================================================
DROP VIEW IF EXISTS vw_reservas_completas CASCADE;
DROP VIEW IF EXISTS vw_estado_habitaciones CASCADE;
DROP VIEW IF EXISTS vw_servicios_reserva CASCADE;
DROP VIEW IF EXISTS vw_reporte_ingresos_habitacion CASCADE;

DROP TABLE IF EXISTS booking_audit CASCADE;
DROP TABLE IF EXISTS detalle_service CASCADE;
DROP TABLE IF EXISTS detalle_room CASCADE;
DROP TABLE IF EXISTS reservation_details CASCADE; -- por compatibilidad con versión anterior
DROP TABLE IF EXISTS service CASCADE;
DROP TABLE IF EXISTS booking CASCADE;
DROP TABLE IF EXISTS room CASCADE;
DROP TABLE IF EXISTS room_type CASCADE;
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS guest CASCADE;
DROP TABLE IF EXISTS city CASCADE;
DROP TABLE IF EXISTS state CASCADE;
DROP TABLE IF EXISTS country CASCADE;

-- =============================================================================
-- 2. DDL: TABLAS Y RESTRICCIONES SEGÚN DIAGRAMA FINAL
-- =============================================================================

-- 2.1. country
CREATE TABLE country (
    id_country      SERIAL,
    name            VARCHAR(100) NOT NULL,
    CONSTRAINT pk_country PRIMARY KEY (id_country),
    CONSTRAINT uq_country_name UNIQUE (name)
);

-- 2.2. state
CREATE TABLE state (
    id_state        SERIAL,
    name            VARCHAR(100) NOT NULL,
    CONSTRAINT pk_state PRIMARY KEY (id_state)
);

-- 2.3. city
CREATE TABLE city (
    id_city         SERIAL,
    name            VARCHAR(100) NOT NULL,
    id_state        INTEGER NOT NULL,
    id_country      INTEGER NOT NULL,
    CONSTRAINT pk_city PRIMARY KEY (id_city),
    CONSTRAINT fk_city_state FOREIGN KEY (id_state) 
        REFERENCES state (id_state) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_city_country FOREIGN KEY (id_country) 
        REFERENCES country (id_country) ON UPDATE CASCADE ON DELETE RESTRICT
);
CREATE INDEX ix_city_state ON city (id_state);
CREATE INDEX ix_city_country ON city (id_country);

-- 2.4. guest
CREATE TABLE guest (
    id_guest        SERIAL,
    first_name      VARCHAR(80) NOT NULL,
    last_name       VARCHAR(80) NOT NULL,
    document_number VARCHAR(30) NOT NULL,
    phone           VARCHAR(20) NOT NULL,
    email           VARCHAR(120),
    id_country      INTEGER NOT NULL,
    CONSTRAINT pk_guest PRIMARY KEY (id_guest),
    CONSTRAINT uq_guest_document UNIQUE (document_number),
    CONSTRAINT fk_guest_country FOREIGN KEY (id_country) 
        REFERENCES country (id_country) ON UPDATE CASCADE ON DELETE RESTRICT
);
CREATE INDEX ix_guest_country ON guest (id_country);

-- 2.5. employee
CREATE TABLE employee (
    id_employee     SERIAL,
    name            VARCHAR(80) NOT NULL,
    last_name       VARCHAR(80) NOT NULL,
    role            VARCHAR(50) NOT NULL,
    CONSTRAINT pk_employee PRIMARY KEY (id_employee)
);

-- 2.6. room_type
CREATE TABLE room_type (
    id_room_type    SERIAL,
    name            VARCHAR(50) NOT NULL,
    capacity        SMALLINT NOT NULL CHECK (capacity > 0),
    base_price      NUMERIC(10, 2) NOT NULL CHECK (base_price >= 0),
    description     VARCHAR(300),
    CONSTRAINT pk_room_type PRIMARY KEY (id_room_type)
);

-- 2.7. room
CREATE TABLE room (
    id_room         SERIAL,
    room_number     VARCHAR(10) NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'Disponible',
    id_room_type    INTEGER NOT NULL,
    CONSTRAINT pk_room PRIMARY KEY (id_room),
    CONSTRAINT uq_room_number UNIQUE (room_number),
    CONSTRAINT fk_room_type FOREIGN KEY (id_room_type) 
        REFERENCES room_type (id_room_type) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_room_status CHECK (status IN ('Disponible', 'Reservada', 'Ocupada', 'Mantenimiento'))
);
CREATE INDEX ix_room_type ON room (id_room_type);

-- 2.8. booking (SIN id_room, tal como ajustó el docente)
CREATE TABLE booking (
    id_booking          SERIAL,
    check_in_date       DATE NOT NULL,
    check_out_date      DATE NOT NULL,
    number_of_guests    SMALLINT NOT NULL CHECK (number_of_guests > 0),
    total_amount        NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (total_amount >= 0),
    status              VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
    id_guest            INTEGER NOT NULL,
    id_employee         INTEGER NOT NULL,
    CONSTRAINT pk_booking PRIMARY KEY (id_booking),
    CONSTRAINT fk_booking_guest FOREIGN KEY (id_guest) 
        REFERENCES guest (id_guest) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_booking_employee FOREIGN KEY (id_employee) 
        REFERENCES employee (id_employee) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_booking_dates CHECK (check_out_date > check_in_date),
    CONSTRAINT chk_booking_status CHECK (status IN ('Pendiente', 'Confirmada', 'Cancelada', 'Finalizada'))
);
CREATE INDEX ix_booking_guest ON booking (id_guest);
CREATE INDEX ix_booking_employee ON booking (id_employee);

-- 2.9. detalle_room (NUEVA TABLA DEL PROFESOR)
CREATE TABLE detalle_room (
    id_booking          INTEGER NOT NULL,
    line_room           INTEGER NOT NULL,
    id_room             INTEGER NOT NULL,
    price_per_night     NUMERIC(10, 2) NOT NULL CHECK (price_per_night >= 0),
    observations        VARCHAR(255),
    CONSTRAINT pk_detalle_room PRIMARY KEY (id_booking, line_room),
    CONSTRAINT fk_detalle_room_booking FOREIGN KEY (id_booking) 
        REFERENCES booking (id_booking) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_detalle_room_room FOREIGN KEY (id_room) 
        REFERENCES room (id_room) ON UPDATE CASCADE ON DELETE RESTRICT
);
CREATE INDEX ix_detalle_room_booking ON detalle_room (id_booking);
CREATE INDEX ix_detalle_room_room ON detalle_room (id_room);

-- 2.10. service
CREATE TABLE service (
    id_service      SERIAL,
    name            VARCHAR(100) NOT NULL,
    price           NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    CONSTRAINT pk_service PRIMARY KEY (id_service)
);

-- 2.11. detalle_service (RENOMBRADA Y CON line_service)
CREATE TABLE detalle_service (
    id_booking          INTEGER NOT NULL,
    line_service        INTEGER NOT NULL,
    id_service          INTEGER NOT NULL,
    CONSTRAINT pk_detalle_service PRIMARY KEY (id_booking, line_service),
    CONSTRAINT fk_detalle_service_booking FOREIGN KEY (id_booking) 
        REFERENCES booking (id_booking) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_detalle_service_service FOREIGN KEY (id_service) 
        REFERENCES service (id_service) ON UPDATE CASCADE ON DELETE RESTRICT
);
CREATE INDEX ix_detalle_service_service ON detalle_service (id_service);

-- 2.12. booking_audit (Auditoría histórica - Requisito 9)
CREATE TABLE booking_audit (
    id_audit        SERIAL PRIMARY KEY,
    id_booking      INTEGER NOT NULL,
    action_type     VARCHAR(10) NOT NULL,
    old_status      VARCHAR(20),
    new_status      VARCHAR(20),
    old_check_in    DATE,
    new_check_in    DATE,
    old_check_out   DATE,
    new_check_out   DATE,
    old_total       NUMERIC(12, 2),
    new_total       NUMERIC(12, 2),
    changed_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    changed_by      VARCHAR(50) NOT NULL DEFAULT CURRENT_USER
);

-- =============================================================================
-- 3. TRIGGERS Y FUNCIONES ACTUALIZADOS
-- =============================================================================

-- Trigger: Evitar solapamiento de fechas al asignar habitación en detalle_room
CREATE OR REPLACE FUNCTION fn_validar_disponibilidad_habitacion_detalle()
RETURNS TRIGGER AS $$
DECLARE
    v_check_in DATE;
    v_check_out DATE;
    v_conflicto_id INTEGER;
BEGIN
    SELECT check_in_date, check_out_date 
    INTO v_check_in, v_check_out
    FROM booking 
    WHERE id_booking = NEW.id_booking;

    SELECT b.id_booking INTO v_conflicto_id
    FROM detalle_room dr
    JOIN booking b ON dr.id_booking = b.id_booking
    WHERE dr.id_room = NEW.id_room
      AND b.status IN ('Pendiente', 'Confirmada')
      AND b.id_booking <> NEW.id_booking
      AND NOT (v_check_out <= b.check_in_date OR v_check_in >= b.check_out_date)
    LIMIT 1;

    IF v_conflicto_id IS NOT NULL THEN
        RAISE EXCEPTION 'REGLA DE NEGOCIO 12/21: La habitación ID % ya está reservada en esas fechas por la reserva #%.',
            NEW.id_room, v_conflicto_id;
    END IF;

    IF NEW.price_per_night IS NULL OR NEW.price_per_night <= 0 THEN
        SELECT rt.base_price INTO NEW.price_per_night
        FROM room r
        JOIN room_type rt ON r.id_room_type = rt.id_room_type
        WHERE r.id_room = NEW.id_room;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validar_disponibilidad_detalle
BEFORE INSERT OR UPDATE OF id_room, price_per_night ON detalle_room
FOR EACH ROW EXECUTE FUNCTION fn_validar_disponibilidad_habitacion_detalle();


-- Trigger: Actualizar el total de la reserva al insertar o cambiar habitaciones o servicios
CREATE OR REPLACE FUNCTION fn_recalcular_total_booking()
RETURNS TRIGGER AS $$
DECLARE
    v_id_booking INTEGER;
    v_dias INTEGER;
    v_total_habitaciones NUMERIC(12, 2) := 0;
    v_total_servicios NUMERIC(12, 2) := 0;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_id_booking := OLD.id_booking;
    ELSE
        v_id_booking := NEW.id_booking;
    END IF;

    SELECT (check_out_date - check_in_date) INTO v_dias
    FROM booking WHERE id_booking = v_id_booking;

    SELECT COALESCE(SUM(price_per_night * v_dias), 0)
    INTO v_total_habitaciones
    FROM detalle_room
    WHERE id_booking = v_id_booking;

    SELECT COALESCE(SUM(s.price), 0)
    INTO v_total_servicios
    FROM detalle_service ds
    JOIN service s ON ds.id_service = s.id_service
    WHERE ds.id_booking = v_id_booking;

    UPDATE booking 
    SET total_amount = (v_total_habitaciones + v_total_servicios)
    WHERE id_booking = v_id_booking;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_recalcular_total_room
AFTER INSERT OR UPDATE OR DELETE ON detalle_room
FOR EACH ROW EXECUTE FUNCTION fn_recalcular_total_booking();

CREATE TRIGGER trg_recalcular_total_service
AFTER INSERT OR UPDATE OR DELETE ON detalle_service
FOR EACH ROW EXECUTE FUNCTION fn_recalcular_total_booking();


-- Trigger: Sincronizar estado de las habitaciones de una reserva
CREATE OR REPLACE FUNCTION fn_sincronizar_estado_habitaciones_reserva()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'Confirmada' THEN
        IF CURRENT_DATE >= NEW.check_in_date AND CURRENT_DATE < NEW.check_out_date THEN
            UPDATE room SET status = 'Ocupada' 
            WHERE id_room IN (SELECT id_room FROM detalle_room WHERE id_booking = NEW.id_booking);
        ELSE
            UPDATE room SET status = 'Reservada' 
            WHERE id_room IN (SELECT id_room FROM detalle_room WHERE id_booking = NEW.id_booking);
        END IF;
    ELSIF NEW.status IN ('Finalizada', 'Cancelada') THEN
        UPDATE room SET status = 'Disponible' 
        WHERE id_room IN (SELECT id_room FROM detalle_room WHERE id_booking = NEW.id_booking);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sincronizar_habitaciones_reserva
AFTER UPDATE OF status ON booking
FOR EACH ROW EXECUTE FUNCTION fn_sincronizar_estado_habitaciones_reserva();


-- Trigger: Auditoría de booking
CREATE OR REPLACE FUNCTION fn_auditar_booking()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO booking_audit (id_booking, action_type, new_status, new_check_in, new_check_out, new_total)
        VALUES (NEW.id_booking, 'INSERT', NEW.status, NEW.check_in_date, NEW.check_out_date, NEW.total_amount);
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        IF (OLD.status <> NEW.status OR OLD.check_in_date <> NEW.check_in_date OR OLD.check_out_date <> NEW.check_out_date OR OLD.total_amount <> NEW.total_amount) THEN
            INSERT INTO booking_audit (id_booking, action_type, old_status, new_status, old_check_in, new_check_in, old_check_out, new_check_out, old_total, new_total)
            VALUES (NEW.id_booking, 'UPDATE', OLD.status, NEW.status, OLD.check_in_date, NEW.check_in_date, OLD.check_out_date, NEW.check_out_date, OLD.total_amount, NEW.total_amount);
        END IF;
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO booking_audit (id_booking, action_type, old_status, old_check_in, old_check_out, old_total)
        VALUES (OLD.id_booking, 'DELETE', OLD.status, OLD.check_in_date, OLD.check_out_date, OLD.total_amount);
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_auditar_booking
AFTER INSERT OR UPDATE OR DELETE ON booking
FOR EACH ROW EXECUTE FUNCTION fn_auditar_booking();


-- =============================================================================
-- 4. VISTAS ACTUALIZADAS (VIEWS)
-- =============================================================================

CREATE OR REPLACE VIEW vw_reservas_completas AS
SELECT 
    b.id_booking AS id_reserva,
    g.first_name || ' ' || g.last_name AS nombre_huesped,
    g.document_number AS documento_huesped,
    g.phone AS telefono_huesped,
    r.room_number AS numero_habitacion,
    rt.name AS tipo_habitacion,
    dr.price_per_night AS precio_noche,
    b.check_in_date AS fecha_ingreso,
    b.check_out_date AS fecha_salida,
    (b.check_out_date - b.check_in_date) AS noches_estadia,
    b.number_of_guests AS numero_huespedes,
    b.total_amount AS total_reserva,
    b.status AS estado_reserva,
    e.name || ' ' || e.last_name AS empleado_atendio
FROM booking b
JOIN guest g ON b.id_guest = g.id_guest
JOIN detalle_room dr ON b.id_booking = dr.id_booking
JOIN room r ON dr.id_room = r.id_room
JOIN room_type rt ON r.id_room_type = rt.id_room_type
JOIN employee e ON b.id_employee = e.id_employee;

CREATE OR REPLACE VIEW vw_estado_habitaciones AS
SELECT 
    r.id_room,
    r.room_number,
    rt.name AS tipo_habitacion,
    rt.capacity AS capacidad_maxima,
    rt.base_price AS precio_base,
    r.status AS estado_actual
FROM room r
JOIN room_type rt ON r.id_room_type = rt.id_room_type;

CREATE OR REPLACE VIEW vw_servicios_reserva AS
SELECT 
    b.id_booking,
    g.first_name || ' ' || g.last_name AS huesped,
    ds.line_service AS linea,
    s.id_service,
    s.name AS servicio,
    s.price AS precio_servicio
FROM detalle_service ds
JOIN booking b ON ds.id_booking = b.id_booking
JOIN guest g ON b.id_guest = g.id_guest
JOIN service s ON ds.id_service = s.id_service;


-- =============================================================================
-- 5. DML: DATOS DE PRUEBA ADAPTADOS AL NUEVO MODELO
-- =============================================================================

INSERT INTO country (name) VALUES ('Colombia'), ('Venezuela'), ('Ecuador'), ('Estados Unidos');
INSERT INTO state (name) VALUES ('Norte de Santander'), ('Santander'), ('Cesar'), ('Antioquia');

INSERT INTO city (name, id_state, id_country) VALUES 
('Ocaña', 1, 1), ('Cúcuta', 1, 1), ('Pamplona', 1, 1),
('Bucaramanga', 2, 1), ('Valledupar', 3, 1), ('Medellín', 4, 1);

INSERT INTO employee (name, last_name, role) VALUES 
('Carlos Andrés', 'Torres Páez', 'Recepcionista'),
('María Fernanda', 'Quintero Lobo', 'Administradora'),
('Javier Enrique', 'Mora Rincón', 'Recepcionista Nocturno');

INSERT INTO room_type (name, capacity, base_price, description) VALUES 
('Suite Don Quesada', 2, 190000.00, 'Suite exclusiva con cama King Size, balcón y sala de estar.'),
('Habitación Estándar', 1, 95000.00, 'Habitación individual con cama semi-doble y baño privado.'),
('Habitación Doble Confort', 2, 140000.00, 'Habitación con dos camas individuales y aire acondicionado.'),
('Habitación Familiar', 4, 220000.00, 'Habitación amplia para familias con dos camas dobles.');

INSERT INTO room (room_number, status, id_room_type) VALUES 
('101', 'Disponible', 2),
('102', 'Ocupada',    3),
('103', 'Disponible', 3),
('201', 'Reservada',  1),
('202', 'Disponible', 1),
('301', 'Disponible', 4);

INSERT INTO service (name, price) VALUES 
('Desayuno Típico Ocañero', 0.00),
('Parqueadero Privado', 0.00),
('Lavandería y Planchado Express', 18000.00),
('Servicio a la Habitación (Cena)', 32000.00),
('Bebidas y Minibar', 12000.00);

INSERT INTO guest (first_name, last_name, document_number, phone, email, id_country) VALUES 
('Juan Camilo', 'Pérez Duarte', '1091234567', '3124567890', 'juan.perez@gmail.com', 1),
('Laura Marcela', 'Álvarez Vega', '1098765432', '3159876543', 'laura.alvarez@outlook.com', 1),
('Diego Fernando', 'García Salcedo', '88234561', '3201239874', 'diego.garcia@hotmail.com', 1),
('Carlos', 'González Smith', 'PAS987123', '3001122334', 'cgonzalez@usa.net', 4);

-- Inserción de reservas (booking ya no tiene id_room)
INSERT INTO booking (check_in_date, check_out_date, number_of_guests, total_amount, status, id_guest, id_employee) VALUES 
('2026-09-10', '2026-09-13', 2, 0, 'Finalizada', 1, 1),
('2026-10-22', '2026-10-25', 2, 0, 'Confirmada', 2, 1),
('2026-11-01', '2026-11-04', 2, 0, 'Confirmada', 3, 2);

-- Inserción en detalle_room (aquí se enlaza la habitación y su tarifa por noche)
INSERT INTO detalle_room (id_booking, line_room, id_room, price_per_night, observations) VALUES 
(1, 1, 4, 190000.00, 'Huésped VIP - balcón con vista'),
(2, 1, 2, 140000.00, 'Habitación con cama doble'),
(3, 1, 4, 190000.00, 'Reserva confirmada con anticipo');

-- Inserción en detalle_service (renombrada con line_service)
INSERT INTO detalle_service (id_booking, line_service, id_service) VALUES 
(1, 1, 1), (1, 2, 2), (1, 3, 3),
(2, 1, 1), (2, 2, 4),
(3, 1, 1), (3, 2, 2);
