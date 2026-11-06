-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje
-- HOTEL: Don Quesada Hotel Boutique (Ocaña, Norte de Santander)
-- ARCHIVO: 06_views.sql (Vistas para Consultas Rápidas y Backend)
-- =============================================================================

-- =============================================================================
-- VISTA 1: Información Completa de Reservas (Dashboard Recepción / Backend)
-- Requisito 7: Consultar historial y relación huésped-habitación-reserva
-- =============================================================================
CREATE OR REPLACE VIEW vw_reservas_completas AS
SELECT 
    b.id_booking AS id_reserva,
    g.id_guest AS id_huesped,
    g.first_name || ' ' || g.last_name AS nombre_huesped,
    g.document_number AS documento_huesped,
    g.phone AS telefono_huesped,
    g.email AS email_huesped,
    c.name AS pais_origen,
    r.id_room AS id_habitacion,
    r.room_number AS numero_habitacion,
    rt.name AS tipo_habitacion,
    rt.base_price AS tarifa_por_noche,
    b.check_in_date AS fecha_ingreso,
    b.check_out_date AS fecha_salida,
    (b.check_out_date - b.check_in_date) AS noches_estadia,
    b.number_of_guests AS numero_huespedes,
    b.total_amount AS total_cobrado,
    b.status AS estado_reserva,
    e.id_employee AS id_empleado,
    e.name || ' ' || e.last_name AS empleado_atendio,
    e.role AS cargo_empleado
FROM booking b
JOIN guest g ON b.id_guest = g.id_guest
JOIN country c ON g.id_country = c.id_country
JOIN room r ON b.id_room = r.id_room
JOIN room_type rt ON r.id_room_type = rt.id_room_type
JOIN employee e ON b.id_employee = e.id_employee;

-- =============================================================================
-- VISTA 2: Estado Actual de Habitaciones (Para saber qué está libre hoy)
-- Requisito 2 y 4: Disponibilidad de habitaciones
-- =============================================================================
CREATE OR REPLACE VIEW vw_estado_habitaciones AS
SELECT 
    r.id_room,
    r.room_number,
    rt.name AS tipo_habitacion,
    rt.capacity AS capacidad_maxima,
    rt.base_price AS precio_noche,
    r.status AS estado_actual,
    -- Si está ocupada hoy, muestra quién está alojado
    (
        SELECT g.first_name || ' ' || g.last_name
        FROM booking b
        JOIN guest g ON b.id_guest = g.id_guest
        WHERE b.id_room = r.id_room 
          AND b.status = 'Confirmada'
          AND CURRENT_DATE >= b.check_in_date AND CURRENT_DATE < b.check_out_date
        LIMIT 1
    ) AS ocupante_actual
FROM room r
JOIN room_type rt ON r.id_room_type = rt.id_room_type;

-- =============================================================================
-- VISTA 3: Detalle de Servicios Consumidos por Reserva
-- Requisito 5 y 7: Servicios adicionales e incluidos por reserva
-- =============================================================================
CREATE OR REPLACE VIEW vw_servicios_reserva AS
SELECT 
    b.id_booking,
    g.first_name || ' ' || g.last_name AS huesped,
    rd.line_booking AS linea,
    s.id_service,
    s.name AS servicio,
    s.price AS precio_servicio
FROM reservation_details rd
JOIN booking b ON rd.id_booking = b.id_booking
JOIN guest g ON b.id_guest = g.id_guest
JOIN service s ON rd.id_service = s.id_service;

-- =============================================================================
-- VISTA 4: Reporte de Ocupación e Ingresos por Tipo de Habitación
-- Requisito 10: Analizar ocupación y valores cobrados para toma de decisiones
-- =============================================================================
CREATE OR REPLACE VIEW vw_reporte_ingresos_habitacion AS
SELECT 
    rt.name AS tipo_habitacion,
    COUNT(b.id_booking) AS total_reservas_realizadas,
    COALESCE(SUM(b.total_amount), 0) AS ingresos_totales,
    COALESCE(ROUND(AVG(b.total_amount), 2), 0) AS promedio_por_reserva
FROM room_type rt
LEFT JOIN room r ON rt.id_room_type = r.id_room_type
LEFT JOIN booking b ON r.id_room = b.id_room AND b.status IN ('Confirmada', 'Finalizada')
GROUP BY rt.name;
