-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje
-- HOTEL: Don Quesada Hotel Boutique (Ocaña, Norte de Santander)
-- MODELO FINAL AJUSTADO SEGÚN REVISIÓN DOCENTE
-- =============================================================================

DROP TABLE IF EXISTS detalle_service CASCADE;
DROP TABLE IF EXISTS detalle_room CASCADE;
DROP TABLE IF EXISTS reservation_details CASCADE;
DROP TABLE IF EXISTS service CASCADE;
DROP TABLE IF EXISTS booking CASCADE;
DROP TABLE IF EXISTS room CASCADE;
DROP TABLE IF EXISTS room_type CASCADE;
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS guest CASCADE;
DROP TABLE IF EXISTS city CASCADE;
DROP TABLE IF EXISTS state CASCADE;
DROP TABLE IF EXISTS country CASCADE;

-- 1. country
CREATE TABLE country (
    id_country      SERIAL,
    name            VARCHAR(100) NOT NULL,
    CONSTRAINT pk_country PRIMARY KEY (id_country),
    CONSTRAINT uq_country_name UNIQUE (name)
);

-- 2. state
CREATE TABLE state (
    id_state        SERIAL,
    name            VARCHAR(100) NOT NULL,
    CONSTRAINT pk_state PRIMARY KEY (id_state)
);

-- 3. city
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

-- 4. guest
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

-- 5. employee
CREATE TABLE employee (
    id_employee     SERIAL,
    name            VARCHAR(80) NOT NULL,
    last_name       VARCHAR(80) NOT NULL,
    role            VARCHAR(50) NOT NULL,
    CONSTRAINT pk_employee PRIMARY KEY (id_employee)
);

-- 6. room_type
CREATE TABLE room_type (
    id_room_type    SERIAL,
    name            VARCHAR(50) NOT NULL,
    capacity        SMALLINT NOT NULL CHECK (capacity > 0),
    base_price      NUMERIC(10, 2) NOT NULL CHECK (base_price >= 0),
    description     VARCHAR(300),
    CONSTRAINT pk_room_type PRIMARY KEY (id_room_type)
);

-- 7. room
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

-- 8. booking (SIN id_room)
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

-- 9. detalle_room (NUEVA TABLA)
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

-- 10. service
CREATE TABLE service (
    id_service      SERIAL,
    name            VARCHAR(100) NOT NULL,
    price           NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    CONSTRAINT pk_service PRIMARY KEY (id_service)
);

-- 11. detalle_service (RENOMBRADA Y CON line_service)
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
