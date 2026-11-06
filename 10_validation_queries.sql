-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje - Hotel Don Quesada Boutique
-- ARCHIVO: 10_validation_queries.sql
-- CONSULTAS DE INTEGRIDAD, EVIDENCIA E8 Y PREPARACIÓN PARA EL PARCIAL (PUNTO 3)
-- =============================================================================

-- =============================================================================
-- PARTE A: VERIFICACIÓN DE CONTEO Y COMPLETITUD (EVIDENCIA E8)
-- =============================================================================

-- 1. Verificar el total de registros en cada tabla poblada con IA
SELECT 'guest' AS tabla, COUNT(*) AS cantidad FROM guest
UNION ALL
SELECT 'booking' AS tabla, COUNT(*) AS cantidad FROM booking
UNION ALL
SELECT 'detalle_room' AS tabla, COUNT(*) AS cantidad FROM detalle_room
UNION ALL
SELECT 'detalle_service' AS tabla, COUNT(*) AS cantidad FROM detalle_service;

-- 2. Verificar que no existan documentos duplicados en guest (Cumplimiento de UNIQUE)
SELECT document_number, COUNT(*) AS duplicados
FROM guest
GROUP BY document_number
HAVING COUNT(*) > 1;
-- Resultado esperado: 0 filas (integridad de unicidad perfecta).

-- 3. Verificar que no existan fechas inválidas (check_out <= check_in)
SELECT id_booking, check_in_date, check_out_date 
FROM booking
WHERE check_out_date <= check_in_date;
-- Resultado esperado: 0 filas (cumple Regla de Negocio 11).

-- 4. Verificar integridad referencial: Huéspedes sin país o Reservas con huésped inexistente
SELECT b.id_booking, b.id_guest 
FROM booking b
LEFT JOIN guest g ON b.id_guest = g.id_guest
WHERE g.id_guest IS NULL;
-- Resultado esperado: 0 filas (cero huérfanos).


-- =============================================================================
-- PARTE B: CONSULTAS CON JOINS (RÚBRICA PUNTO 3 - VALOR 1.0)
-- =============================================================================

-- Consulta 1: Relacionar 3 tablas para listar reservas, huésped y habitación asignada
SELECT 
    b.id_booking AS reserva,
    g.first_name || ' ' || g.last_name AS huesped,
    g.document_number AS documento,
    r.room_number AS habitacion,
    dr.price_per_night AS tarifa_noche,
    b.check_in_date AS fecha_ingreso,
    b.check_out_date AS fecha_salida,
    b.status AS estado
FROM booking b
INNER JOIN guest g ON b.id_guest = g.id_guest
INNER JOIN detalle_room dr ON b.id_booking = dr.id_booking
INNER JOIN room r ON dr.id_room = r.id_room
ORDER BY b.id_booking ASC
LIMIT 15;

-- Consulta 2: LEFT JOIN para ver todas las habitaciones y cuántas veces han sido reservadas
SELECT 
    r.room_number AS habitacion,
    rt.name AS tipo,
    COUNT(dr.id_booking) AS total_veces_reservada
FROM room r
INNER JOIN room_type rt ON r.id_room_type = rt.id_room_type
LEFT JOIN detalle_room dr ON r.id_room = dr.id_room
GROUP BY r.room_number, rt.name
ORDER BY total_veces_reservada DESC;


-- =============================================================================
-- PARTE C: FUNCIONES AGREGADAS + GROUP BY + HAVING (RÚBRICA PUNTO 3 - VALOR 1.0)
-- =============================================================================

-- Consulta 3: Total recaudado, promedio, mínimo y máximo valor por estado de reserva
SELECT 
    status AS estado_reserva,
    COUNT(*) AS total_reservas,
    SUM(total_amount) AS total_recaudado,
    ROUND(AVG(total_amount), 2) AS promedio_recaudado,
    MIN(total_amount) AS valor_minimo,
    MAX(total_amount) AS valor_maximo
FROM booking
GROUP BY status
ORDER BY total_recaudado DESC;

-- Consulta 4: Huéspedes frecuentes con más de 2 reservas (Uso de HAVING)
SELECT 
    g.id_guest,
    g.first_name || ' ' || g.last_name AS nombre_huesped,
    g.document_number AS documento,
    COUNT(b.id_booking) AS numero_de_reservas,
    SUM(b.total_amount) AS inversion_total
FROM guest g
INNER JOIN booking b ON g.id_guest = b.id_guest
GROUP BY g.id_guest, g.first_name, g.last_name, g.document_number
HAVING COUNT(b.id_booking) >= 2
ORDER BY numero_de_reservas DESC, inversion_total DESC
LIMIT 10;
