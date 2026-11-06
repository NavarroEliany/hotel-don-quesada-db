-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje
-- HOTEL: Don Quesada Hotel Boutique (Ocaña, Norte de Santander)
-- ARCHIVO: 08_security_roles.sql (Seguridad, Roles y Privilegios DCL)
-- =============================================================================

-- =============================================================================
-- BUENA PRÁCTICA DE SEGURIDAD (OWASP / DB SECURITY):
-- El Backend y la aplicación web nunca deben conectarse con el superusuario 'postgres'.
-- Se crea un usuario exclusivo con los permisos necesarios para la operación.
-- =============================================================================

-- 1. Crear el usuario para la aplicación (si no existe)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'hotel_app_user') THEN
        CREATE ROLE hotel_app_user WITH LOGIN PASSWORD 'HotelDonQuesada2026*';
    END IF;
END
$$;

-- 2. Asignar permisos sobre la base de datos y esquema
GRANT CONNECT ON DATABASE hotel_don_quesada_db TO hotel_app_user;
GRANT USAGE ON SCHEMA public TO hotel_app_user;

-- 3. Permisos de lectura, inserción y actualización sobre las tablas
GRANT SELECT, INSERT, UPDATE ON TABLE 
    country, state, city, employee, guest, 
    room_type, room, booking, service, reservation_details 
TO hotel_app_user;

-- Permiso de lectura sobre la auditoría (solo lectura para la app)
GRANT SELECT ON TABLE booking_audit TO hotel_app_user;

-- 4. Permisos sobre secuencias (para que pueda insertar con IDs autoincrementables)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO hotel_app_user;

-- 5. Permiso de lectura sobre todas las vistas
GRANT SELECT ON 
    vw_reservas_completas, 
    vw_estado_habitaciones, 
    vw_servicios_reserva, 
    vw_reporte_ingresos_habitacion 
TO hotel_app_user;

-- 6. Permiso de ejecución sobre los procedimientos almacenados y funciones
GRANT EXECUTE ON PROCEDURE sp_registrar_reserva(VARCHAR, VARCHAR, DATE, DATE, INTEGER, INTEGER, INTEGER) TO hotel_app_user;
GRANT EXECUTE ON PROCEDURE sp_cancelar_reserva(INTEGER) TO hotel_app_user;
GRANT EXECUTE ON PROCEDURE sp_agregar_servicio_reserva(INTEGER, INTEGER) TO hotel_app_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO hotel_app_user;
