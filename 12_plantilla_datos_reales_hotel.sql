-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje - Hotel Don Quesada Boutique
-- ARCHIVO: 12_plantilla_datos_reales_hotel.sql
-- INSTRUCCIONES:
-- Cuando el dueño del hotel te entregue la información real, solo reemplazas
-- o agregas las líneas de este archivo y lo ejecutas en pgAdmin en 1 segundo.
-- =============================================================================

-- 1. TIPOS DE HABITACIONES REALES (Ejemplo: Suite, Estándar, Doble, Familiar...)
-- Campos: (name, capacity, base_price, description)
INSERT INTO room_type (name, capacity, base_price, description) VALUES
('Suite Don Quesada', 2, 190000.00, 'Cama King, aire acondicionado, balcón con vista y sala de estar.'),
('Habitación Doble', 2, 140000.00, 'Dos camas individuales o una doble, wifi y baño privado.'),
('Habitación Familiar', 4, 220000.00, 'Dos camas dobles, ideal para grupos familiares.'),
('Habitación Estándar', 1, 95000.00, 'Cama individual o semi-doble, televisión y baño.');

-- 2. HABITACIONES FÍSICAS REALES
-- Campos: (room_number, status, id_room_type)
-- (id_room_type 1=Suite, 2=Doble, 3=Familiar, 4=Estándar)
INSERT INTO room (room_number, status, id_room_type) VALUES
('101', 'Disponible', 4),
('102', 'Disponible', 2),
('103', 'Disponible', 2),
('201', 'Disponible', 1),
('202', 'Disponible', 1),
('301', 'Disponible', 3);

-- 3. SERVICIOS REALES QUE OFRECE EL HOTEL
-- Campos: (name, price)
INSERT INTO service (name, price) VALUES
('Desayuno Típico Ocañero', 0.00),         -- Incluido en la estadía
('Parqueadero Privado', 0.00),             -- Incluido
('Wifi de Alta Velocidad', 0.00),          -- Incluido
('Lavandería y Planchado', 18000.00),      -- Con costo adicional
('Servicio a la Habitación (Cena)', 32000.00),
('Bebidas y Minibar', 12000.00);

-- 4. EMPLEADOS REALES Y SU ROL
-- Campos: (name, last_name, role)
INSERT INTO employee (name, last_name, role) VALUES
('Carlos Andrés', 'Torres', 'Recepcionista'),
('María Fernanda', 'Quintero', 'Administradora'),
('Javier Enrique', 'Mora', 'Recepcionista Nocturno');
