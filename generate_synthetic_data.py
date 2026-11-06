import os
import random
import csv
import zipfile
import io
import xml.sax.saxutils as saxutils
from datetime import datetime, timedelta

output_dir = r"C:\Users\COMPUMAX\.gemini\antigravity\scratch\hotel_don_quesada\datos_sinteticos"
os.makedirs(output_dir, exist_ok=True)

# Helper to generate XLSX without third-party packages
def save_as_xlsx(filename, headers, rows):
    zbuf = io.BytesIO()
    with zipfile.ZipFile(zbuf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>''')
        z.writestr('_rels/.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>''')
        z.writestr('xl/_rels/workbook.xml.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>''')
        z.writestr('xl/workbook.xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets>
</workbook>''')
        
        sheet_rows = []
        all_data = [headers] + rows
        for r_idx, row in enumerate(all_data, 1):
            row_cells = []
            for c_idx, val in enumerate(row, 1):
                # Excel column letter
                if c_idx <= 26:
                    col_letter = chr(64 + c_idx)
                else:
                    col_letter = chr(64 + (c_idx - 1) // 26) + chr(64 + ((c_idx - 1) % 26) + 1)
                cell_ref = f"{col_letter}{r_idx}"
                s_val = saxutils.escape(str(val) if val is not None else '')
                row_cells.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{s_val}</t></is></c>')
            sheet_rows.append(f'<row r="{r_idx}">{"".join(row_cells)}</row>')
            
        sheet_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData>{"".join(sheet_rows)}</sheetData>
</worksheet>'''
        z.writestr('xl/worksheets/sheet1.xml', sheet_content)
        
    with open(filename, 'wb') as f:
        f.write(zbuf.getvalue())
    print(f"XLSX generado: {filename}")

def save_as_csv(filename, headers, rows):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"CSV generado: {filename}")

# Seed reproducible
random.seed(42)

# Pools of realistic Colombian names
first_names = [
    "Juan", "Carlos", "Andres", "Luis", "Jose", "Diego", "Santiago", "Mateo", "Daniel", "David",
    "Alejandro", "Sebastian", "Camilo", "Felipe", "Gabriel", "Nicolas", "Julian", "Miguel", "Javier", "Fernando",
    "Maria", "Laura", "Ana", "Sofia", "Valentina", "Camila", "Daniela", "Paula", "Andrea", "Natalia",
    "Juliana", "Mariana", "Isabella", "Catalina", "Carolina", "Diana", "Adriana", "Lucia", "Elena", "Patricia",
    "Agna", "Eliany", "Byron", "Sandra", "Paola", "Claudia", "Angela", "Monica", "Lina", "Martha"
]

last_names = [
    "Rodriguez", "Gomez", "Gonzalez", "Martinez", "Garcia", "Lopez", "Hernandez", "Sanchez", "Perez", "Ramirez",
    "Torres", "Flores", "Diaz", "Vargas", "Morales", "Castillo", "Reyes", "Gutierrez", "Alvarez", "Mendoza",
    "Navarro", "Vega", "Quintero", "Lobo", "Rincon", "Paredes", "Duarte", "Cuesta", "Chacon", "Carrascal",
    "Mora", "Pabon", "Oviedo", "Salcedo", "Bautista", "Contreras", "Maldonado", "Rojas", "Silva", "Ortiz"
]

email_domains = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.es", "ufps.edu.co"]

# -------------------------------------------------------------------------
# 1. GENERAR 1000 GUESTS
# -------------------------------------------------------------------------
print("Generando 1000 registros para guest...")
guest_headers = ["id_guest", "first_name", "last_name", "document_number", "phone", "email", "id_country"]
guest_rows = []
used_documents = set()

# Base doc number around 1090000000 (typical Norte de Santander CC range)
doc_counter = 1091200000

for i in range(1, 1001):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    doc_counter += random.randint(1, 7)
    doc = str(doc_counter)
    phone = f"3{random.choice(['00','10','11','12','13','14','15','20','21','22'])}{random.randint(1000000, 9999999)}"
    clean_fn = fn.lower().replace(" ", "")
    clean_ln = ln.lower().replace(" ", "")
    email = f"{clean_fn}.{clean_ln}{random.randint(10, 99)}@{random.choice(email_domains)}"
    # 85% Colombia (1), 7% Venezuela (2), 4% Ecuador (3), 4% USA (4)
    country_id = random.choices([1, 2, 3, 4], weights=[85, 7, 4, 4])[0]
    
    guest_rows.append([i, fn, ln, doc, phone, email, country_id])

# -------------------------------------------------------------------------
# 2. GENERAR 1000 BOOKINGS
# -------------------------------------------------------------------------
print("Generando 1000 registros para booking...")
booking_headers = ["id_booking", "check_in_date", "check_out_date", "number_of_guests", "total_amount", "status", "id_guest", "id_employee"]
booking_rows = []

start_date = datetime(2026, 1, 1)
statuses = ["Confirmada", "Finalizada", "Cancelada", "Pendiente"]
status_weights = [40, 45, 10, 5]

