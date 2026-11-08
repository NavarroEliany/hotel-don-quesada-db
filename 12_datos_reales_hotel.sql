
-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje
-- HOTEL: Don Quesada Boutique
-- ARCHIVO: 12_plantilla_datos_reales_hotel.sql
-- DESCRIPCIÓN: Registro de habitaciones, tarifas y servicios reales del hotel.
-- =============================================================================


-- =============================================================================
-- 1. TIPOS DE HABITACIONES Y TARIFAS
-- =============================================================================

INSERT INTO room_type (name, capacity, base_price, description) VALUES

('Habitación Doble Cama Sencilla', 2, 80000.00,
 'Habitación con dos camas sencillas. Tarifa de $80.000 por persona y noche. Desayuno incluido.'),

('Habitación Suite Jacuzzi', 2, 270000.00,
 'Suite con jacuzzi. Tarifa de $270.000 por noche. Desayunos incluidos.'),

('Habitación Familiar Múltiple', 6, 90000.00,
 'Habitación familiar. De 4 a 6 adultos: $90.000 por persona. Tres adultos: $100.000 por persona. Pareja: $250.000 por noche. Niños menores de 10 años: $40.000. Niños de 10 a 14 años: $50.000. Desde los 15 años se cobra tarifa de adulto. Desayunos incluidos.'),

('Habitación Cama Nido', 2, 230000.00,
 'Habitación con cama nido. Tarifa de $230.000 por noche.'),

('Habitación para Pareja', 2, 170000.00,
 'Habitación para dos personas. Tarifa de $170.000 por noche. Desayunos incluidos.'),

('Habitación Individual', 1, 110000.00,
 'Habitación para una persona. Tarifa de $110.000 por noche. Desayuno incluido.');


-- =============================================================================
-- 2. HABITACIONES FÍSICAS CON NÚMEROS CONFIRMADOS
-- =============================================================================

-- Habitaciones con dos camas sencillas: 206 y 306.

INSERT INTO room (room_number, status, id_room_type) VALUES
('206', 'Disponible',
 (SELECT id_room_type FROM room_type WHERE name = 'Habitación Doble Cama Sencilla')),

('306', 'Disponible',
 (SELECT id_room_type FROM room_type WHERE name = 'Habitación Doble Cama Sencilla'));


-- Suite con jacuzzi: 301.

INSERT INTO room (room_number, status, id_room_type) VALUES
('301', 'Disponible',
 (SELECT id_room_type FROM room_type WHERE name = 'Habitación Suite Jacuzzi'));


-- Habitación familiar: 307.

INSERT INTO room (room_number, status, id_room_type) VALUES
('307', 'Disponible',
 (SELECT id_room_type FROM room_type WHERE name = 'Habitación Familiar Múltiple'));


-- Habitaciones con cama nido: 303, 304 y 305.

INSERT INTO room (room_number, status, id_room_type) VALUES
('303', 'Disponible',
 (SELECT id_room_type FROM room_type WHERE name = 'Habitación Cama Nido')),

('304', 'Disponible',
 (SELECT id_room_type FROM room_type WHERE name = 'Habitación Cama Nido')),

('305', 'Disponible',
 (SELECT id_room_type FROM room_type WHERE name = 'Habitación Cama Nido'));


-- NOTA:
-- El hotel cuenta con 27 habitaciones en total.
-- Quedan pendientes los números de las otras 20 habitaciones.
-- Se deben registrar cuando el hotel proporcione su distribución exacta.


-- =============================================================================
-- 3. SERVICIOS E INSTALACIONES DEL HOTEL
-- =============================================================================

INSERT INTO service (name, price) VALUES

-- Servicios incluidos en el valor de la habitación.

('Desayuno incluido', 0.00),

('Retoque de aseo', 0.00),

('Ducha con agua caliente', 0.00),

('Wi-Fi', 0.00),

('Netflix', 0.00),

('Parqueadero privado', 0.00),

-- Servicios con costo adicional.

('Lavandería por prenda', 2000.00),

('Servicio de planchado por prenda', 2000.00);


-- =============================================================================
-- 4. INFORMACIÓN DE INSTALACIONES Y SERVICIOS COMPLEMENTARIOS
-- =============================================================================

-- Las habitaciones cuentan normalmente con:
-- * Ducha de agua caliente.
-- * Pequeño minibar.
-- * Conexión Wi-Fi.
-- * Acceso a Netflix.
-- * Parqueadero privado.
--
-- El hotel tiene conexión directa con el Restaurante Boyacá.
-- Los consumos del minibar y del restaurante no tienen tarifas
-- especificadas en esta plantilla.


-- =============================================================================
-- 5. PERSONAL DEL HOTEL
-- =============================================================================

-- Distribución real del personal:
--
-- 3 Camareras.
-- 3 Recepcionistas.
-- 1 Empleado de oficios varios.
--
-- TOTAL: 7 EMPLEADOS.
--
-- PENDIENTE:
-- Registrar nombres y apellidos reales de los empleados.
-- No se insertan registros ficticios porque la tabla employee
-- requiere información personal que todavía no ha sido suministrada.


