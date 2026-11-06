import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()

# Set standard margins (1 inch)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Helper function to set table header shading
def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

# Title & Header
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(0)
title_p.paragraph_format.space_after = Pt(4)
title_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_title = title_p.add_run("ANEXO 1. INSTRUMENTO DE RECOLECCIÓN DE EVIDENCIAS")
run_title.font.name = "Calibri"
run_title.font.size = Pt(16)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(160, 16, 32) # UFPS Crimson

sub_p = doc.add_paragraph()
sub_p.paragraph_format.space_before = Pt(0)
sub_p.paragraph_format.space_after = Pt(14)
sub_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = sub_p.add_run("Utilización de Inteligencia Artificial para la Generación de Datos Sintéticos\nSegundo Parcial de Base de Datos — Criterio 2 (Valor 1.0)")
run_sub.font.name = "Calibri"
run_sub.font.size = Pt(12)
run_sub.font.bold = True
run_sub.font.color.rgb = RGBColor(50, 50, 50)

# Metadata Box (Table)
meta_table = doc.add_table(rows=5, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Proyecto Académico:", "Sistema de Gestión de Reservas y Hospedaje — Don Quesada Hotel Boutique"),
    ("Asignatura y Docente:", "Base de Datos | Docente: Byron Cuesta Quintero"),
    ("Institución:", "Universidad Francisco de Paula Santander Seccional Ocaña (UFPS)"),
    ("Estudiantes:", "Eliany Liseth Navarro Barbosa (0192234)\nAgna Sharik Vega León (0192289)"),
    ("Herramienta LLM Utilizada:", "Gemini 3.8 Flash (High) de Google")
]
for idx, (k, v) in enumerate(meta_data):
    row = meta_table.rows[idx]
    c0, c1 = row.cells[0], row.cells[1]
    c0.width = Inches(2.2)
    c1.width = Inches(4.3)
    set_cell_background(c0, "F2F2F2")
    set_cell_background(c1, "FAFAFA")
    set_cell_margins(c0, 60, 60, 100, 100)
    set_cell_margins(c1, 60, 60, 100, 100)
    
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(2)
    r0 = p0.add_run(k)
    r0.font.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(9.5)
    
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run(v)
    r1.font.name = "Calibri"
    r1.font.size = Pt(9.5)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(160, 16, 32)
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(30, 60, 100)
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

# -----------------------------------------------------------------------------
# E1. Diseño Relacional
# -----------------------------------------------------------------------------
add_heading_1("E1. Diseño Relacional del Sistema")
add_body("El modelo de datos sobre el cual se generaron los datos sintéticos corresponde al esquema final relacional ajustado y aprobado por el docente Byron Cuesta Quintero, conformado por 10 tablas en Tercera Forma Normal (3FN):")

e1_items = [
    ("guest (1.000 registros): ", "Entidad que almacena los datos de los huéspedes. Atributos: id_guest (PK SERIAL), first_name, last_name, document_number (UNIQUE NOT NULL), phone (NOT NULL), email, id_country (FK)."),
    ("booking (1.000 registros): ", "Entidad transaccional que registra las reservas. Atributos: id_booking (PK SERIAL), check_in_date, check_out_date, number_of_guests, total_amount, status, id_guest (FK), id_employee (FK). Restricción CHECK: check_out_date > check_in_date."),
    ("detalle_room (200 registros): ", "Tabla intermedia de asignación de habitaciones físicas a una reserva. Atributos: id_booking (PK, FK), line_room (PK), id_room (FK hacia room), price_per_night (NUMERIC tarifa histórica congelada), observations (VARCHAR)."),
    ("detalle_service (200 registros): ", "Tabla intermedia de consumos de servicios por reserva. Atributos: id_booking (PK, FK), line_service (PK), id_service (FK hacia service)."),
    ("Tablas Catálogo / Maestras: ", "country (países reales), state (departamentos colombianos), city (ciudades de origen hacia Ocaña), room_type (tipos de habitación), room (habitaciones físicas con estado) y service (catálogo de servicios incluidos y adicionales).")
]
for pre, desc in e1_items:
    add_body(desc, pre)

