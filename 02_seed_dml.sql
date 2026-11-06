-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje
-- HOTEL: Don Quesada Hotel Boutique (Ocaña, Norte de Santander)
-- ARCHIVO: 02_seed_dml.sql (Datos de Prueba para Modelo Final)
-- =============================================================================

-- 1. Países
INSERT INTO country (name) VALUES 
('Colombia'), ('Venezuela'), ('Ecuador'), ('Estados Unidos');

-- 2. Departamentos
INSERT INTO state (name) VALUES 
('Norte de Santander'), ('Santander'), ('Cesar'), ('Antioquia');

-- 3. Ciudades
INSERT INTO city (name, id_state, id_country) VALUES 
('Ocaña', 1, 1), ('Cúcuta', 1, 1), ('Pamplona', 1, 1),
('Bucaramanga', 2, 1), ('Valledupar', 3, 1), ('Medellín', 4, 1);

-- 4. Empleados
INSERT INTO employee (name, last_name, role) VALUES 
('Carlos Andrés', 'Torres Páez', 'Recepcionista'),
('María Fernanda', 'Quintero Lobo', 'Administradora'),
('Javier Enrique', 'Mora Rincón', 'Recepcionista Nocturno');

-- 5. Tipos de Habitación
INSERT INTO room_type (name, capacity, base_price, description) VALUES 
('Suite Don Quesada', 2, 190000.00, 'Suite exclusiva con cama King Size, sala de estar, balcón privado y vista.'),
('Habitación Estándar', 1, 95000.00, 'Habitación individual con cama semi-doble, TV Smart, wifi y baño privado.'),
('Habitación Doble Confort', 2, 140000.00, 'Habitación espaciosa con dos camas individuales, aire acondicionado y escritorio.'),
('Habitación Familiar', 4, 220000.00, 'Habitación amplia ideal para familias, incluye dos camas dobles y espacio de confort.');

-- 6. Habitaciones
INSERT INTO room (room_number, status, id_room_type) VALUES 
('101', 'Disponible', 2),
('102', 'Ocupada',    3),
('103', 'Disponible', 3),
('201', 'Reservada',  1),
('202', 'Disponible', 1),
('301', 'Disponible', 4);

-- 7. Servicios
INSERT INTO service (name, price) VALUES 
('Desayuno Típico Ocañero', 0.00),
('Parqueadero Privado', 0.00),
('Lavandería y Planchado Express', 18000.00),
('Servicio a la Habitación (Cena)', 32000.00),
('Bebidas y Minibar', 12000.00);

-- 8. Huéspedes
INSERT INTO guest (first_name, last_name, document_number, phone, email, id_country) VALUES 
('Juan Camilo', 'Pérez Duarte', '1091234567', '3124567890', 'juan.perez@gmail.com', 1),
('Laura Marcela', 'Álvarez Vega', '1098765432', '3159876543', 'laura.alvarez@outlook.com', 1),
('Diego Fernando', 'García Salcedo', '88234561', '3201239874', 'diego.garcia@hotmail.com', 1),
('Carlos', 'González Smith', 'PAS987123', '3001122334', 'cgonzalez@usa.net', 4);

-- 9. Reservas (en booking, sin id_room)
INSERT INTO booking (check_in_date, check_out_date, number_of_guests, total_amount, status, id_guest, id_employee) VALUES 
('2026-09-10', '2026-09-13', 2, 0, 'Finalizada', 1, 1),
('2026-10-22', '2026-10-25', 2, 0, 'Confirmada', 2, 1),
('2026-11-01', '2026-11-04', 2, 0, 'Confirmada', 3, 2);

-- 10. Detalle de Habitaciones (detalle_room)
INSERT INTO detalle_room (id_booking, line_room, id_room, price_per_night, observations) VALUES 
(1, 1, 4, 190000.00, 'Huésped VIP - balcón con vista'),
(2, 1, 2, 140000.00, 'Habitación con cama doble'),
(3, 1, 4, 190000.00, 'Reserva confirmada con anticipo');

-- 11. Detalle de Servicios (detalle_service con line_service)
INSERT INTO detalle_service (id_booking, line_service, id_service) VALUES 
(1, 1, 1), (1, 2, 2), (1, 3, 3),
(2, 1, 1), (2, 2, 4),
(3, 1, 1), (3, 2, 2);
