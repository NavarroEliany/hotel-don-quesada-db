-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje
-- HOTEL: Don Quesada Hotel Boutique (Ocaña, Norte de Santander)
-- ARCHIVO: 03_test_queries.sql (Consultas de Verificación y Reportes)
-- =============================================================================

-- 1. CONSULTAR TODAS LAS RESERVAS CON DATOS COMPLETOS
-- Muestra el huésped, el empleado que atendió, la habitación, el tipo y fechas
SELECT 
    b.id_booking AS id_reserva,
    g.first_name || ' ' || g.last_name AS huesped,
    g.document_number AS documento,
    r.room_number AS habitacion,
    rt.name AS tipo_habitacion,
    b.check_in_date AS fecha_ingreso,
    b.check_out_date AS fecha_salida,
    b.number_of_guests AS num_huespedes,
    b.status AS estado_reserva,
    b.total_amount AS total_cobrado,
    e.name || ' ' || e.last_name AS atendido_por
FROM booking b
JOIN guest g ON b.id_guest = g.id_guest
JOIN room r ON b.id_room = r.id_room
JOIN room_type rt ON r.id_room_type = rt.id_room_type
JOIN employee e ON b.id_employee = e.id_employee
ORDER BY b.id_booking;

-- 2. CONSULTAR SERVICIOS INCLUIDOS Y ADICIONALES POR RESERVA
SELECT 
    b.id_booking AS id_reserva,
    g.first_name || ' ' || g.last_name AS huesped,
    rd.line_booking AS linea,
    s.name AS servicio,
    s.price AS precio_servicio
FROM reservation_details rd
JOIN booking b ON rd.id_booking = b.id_booking
JOIN guest g ON b.id_guest = g.id_guest
JOIN service s ON rd.id_service = s.id_service
ORDER BY b.id_booking, rd.line_booking;

-- 3. REQUISITO 4: CONSULTAR HABITACIONES DISPONIBLES PARA UN RANGO DE FECHAS
-- Ejemplo: Buscar habitaciones libres entre '2026-11-10' y '2026-11-15'
SELECT 
    r.id_room,
    r.room_number,
    rt.name AS tipo,
    rt.capacity AS capacidad,
    rt.base_price AS precio_noche
FROM room r
JOIN room_type rt ON r.id_room_type = rt.id_room_type
WHERE r.id_room NOT IN (
    -- Habitaciones con reservas que se solapan en esas fechas
    SELECT id_room 
    FROM booking 
    WHERE status IN ('Confirmada', 'Pendiente')
      AND NOT (check_out_date <= '2026-11-10' OR check_in_date >= '2026-11-15')
)
ORDER BY r.room_number;

-- 4. TOTAL RECAUDADO Y OCUPACIÓN POR TIPO DE HABITACIÓN
SELECT 
    rt.name AS tipo_habitacion,
    COUNT(b.id_booking) AS total_reservas,
    COALESCE(SUM(b.total_amount), 0) AS total_ingresos
FROM room_type rt
LEFT JOIN room r ON rt.id_room_type = r.id_room_type
LEFT JOIN booking b ON r.id_room = b.id_room
GROUP BY rt.name
ORDER BY total_ingresos DESC;