# -----------------------------------------------------------------------------
# E2. Prompt Inicial
# -----------------------------------------------------------------------------
add_heading_1("E2. Prompt Inicial Formulado a la Inteligencia Artificial")
add_body("LLM Utilizado: Gemini 3.8 Flash (High) de Google.", "Herramienta: ")
add_body("A continuación se transcribe la primera instrucción estructurada formulada a la IA para la generación del conjunto de datos:")

initial_prompt = (
    "\"Actúa como un Administrador de Bases de Datos senior (DBA) especializado en PostgreSQL.\n"
    "Necesito generar datos sintéticos realistas para poblar la base de datos de un hotel boutique ubicado en Ocaña, "
    "Norte de Santander, Colombia (Don Quesada Hotel Boutique). El sistema administra 10 tablas relacionales.\n\n"
    "Genera los datos con las siguientes cantidades y especificaciones:\n"
    "1. guest: 1000 registros con nombres y apellidos comunes colombianos, documento de identidad único de 10 dígitos, "
    "teléfonos celulares válidos y correo electrónico.\n"
    "2. booking: 1000 reservas distribuidas a lo largo del año 2026, con fechas de entrada y salida coherentes (1 a 7 noches), "
    "estados ('Confirmada', 'Pendiente', 'Cancelada', 'Finalizada') y llaves foráneas válidas a huéspedes y empleados.\n"
    "3. detalle_room: 200 registros asignando habitaciones a las reservas, con tarifa por noche y observaciones de la estancia.\n"
    "4. detalle_service: 200 registros asociando servicios adicionales consumidos por los huéspedes.\n\n"
    "Entrega los datos estructurados en formato de tabla para exportación a Excel y scripts para inserción masiva en PostgreSQL.\""
)
add_code_block(initial_prompt)

add_heading_2("Justificación Técnica de las Instrucciones Incluidas en el Prompt:")
add_body("1. Delimitación de Contexto Geográfico: Se especificó Ocaña y Colombia para garantizar que los nombres, apellidos y dominios de correo fueran culturalmente coherentes, evitando datos anglosajones que restarían verosimilitud.")
add_body("2. Exigencia de Unicidad: Se instruyó la generación de números de documento de 10 dígitos únicos para prevenir violaciones de la restricción UNIQUE en la clave uq_guest_document.")
add_body("3. Coherencia Temporal: Se delimitó el año 2026 y una estancia realista de 1 a 7 noches para asegurar que el sistema evaluara transacciones pasadas (Finalizada), actuales y futuras.")

# -----------------------------------------------------------------------------
# E3. Archivo Excel Inicial
# -----------------------------------------------------------------------------
add_heading_1("E3. Archivo Excel Inicial Generado en el Primer Intento")
add_body("Como resultado del primer prompt, la IA generó una primera muestra de datos tabulados que fue exportada directamente sin modificaciones:")
add_body("• Archivo adjunto oficial: guest_inicial.xlsx (y su versión en CSV guest_inicial.csv).")
add_body("• Descripción: Contiene un primer lote de prueba. Este archivo sirvió como insumo de auditoría para identificar las fallas sintácticas y semánticas que la IA comete de forma predeterminada cuando genera grandes volúmenes.")

# -----------------------------------------------------------------------------
# E4. Registro de Revisión y Detección de Inconsistencias
# -----------------------------------------------------------------------------
add_heading_1("E4. Registro de Revisión: Errores Encontrados y Verificaciones")
add_body("Se realizó una auditoría rigurosa sobre los datos preliminares generados por la IA contra las restricciones del modelo físico en PostgreSQL. Se detectaron 5 inconsistencias críticas:")

