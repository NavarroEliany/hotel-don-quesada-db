import os
import csv

data_dir = r"C:\Users\COMPUMAX\.gemini\antigravity\scratch\hotel_don_quesada\datos_sinteticos"
sql_file = r"C:\Users\COMPUMAX\.gemini\antigravity\scratch\hotel_don_quesada\09_import_synthetic_data.sql"

def read_csv(filename):
    with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    return headers, rows

guest_headers, guest_rows = read_csv("guest_definitivo.csv")
booking_headers, booking_rows = read_csv("booking_definitivo.csv")
detalle_room_headers, detalle_room_rows = read_csv("detalle_room_definitivo.csv")
detalle_service_headers, detalle_service_rows = read_csv("detalle_service_definitivo.csv")

with open(sql_file, 'w', encoding='utf-8') as f:
    f.write("""-- =============================================================================
-- SISTEMA DE GESTIÓN DE RESERVAS Y HOSPEDAJE - HOTEL DON QUESADA BOUTIQUE
-- ARCHIVO: 09_import_synthetic_data.sql
-- POBLAMIENTO MASIVO DE DATOS SINTÉTICOS GENERADOS CON IA
-- =============================================================================

-- 1. Limpiar los datos de prueba anteriores para evitar duplicados de clave primaria (id 1, 2, 3...)
TRUNCATE TABLE detalle_service, detalle_room, booking, guest RESTART IDENTITY CASCADE;

-- 2. Desactivar temporalmente disparadores de validación para carga masiva rápida (Buena práctica DBA)
ALTER TABLE booking DISABLE TRIGGER trg_auditar_booking;
ALTER TABLE detalle_room DISABLE TRIGGER trg_validar_disponibilidad_detalle;
ALTER TABLE detalle_room DISABLE TRIGGER trg_recalcular_total_room;
ALTER TABLE detalle_service DISABLE TRIGGER trg_recalcular_total_service;

-- =============================================================================
-- 1. POBLAR TABLA: guest (1000 REGISTROS)
-- =============================================================================
INSERT INTO guest (id_guest, first_name, last_name, document_number, phone, email, id_country) VALUES
""")
    guest_lines = []
    for r in guest_rows:
        escaped_fn = r[1].replace("'", "''")
        escaped_ln = r[2].replace("'", "''")
        guest_lines.append(f"({r[0]}, '{escaped_fn}', '{escaped_ln}', '{r[3]}', '{r[4]}', '{r[5]}', {r[6]})")
    f.write(",\n".join(guest_lines))
    f.write(";\n\n")

    f.write("""-- Sincronizar secuencia autoincremental de guest
SELECT setval('guest_id_guest_seq', (SELECT MAX(id_guest) FROM guest));

-- =============================================================================
-- 2. POBLAR TABLA: booking (1000 REGISTROS)
-- =============================================================================
INSERT INTO booking (id_booking, check_in_date, check_out_date, number_of_guests, total_amount, status, id_guest, id_employee) VALUES
""")
    booking_lines = []
    for r in booking_rows:
        booking_lines.append(f"({r[0]}, '{r[1]}', '{r[2]}', {r[3]}, {r[4]}, '{r[5]}', {r[6]}, {r[7]})")
    f.write(",\n".join(booking_lines))
    f.write(";\n\n")

    f.write("""-- Sincronizar secuencia autoincremental de booking
SELECT setval('booking_id_booking_seq', (SELECT MAX(id_booking) FROM booking));

-- =============================================================================
-- 3. POBLAR TABLA: detalle_room (200 REGISTROS)
-- =============================================================================
INSERT INTO detalle_room (id_booking, line_room, id_room, price_per_night, observations) VALUES
""")
    room_lines = []
    for r in detalle_room_rows:
        escaped_obs = r[4].replace("'", "''")
        room_lines.append(f"({r[0]}, {r[1]}, {r[2]}, {r[3]}, '{escaped_obs}')")
    f.write(",\n".join(room_lines))
    f.write(";\n\n")

    f.write("""-- =============================================================================
-- 4. POBLAR TABLA: detalle_service (200 REGISTROS)
-- =============================================================================
INSERT INTO detalle_service (id_booking, line_service, id_service) VALUES
""")
    service_lines = []
    for r in detalle_service_rows:
        service_lines.append(f"({r[0]}, {r[1]}, {r[2]})")
    f.write(",\n".join(service_lines))
    f.write(";\n\n")

    f.write("""-- Reactivar disparadores del sistema
ALTER TABLE booking ENABLE TRIGGER trg_auditar_booking;
ALTER TABLE detalle_room ENABLE TRIGGER trg_validar_disponibilidad_detalle;
ALTER TABLE detalle_room ENABLE TRIGGER trg_recalcular_total_room;
ALTER TABLE detalle_service ENABLE TRIGGER trg_recalcular_total_service;

-- =============================================================================
-- VERIFICACIÓN INMEDIATA DEL POBLAMIENTO
-- =============================================================================
SELECT 'guest' AS tabla, COUNT(*) AS total_registros FROM guest
UNION ALL
SELECT 'booking' AS tabla, COUNT(*) AS total_registros FROM booking
UNION ALL
SELECT 'detalle_room' AS tabla, COUNT(*) AS total_registros FROM detalle_room
UNION ALL
SELECT 'detalle_service' AS tabla, COUNT(*) AS total_registros FROM detalle_service;
""")

print("09_import_synthetic_data.sql regenerado con TRUNCATE exitosamente.")