for i in range(1, 1001):
    # Distributed across the year 2026
    check_in = start_date + timedelta(days=random.randint(0, 340))
    nights = random.choices([1, 2, 3, 4, 5, 6, 7], weights=[20, 35, 25, 10, 5, 3, 2])[0]
    check_out = check_in + timedelta(days=nights)
    
    num_guests = random.choices([1, 2, 3, 4], weights=[40, 45, 10, 5])[0]
    st = random.choices(statuses, weights=status_weights)[0]
    
    # Guest ID references 1..1000
    guest_id = random.randint(1, 1000)
    # Employee ID references 1..3
    emp_id = random.randint(1, 3)
    
    # Approximate base total (will be finalized or synced by trigger/detalle_room)
    # Average 150000 per night
    base_rate = random.choice([95000, 140000, 190000, 220000])
    tot_amount = float(base_rate * nights)
    
    booking_rows.append([
        i,
        check_in.strftime("%Y-%m-%d"),
        check_out.strftime("%Y-%m-%d"),
        num_guests,
        f"{tot_amount:.2f}",
        st,
        guest_id,
        emp_id
    ])

# -------------------------------------------------------------------------
# 3. GENERAR 200 DETALLE_ROOM
# -------------------------------------------------------------------------
print("Generando 200 registros para detalle_room...")
detalle_room_headers = ["id_booking", "line_room", "id_room", "price_per_night", "observations"]
detalle_room_rows = []

# Room types and prices
# Room 1: 101 (Estándar, 95000)
# Room 2: 102 (Doble Confort, 140000)
# Room 3: 103 (Doble Confort, 140000)
# Room 4: 201 (Suite, 190000)
# Room 5: 202 (Suite, 190000)
# Room 6: 301 (Familiar, 220000)
room_price_map = {
    1: 95000.00,
    2: 140000.00,
    3: 140000.00,
    4: 190000.00,
    5: 190000.00,
    6: 220000.00
}

obs_list = [
    "Huésped solicita cama adicional si es posible",
    "Habitación con vista al jardín interior",
    "Check-in temprano solicitado (12:00 PM)",
    "Huésped corporativo - requiere factura",
    "Huésped VIP - atención personalizada",
    "Sin peticiones especiales",
    "Solicita habitación en piso silencioso",
    "Pareja en viaje de aniversario"
]

for i in range(1, 201):
    b_id = i # 1..200
    line = 1
    r_id = random.randint(1, 6)
    price = room_price_map[r_id]
    obs = random.choice(obs_list)
    detalle_room_rows.append([b_id, line, r_id, f"{price:.2f}", obs])

# -------------------------------------------------------------------------
# 4. GENERAR 200 DETALLE_SERVICE
# -------------------------------------------------------------------------
print("Generando 200 registros para detalle_service...")
detalle_service_headers = ["id_booking", "line_service", "id_service"]
detalle_service_rows = []

for i in range(1, 201):
    b_id = i
    line = 1
    # Services: 1: Desayuno, 2: Parqueadero, 3: Lavandería, 4: Cena Room Service, 5: Minibar
    s_id = random.choices([1, 2, 3, 4, 5], weights=[40, 25, 15, 10, 10])[0]
    detalle_service_rows.append([b_id, line, s_id])

# -------------------------------------------------------------------------
# GUARDAR ARCHIVOS DEFINITIVOS (EXCEL Y CSV)
# -------------------------------------------------------------------------
# 1. Guests
save_as_csv(os.path.join(output_dir, "guest_definitivo.csv"), guest_headers, guest_rows)
save_as_xlsx(os.path.join(output_dir, "guest_definitivo.xlsx"), guest_headers, guest_rows)

# 2. Bookings
save_as_csv(os.path.join(output_dir, "booking_definitivo.csv"), booking_headers, booking_rows)
save_as_xlsx(os.path.join(output_dir, "booking_definitivo.xlsx"), booking_headers, booking_rows)

# 3. Detalle Room
save_as_csv(os.path.join(output_dir, "detalle_room_definitivo.csv"), detalle_room_headers, detalle_room_rows)
save_as_xlsx(os.path.join(output_dir, "detalle_room_definitivo.xlsx"), detalle_room_headers, detalle_room_rows)

# 4. Detalle Service
save_as_csv(os.path.join(output_dir, "detalle_service_definitivo.csv"), detalle_service_headers, detalle_service_rows)
save_as_xlsx(os.path.join(output_dir, "detalle_service_definitivo.xlsx"), detalle_service_headers, detalle_service_rows)

# -------------------------------------------------------------------------
# GENERAR ARCHIVO "INICIAL" CON ERRORES PARA EVIDENCIA E3 Y E4
# -------------------------------------------------------------------------
print("Generando archivos iniciales (con inconsistencias pedagógicas para justificar la revisión en E4)...")
guest_initial_rows = []
for r in guest_rows[:50]: # Muestra representativa de 50 para el anexo inicial
    row_copy = list(r)
    # Introducir errores típicos de IA inicial:
    if row_copy[0] == 5:
        row_copy[3] = "1091200010" # Documento duplicado
    elif row_copy[0] == 12:
        row_copy[4] = "310-456-7890" # Formato no numérico con guiones
    elif row_copy[0] == 25:
        row_copy[5] = "correo_invalido_sin_arroba" # Formato de email incorrecto
    elif row_copy[0] == 33:
        row_copy[6] = 99 # FK que no existe en country
    guest_initial_rows.append(row_copy)

save_as_csv(os.path.join(output_dir, "guest_inicial.csv"), guest_headers, guest_initial_rows)
save_as_xlsx(os.path.join(output_dir, "guest_inicial.xlsx"), guest_headers, guest_initial_rows)

print("¡Todos los archivos Excel y CSV generados exitosamente!")