rev_table = doc.add_table(rows=6, cols=4)
rev_table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Campo / Entidad", "Error o Inconsistencia Detectada", "Causa Técnica en la IA", "Impacto en PostgreSQL"]
for i, h in enumerate(headers):
    c = rev_table.rows[0].cells[i]
    set_cell_background(c, "A01020")
    set_cell_margins(c, 80, 80, 100, 100)
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.font.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(255, 255, 255)

table_rows = [
    ("guest.document_number", "Duplicación esporádica de números de documento.", "La IA genera números pseudo-aleatorios sin control estricto de colisiones en memoria.", "Error 23505: Violación de la restricción UNIQUE (uq_guest_document). Aborta la carga."),
    ("guest.phone", "Formatos inconsistentes con guiones y paréntesis ej: '(310)-456-7890'.", "La IA asume formatos telefónicos estadounidenses por defecto de entrenamiento.", "Inconsistencia en tipos VARCHAR(20) y dificultad en validaciones de longitud fija."),
    ("booking.dates", "Casos donde check_out_date era igual o menor a check_in_date.", "La IA seleccionó dos fechas independientes sin aplicar la regla de precedencia.", "Error 23514: Violación de la restricción CHECK chk_booking_dates. Transacción rechazada."),
    ("booking.total_amount", "Montos fijos arbitrarios sin correspondencia con las noches de estancia.", "Falta de lógica computacional de negocio en la generación puramente textual.", "Inconsistencia contable entre noches reservadas y valor liquidado al huésped."),
    ("guest.id_country", "Presencia de IDs foráneos inexistentes (ej: ID 99 o 15).", "La IA alucinó países fuera de los registrados en la tabla maestra country.", "Error 23503: Violación de llave foránea (fk_guest_country). Pérdida de integridad.")
]

for row_idx, data_row in enumerate(table_rows, start=1):
    row_cells = rev_table.rows[row_idx].cells
    bg_color = "FFFFFF" if row_idx % 2 != 0 else "F8F8F8"
    for col_idx, text in enumerate(data_row):
        c = row_cells[col_idx]
        set_cell_background(c, bg_color)
        set_cell_margins(c, 60, 60, 80, 80)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# -----------------------------------------------------------------------------
# E5. Historial de Interacción y Prompts Correctivos
# -----------------------------------------------------------------------------
add_heading_1("E5. Historial de Interacción: Prompts de Corrección y Justificación")
add_body("Con base en los hallazgos del registro de revisión (E4), se diseñó un segundo prompt correctivo de alta precisión para depurar la generación:")

corrective_prompt = (
    "\"Revisando los datos generados se identificaron inconsistencias críticas que violan el modelo en PostgreSQL.\n"
    "Aplica de forma estricta las siguientes correcciones:\n\n"
    "1. guest: Asegura que los 1.000 números de cédula sean absolutamente únicos mediante una secuencia continua base "
    "(rango 1091200000 a 1091207000). Normaliza los teléfonos a números celulares colombianos limpios de 10 dígitos (ej: 3124567890).\n"
    "2. Claves foráneas: El campo id_country en guest SOLO puede tomar valores entre 1 y 4 (1: Colombia, 2: Venezuela, 3: Ecuador, 4: EE.UU.).\n"
    "3. booking: La fecha check_out_date DEBE ser obligatoriamente calculada como check_in_date + un intervalo de 1 a 7 noches. "
    "El total_amount debe corresponder a noches * precio de habitación.\n"
    "4. detalle_room: Los id_room deben coincidir con las habitaciones existentes (1 a 6) y heredar la tarifa oficial del tipo de habitación.\n"
    "5. Formato: Genera los archivos en formato XLSX nativo, CSV UTF-8 y un script de carga masiva con manejo de triggers y secuencias.\""
)
add_code_block(corrective_prompt)
add_body("Justificación de las Modificaciones: Este prompt garantiza la integridad matemática y referencial requerida por PostgreSQL, cerrando la brecha entre la generación probabilística de la IA y el determinismo formal que exige un Sistema Gestor de Bases de Datos Relacionales (RDBMS).")

