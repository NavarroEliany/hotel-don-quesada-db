import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()

# Margins
for s in doc.sections:
    s.top_margin = Inches(1)
    s.bottom_margin = Inches(1)
    s.left_margin = Inches(1)
    s.right_margin = Inches(1)

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(160, 16, 32) # UFPS Crimson
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(30, 60, 100) # Deep Navy
    return p

def add_body(text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    return p

def add_code_block(code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.rows[0].cells[0]
    c.width = Inches(6.5)
    set_cell_background(c, "F5F5F7")
    set_cell_margins(c, 80, 80, 120, 120)
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(code_text)
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(40, 40, 40)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Document Header
header_p = doc.add_paragraph()
header_p.paragraph_format.space_after = Pt(12)
header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_h = header_p.add_run("CONTINUACIÓN DEL DOCUMENTO DE ESPECIFICACIÓN\nCAPÍTULOS 3 AL 8: DISEÑO, CREACIÓN, TRANSICIÓN Y PRODUCCIÓN")
r_h.font.name = "Calibri"
r_h.font.size = Pt(14)
r_h.font.bold = True
r_h.font.color.rgb = RGBColor(160, 16, 32)

add_body("Este documento contiene el desarrollo completo y riguroso de los capítulos 3 al 8 para ser integrados al documento general de especificación del Don Quesada Hotel Boutique, completando el 100% de la rúbrica del Bloque 1.")

# =============================================================================
# 3. DISEÑO
# =============================================================================
add_heading_1("3. Diseño")

add_heading_2("3.1 Especificaciones de diseño")
add_body("Las especificaciones de diseño formalizan la estructura de datos que soportará el Sistema de Gestión de Reservas y Hospedaje. A continuación, se detalla el diccionario de datos de las entidades del modelo relacional, indicando tipos físicos en PostgreSQL, restricciones de integridad y decisiones técnicas de diseño:")

# Data Dictionary Table
dict_table = doc.add_table(rows=11, cols=5)
dict_table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Tabla", "Atributos Principales", "Tipo PostgreSQL", "Restricción / Clave", "Descripción y Regla"]
for i, h in enumerate(headers):
    c = dict_table.rows[0].cells[i]
    set_cell_background(c, "A01020")
    set_cell_margins(c, 70, 70, 80, 80)
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.font.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

dict_data = [
    ("country", "id_country\nname", "SERIAL\nVARCHAR(100)", "PK\nUNIQUE NOT NULL", "Catálogo maestro de países de procedencia."),
    ("state", "id_state\nname", "SERIAL\nVARCHAR(100)", "PK\nNOT NULL", "Catálogo de departamentos / divisiones territoriales."),
    ("city", "id_city\nname\nid_state, id_country", "SERIAL\nVARCHAR(100)\nINTEGER", "PK\nNOT NULL\nFK (state, country)", "Catálogo de ciudades vinculadas a departamento y país."),
    ("employee", "id_employee\nname, last_name\nrole", "SERIAL\nVARCHAR(80)\nVARCHAR(50)", "PK\nNOT NULL\nNOT NULL", "Personal responsable de operar y registrar reservas."),
    ("guest", "id_guest\nfirst_name, last_name\ndocument_number\nphone, email\nid_country", "SERIAL\nVARCHAR(80)\nVARCHAR(30)\nVARCHAR(20), (120)\nINTEGER", "PK\nNOT NULL\nUNIQUE NOT NULL\nNOT NULL, NULL\nFK (country)", "Huéspedes registrados. Se asegura documento único (Regla 1)."),
    ("room_type", "id_room_type\nname, capacity\nbase_price\ndescription", "SERIAL\nVARCHAR(50), INT2\nNUMERIC(10,2)\nVARCHAR(300)", "PK\nNOT NULL, CHECK >0\nNOT NULL, CHECK >=0\nNULL", "Categorías de habitación (Suite, Estándar, Doble, Familiar)."),
    ("room", "id_room\nroom_number\nstatus\nid_room_type", "SERIAL\nVARCHAR(10)\nVARCHAR(20)\nINTEGER", "PK\nUNIQUE NOT NULL\nCHECK in ('Disponible'...)\nFK (room_type)", "Habitaciones físicas del hotel. Control de disponibilidad (Regla 8)."),
    ("booking", "id_booking\ncheck_in_date, out\nnumber_of_guests\ntotal_amount\nstatus\nid_guest, id_employee", "SERIAL\nDATE\nSMALLINT\nNUMERIC(12,2)\nVARCHAR(20)\nINTEGER", "PK\nNOT NULL, CHECK out>in\nCHECK > 0\nCHECK >= 0\nCHECK in ('Pendiente'...)\nFK (guest), FK (employee)", "Cabecera de la reserva. Contiene fechas, cliente, empleado y valor liquidado total."),
    ("detalle_room", "id_booking, line_room\nid_room\nprice_per_night\nobservations", "INTEGER, INTEGER\nINTEGER\nNUMERIC(10,2)\nVARCHAR(255)", "PK COMPUESTA\nFK (room)\nNOT NULL, CHECK >=0\nNULL", "Asignación de habitaciones por reserva. Permite reservas multi-habitación y tarifa histórica congelada (Regla 6 y 12)."),
    ("detalle_service", "id_booking, line_service\nid_service", "INTEGER, INTEGER\nINTEGER", "PK COMPUESTA\nFK (service)", "Detalle de servicios consumidos por reserva (Regla 19).")
]

for row_idx, data_row in enumerate(dict_data, start=1):
    bg_color = "FFFFFF" if row_idx % 2 != 0 else "F9F9F9"
    for col_idx, text in enumerate(data_row):
        c = dict_table.rows[row_idx].cells[col_idx]
        set_cell_background(c, bg_color)
        set_cell_margins(c, 50, 50, 60, 60)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8)

add_heading_2("Decisiones Técnicas de Diseño:")
add_body("1. Separación de Reserva y Habitaciones (detalle_room): Siguiendo la retroalimentación del docente, se desacopló id_room de la tabla booking. Esto permite que una misma reserva agrupe múltiples habitaciones bajo una misma cuenta familiar o corporativa.")
add_body("2. Tarifa Histórica Congelada (price_per_night): En cumplimiento de la Regla de Negocio 12 y 22, el precio acordado por noche se almacena en detalle_room. Si en el futuro el hotel incrementa las tarifas en room_type, las reservas históricas mantienen intacto su valor contractual.")
add_body("3. Alcance de Pagos (Supuesto 11): Se determinó que el registro detallado de pasarelas de pago queda fuera del alcance de esta versión, registrándose el total_amount liquidado en la cabecera de la reserva.")

add_heading_2("3.2 Transformación del modelo lógico a Diagrama de tablas")
add_body("El paso del modelo lógico al relacional físico se sustentó en las reglas formales de normalización:")
add_body("• Transformación de Relaciones Muchos a Muchos (M:N): Las relaciones entre Reservas y Habitaciones, y entre Reservas y Servicios, se transformaron en las tablas detalle_room y detalle_service, utilizando claves primarias compuestas por el identificador de la reserva y un número secuencial de línea (line_room, line_service).")
add_body("• Integridad Referencial: Se definieron claves foráneas con ON UPDATE CASCADE para mantener consistencia en cascada ante actualizaciones de códigos, y ON DELETE RESTRICT para proteger la eliminación accidental de registros con transacciones activas.")

# =============================================================================
# 4. CREACIÓN
# =============================================================================
add_heading_1("4. Creación")

add_heading_2("4.1 Modelo físico")
add_body("La base de datos fue implementada sobre el motor relacional PostgreSQL (v14+). Se aprovecharon sus ventajas en integridad transaccional ACID, soporte de procedimientos almacenados en PL/pgSQL y disparadores avanzados.")
add_body("Nota para el informe: En este apartado se inserta la captura del Diagrama ERD generado directamente desde pgAdmin 4 (clic derecho sobre hotel_don_quesada_db > Generate ERD).")

add_heading_2("4.2 Scripts DDL y DML")
add_body("La creación física se encuentra modularizada en scripts estándar SQL:")
add_body("• 00_master_database_setup.sql: Script maestro que ejecuta en orden DDL (tablas, restricciones, índices), disparadores (PL/pgSQL), vistas, procedimientos y datos iniciales.")
add_body("• Disparadores de Lógica Procedimental (Triggers):")
add_body("  - trg_validar_disponibilidad_detalle: Impide sobreventa o cruce de fechas en una misma habitación (Reglas 7 y 15).")
add_body("  - trg_recalcular_total_booking: Recalcula automáticamente el total_amount de la reserva sumando noches de habitación y servicios adicionales (Regla 21).")
add_body("  - trg_sincronizar_habitaciones_reserva: Sincroniza el estado de la habitación a 'Ocupada' o 'Disponible' según el estado de la reserva (Reglas 8 y 17).")
add_body("  - trg_auditar_booking: Registra en booking_audit cualquier modificación de fechas, estado o importes.")

add_heading_2("4.3 Modelo C4")
add_body("Para documentar la arquitectura del software se aplicó la notación C4:")

add_body("Nivel 1: Diagrama de Contexto del Sistema", "A. ")
add_body("Muestra cómo el Huésped, el Recepcionista y el Administrador interactúan con el Sistema de Gestión Hotel Don Quesada Boutique, comunicándose externamente con pasarelas de pago y servicios de mensajería/notificación por correo.")

add_body("Nivel 2: Diagrama de Contenedores", "B. ")
add_body("Detalla la separación tecnológica en 3 capas:")
add_body("1. Frontend Web (SPA en React / HTML5): Interfaz gráfica responsiva utilizada por el recepcionista y clientes.")
add_body("2. Backend API REST (Node.js/Express o Python/FastAPI): Gestiona la lógica de aplicación, validaciones y endpoints HTTP JSON.")
add_body("3. Base de Datos Relacional (PostgreSQL 14+): Almacena tablas, vistas, triggers y auditoría con comunicación por puerto 5432.")

add_heading_2("4.4 Desarrollo Web y 4.5 Repositorio GitHub")
add_body("• Desarrollo Web: La base de datos expone vistas especializadas (vw_reservas_completas, vw_estado_habitaciones) diseñadas para ser consumidas mediante endpoints REST en formato JSON.")
add_body("• Repositorio GitHub: El código fuente, scripts DDL/DML, datos sintéticos y documentación se encuentran versionados en el repositorio oficial de GitHub del proyecto.")

# =============================================================================
# 5. TRANSICIÓN
# =============================================================================
add_heading_1("5. Transición")

add_heading_2("5.1 Pruebas de aceptación")
add_body("Para dar cumplimiento al Criterio 11 de la rúbrica de evaluación, se diseñaron y ejecutaron seis (6) escenarios de prueba funcionales en PostgreSQL para validar el cumplimiento riguroso de los requisitos y reglas de negocio:")

# Test Cases Table
test_table = doc.add_table(rows=7, cols=5)
test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
t_headers = ["ID Prueba", "Escenario y Objetivo", "Datos de Entrada", "Resultado Esperado", "Resultado Obtenido"]
for i, h in enumerate(t_headers):
    c = test_table.rows[0].cells[i]
    set_cell_background(c, "1E3C64")
    set_cell_margins(c, 70, 70, 80, 80)
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.font.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

tests_data = [
    ("CP-01", "Registro exitoso de reserva y cálculo de importe (Reglas 10 y 21)", "Huésped 1, Cuarto 101 ($95.000), 3 noches de estadía.", "La BD calcula total_amount = $285.000 automáticamente.", "EXITOSA. total_amount calculado en $285.000 mediante trigger."),
    ("CP-02", "Control de solapamiento de fechas en misma habitación (Reglas 7 y 15)", "Intentar reservar cuarto 102 en fechas que se cruzan con una reserva activa.", "El motor debe rechazar la inserción lanzando un error claro de excepción.", "EXITOSA. PostgreSQL lanza EXCEPTION 12/21 bloqueando la sobreventa."),
    ("CP-03", "Validación de fechas invertidas (Regla 13)", "check_in: '2026-11-20', check_out: '2026-11-15' (salida anterior a entrada).", "Error 23514 por violación de CHECK chk_booking_dates.", "EXITOSA. El motor rechaza la operación inmediatamente."),
    ("CP-04", "Liberación automática de habitación al cancelar reserva (Regla 17)", "Ejecutar procedimiento sp_cancelar_reserva(id).", "La reserva pasa a 'Cancelada' y la habitación vuelve a 'Disponible'.", "EXITOSA. Habitación actualizada a 'Disponible' en tiempo real."),
    ("CP-05", "Unicidad de identificación de huéspedes (Regla 1)", "Insertar huésped con documento de identidad ya existente.", "Error 23505 por violación de restricción UNIQUE (uq_guest_document).", "EXITOSA. No permite documentos duplicados."),
    ("CP-06", "Auditoría de modificaciones (Regla 22)", "Modificar fechas de una reserva existente en booking.", "Registro automático en booking_audit con usuario, fecha y valores anteriores.", "EXITOSA. Fila registrada en booking_audit con action_type = 'UPDATE'.")
]

for row_idx, data_row in enumerate(tests_data, start=1):
    bg_color = "FFFFFF" if row_idx % 2 != 0 else "F9F9F9"
    for col_idx, text in enumerate(data_row):
        c = test_table.rows[row_idx].cells[col_idx]
        set_cell_background(c, bg_color)
        set_cell_margins(c, 50, 50, 60, 60)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8)

