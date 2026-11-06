-- =============================================================================
-- PROYECTO: Sistema de Gestión de Reservas y Hospedaje
-- HOTEL: Don Quesada Hotel Boutique (Ocaña, Norte de Santander)
-- ARCHIVO: 05_audit_log.sql (Auditoría e Historial de Cambios)
-- =============================================================================

-- =============================================================================
-- CUMPLE EL REQUISITO DE INFORMACIÓN 9 Y LA REGLA DE NEGOCIO 22:
-- "Se requiere mantener un registro de los cambios importantes realizados sobre
--  las reservas (fechas, estado, total, usuario y fecha de modificación)"
-- =============================================================================

-- 1. Tabla para registrar los cambios históricos de reservas
CREATE TABLE IF NOT EXISTS booking_audit (
    id_audit        SERIAL PRIMARY KEY,
    id_booking      INTEGER NOT NULL,
    action_type     VARCHAR(10) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
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

-- 2. Función disparadora que captura qué cambió
CREATE OR REPLACE FUNCTION fn_auditar_booking()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO booking_audit (
            id_booking, action_type, new_status, new_check_in, new_check_out, new_total
        ) VALUES (
            NEW.id_booking, 'INSERT', NEW.status, NEW.check_in_date, NEW.check_out_date, NEW.total_amount
        );
        RETURN NEW;

    ELSIF (TG_OP = 'UPDATE') THEN
        -- Solo auditar si hubo cambio real en estado, fechas o valor total
        IF (OLD.status <> NEW.status OR 
            OLD.check_in_date <> NEW.check_in_date OR 
            OLD.check_out_date <> NEW.check_out_date OR 
            OLD.total_amount <> NEW.total_amount) THEN
            
            INSERT INTO booking_audit (
                id_booking, action_type,
                old_status, new_status,
                old_check_in, new_check_in,
                old_check_out, new_check_out,
                old_total, new_total
            ) VALUES (
                NEW.id_booking, 'UPDATE',
                OLD.status, NEW.status,
                OLD.check_in_date, NEW.check_in_date,
                OLD.check_out_date, NEW.check_out_date,
                OLD.total_amount, NEW.total_amount
            );
        END IF;
        RETURN NEW;

    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO booking_audit (
            id_booking, action_type,
            old_status, old_check_in, old_check_out, old_total
        ) VALUES (
            OLD.id_booking, 'DELETE',
            OLD.status, OLD.check_in_date, OLD.check_out_date, OLD.total_amount
        );
        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- 3. Crear el Trigger de Auditoría
DROP TRIGGER IF EXISTS trg_auditar_booking ON booking;

CREATE TRIGGER trg_auditar_booking
AFTER INSERT OR UPDATE OR DELETE ON booking
FOR EACH ROW
EXECUTE FUNCTION fn_auditar_booking();