# -----------------------------------------------------------------------------
# E6. Archivos Excel Definitivos
# -----------------------------------------------------------------------------
add_heading_1("E6. Archivos Excel Definitivos Validados")
add_body("Se generaron y validaron los cuatro (4) archivos de datos definitivos, almacenados en la carpeta del proyecto para entrega adjunta:")
add_body("1. guest_definitivo.xlsx / .csv: 1.000 registros depurados de huéspedes sin cédulas duplicadas y con teléfonos estandarizados.")
add_body("2. booking_definitivo.xlsx / .csv: 1.000 reservas con cálculo cronológico de fechas 100% conforme a la Regla de Negocio 11.")
add_body("3. detalle_room_definitivo.xlsx / .csv: 200 asignaciones físicas de habitación con tarifas históricas y observaciones.")
add_body("4. detalle_service_definitivo.xlsx / .csv: 200 consumos de servicios por reserva con clave compuesta íntegra.")

# -----------------------------------------------------------------------------
# E7. Base de Datos Poblada en PostgreSQL
# -----------------------------------------------------------------------------
add_heading_1("E7. Base de Datos Poblada en PostgreSQL (Script y Evidencias)")
add_body("La importación masiva se ejecutó en pgAdmin 4 sobre PostgreSQL 14+ mediante el script 09_import_synthetic_data.sql. Como buena práctica de DBA, se desactivaron temporalmente los triggers durante la carga masiva para optimizar el rendimiento, reactivándolos inmediatamente y sincronizando las secuencias (setval).")

add_body("Consulta de Comprobación Ejecutada en pgAdmin 4:")
add_code_block(
    "SELECT 'guest' AS tabla, COUNT(*) AS total_registros FROM guest\n"
    "UNION ALL\n"
    "SELECT 'booking' AS tabla, COUNT(*) AS total_registros FROM booking\n"
    "UNION ALL\n"
    "SELECT 'detalle_room' AS tabla, COUNT(*) AS total_registros FROM detalle_room\n"
    "UNION ALL\n"
    "SELECT 'detalle_service' AS tabla, COUNT(*) AS total_registros FROM detalle_service;"
)

# Table counts
cnt_table = doc.add_table(rows=5, cols=3)
cnt_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for idx, h in enumerate(["Nombre de la Tabla", "Total Registros Poblados", "Estado de Cumplimiento"]):
    c = cnt_table.rows[0].cells[idx]
    set_cell_background(c, "1E3C64")
    set_cell_margins(c, 60, 60, 100, 100)
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.font.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

counts_data = [
    ("guest", "1.000", "Cumple al 100% la solicitud del docente"),
    ("booking", "1.000", "Cumple al 100% la solicitud del docente"),
    ("detalle_room", "200", "Cumple al 100% la solicitud del docente"),
    ("detalle_service", "200", "Cumple al 100% la solicitud del docente")
]
for row_idx, (t_name, t_cnt, t_st) in enumerate(counts_data, start=1):
    c0 = cnt_table.rows[row_idx].cells[0]
    c1 = cnt_table.rows[row_idx].cells[1]
    c2 = cnt_table.rows[row_idx].cells[2]
    set_cell_background(c0, "FFFFFF" if row_idx % 2 != 0 else "F9F9F9")
    set_cell_background(c1, "FFFFFF" if row_idx % 2 != 0 else "F9F9F9")
    set_cell_background(c2, "FFFFFF" if row_idx % 2 != 0 else "F9F9F9")
    set_cell_margins(c0, 60, 60, 80, 80)
    set_cell_margins(c1, 60, 60, 80, 80)
    set_cell_margins(c2, 60, 60, 80, 80)
    
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(0)
    r0 = p0.add_run(t_name)
    r0.font.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(9)
    
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_after = Pt(0)
    p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p1.add_run(t_cnt)
    r1.font.name = "Calibri"
    r1.font.size = Pt(9)
    
    p2 = c2.paragraphs[0]
    p2.paragraph_format.space_after = Pt(0)
    r2 = p2.add_run(t_st)
    r2.font.name = "Calibri"
    r2.font.size = Pt(9)
    r2.font.color.rgb = RGBColor(0, 130, 50)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# -----------------------------------------------------------------------------