# =============================================================================
# 6. PRODUCCIÓN
# =============================================================================
add_heading_1("6. Producción")

add_heading_2("6.1 Desplegar el modelo físico en la nube (Supabase)")
add_body("En cumplimiento del Criterio 12 de la rúbrica, la base de datos se despliega en Supabase (Backend as a Service basado en PostgreSQL dedicado en la nube):")
add_body("1. Creación del Proyecto: Se aprovisionó una instancia de PostgreSQL en la región de AWS South America (São Paulo) para garantizar baja latencia.")
add_body("2. Ejecución DDL y DML: Se ejecutó el script maestro 00_master_database_setup.sql a través del SQL Editor web de Supabase, desplegando las 12 tablas, triggers, vistas y datos sintéticos.")
add_body("3. Verificación de Conectividad: Se comprobó el acceso seguro mediante la cadena de conexión SSL (puerto 5432 o 6543 con pooling de conexiones).")

add_heading_2("6.2 Colocar en funcionamiento el sistema")
add_body("El sistema queda completamente disponible para ser consumido por clientes web o herramientas de gestión hotelera mediante cadenas de conexión seguras y credenciales parametrizadas.")

# =============================================================================
# 7. CONCLUSIÓN Y 8. RECOMENDACIONES
# =============================================================================
add_heading_1("7. Conclusión")
add_body("1. El diseño implementado para el Don Quesada Hotel Boutique resuelve con precisión técnica los requerimientos del sector hotelero en Ocaña, permitiendo administrar reservas complejas (multi-habitación) y garantizando la integridad de datos a través de la Tercera Forma Normal (3FN).")
add_body("2. La incorporación de lógica procedimental dentro del motor mediante funciones PL/pgSQL y disparadores (triggers) demostró ser una solución superior para asegurar que reglas críticas (como evitar reservas dobles en la misma habitación o calcular totales) se cumplan directamente en la base de datos, independientemente de la aplicación externa que se conecte.")
add_body("3. El proceso de poblamiento con Inteligencia Artificial fortaleció las habilidades de auditoría, limpieza y validación de datos sintéticos, demostrando la importancia de las restricciones físicas en un RDBMS.")

add_heading_1("8. Recomendaciones")
add_body("1. Implementar en una versión posterior el módulo detallado de pagos y facturación electrónica (DIAN), para registrar medios de pago específicos (efectivo, datáfono, transferencias PSE) y anticipos.")
add_body("2. Integrar una interfaz web responsiva conectada mediante API REST que permita al personal de recepción consultar el tablero visual de disponibilidad de habitaciones (Room Rack) en tiempo real aprovechando la vista vw_estado_habitaciones.")
add_body("3. Establecer políticas automatizadas de copias de seguridad (Backups periódicos mediante pg_dump) tanto en el servidor local como en la nube para garantizar alta disponibilidad ante contingencias.")

# Save document
final_docx_path = r"C:\Users\COMPUMAX\.gemini\antigravity\scratch\hotel_don_quesada\Capitulos_3_al_8_Documento_Final.docx"
doc.save(final_docx_path)
print(f"Documento completo de Capítulos 3 al 8 generado exitosamente en: {final_docx_path}")