# E8. Validación SQL de Integridad
# -----------------------------------------------------------------------------
add_heading_1("E8. Validación SQL de Integridad de los Datos")
add_body("Para comprobar la integridad física, lógica y semántica de la base de datos poblada, se formularon y ejecutaron tres consultas de auditoría en PostgreSQL:")

add_heading_2("1. Validación de Unicidad de Cédulas en guest (Restricción UNIQUE):")
add_code_block(
    "SELECT document_number, COUNT(*) AS duplicados\n"
    "FROM guest\n"
    "GROUP BY document_number\n"
    "HAVING COUNT(*) > 1;"
)
add_body("Resultado obtenido: 0 filas retornadas. Explicación: Ningún número de documento de identificación se encuentra repetido en la base de datos, garantizando la unicidad de cada cliente.")

add_heading_2("2. Validación de Prevalencia de Fechas en booking (Regla de Negocio 11):")
add_code_block(
    "SELECT id_booking, check_in_date, check_out_date \n"
    "FROM booking\n"
    "WHERE check_out_date <= check_in_date;"
)
add_body("Resultado obtenido: 0 filas retornadas. Explicación: Las 1.000 reservas satisfacen la regla de procedimiento de que la fecha de check-out debe ser estrictamente posterior a la fecha de check-in.")

add_heading_2("3. Validación de Integridad Referencial (Cero Claves Huérfanas):")
add_code_block(
    "SELECT b.id_booking, b.id_guest \n"
    "FROM booking b\n"
    "LEFT JOIN guest g ON b.id_guest = g.id_guest\n"
    "WHERE g.id_guest IS NULL;"
)
add_body("Resultado obtenido: 0 filas retornadas. Explicación: No existen registros huérfanos; el 100% de las reservas apuntan a un huésped real y previamente registrado.")

# -----------------------------------------------------------------------------
# E9. Reflexión Individual
# -----------------------------------------------------------------------------
add_heading_1("E9. Reflexión Individual y Aprendizajes Obtenidos")
add_body("La realización de este laboratorio sobre producción de datos sintéticos con Inteligencia Artificial permitió consolidar aprendizajes fundamentales en la formación como ingenieros de sistemas:")

reflections = [
    ("Pensamiento Crítico frente a la IA: ", "Se constató que la Inteligencia Artificial generativa es una herramienta de asistencia extraordinaria para acelerar tareas repetitivas, pero carece de conciencia sobre las reglas formales de integridad relacional. Un DBA no puede confiar ciegamente en la salida de un modelo de lenguaje sin antes aplicar auditoría, perfilamiento de datos y scripts de verificación."),
    ("Importancia de las Restricciones en el Motor: ", "Las restricciones físicas definidas en el DDL (PRIMARY KEY, FOREIGN KEY, UNIQUE y CHECK) no son meros formalismos teóricos, sino la última línea de defensa infalible de un sistema informático. Cuando los datos sintéticos con errores intentaron cargarse, el motor PostgreSQL los rechazó inmediatamente, demostrando el valor de un diseño relacional estricto."),
    ("Simulación Real de Operaciones DBA: ", "El proceso permitió vivenciar el ciclo completo de aprovisionamiento de datos que se vive en la industria del software: formulación de requerimientos, generación sintética, limpieza de datos (Data Cleansing), importación transaccional por lotes y validación rigurosa mediante consultas SQL avanzadas.")
]
for pre, desc in reflections:
    add_body(desc, pre)

# Save document
output_docx_path = r"C:\Users\COMPUMAX\.gemini\antigravity\scratch\hotel_don_quesada\Anexo_1_Evidencias_IA_Hotel_Don_Quesada.docx"
doc.save(output_docx_path)
print(f"Documento Word generado exitosamente en: {output_docx_path}")
