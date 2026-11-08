# Sistema de Gestión de Reservas y Hospedaje
## Hotel Don Quesada Boutique, Ocaña (Norte de Santander)

- **Asignatura:** Base de Datos
- **Docente:** Byron Cuesta Quintero
- **Institución:** Universidad Francisco de Paula Santander, Seccional Ocaña (UFPSO)
- **Integrantes:**
  - Eliany Liseth Navarro Barbosa (0192234)
  - Agna Sharik Vega León (0192289)

---

## Descripción del proyecto

Este proyecto es un sistema para administrar las reservas y el hospedaje del Hotel Don Quesada Boutique. Guarda la información de huéspedes, habitaciones y sus tipos, reservas, servicios adicionales y empleados, y deja un registro de auditoría de los cambios que se hacen sobre las reservas.

La base de datos está en PostgreSQL y desplegada en Supabase. El back es una API hecha con Flask (Python) que se conecta a esa base.

Los datos del hotel (27 habitaciones, tarifas, servicios y personal) fueron suministrados por el establecimiento. Los datos de huéspedes y reservas son sintéticos, generados con IA y validados antes de cargarlos

---

## Tecnologías

| Capa | Tecnología |
| :--- | :--- |
| Base de datos | PostgreSQL (administrada con pgAdmin 4) |
| Despliegue de la base | Supabase |
| Back | Python con Flask |

---


---

## Modelo de datos

La base tiene 12 tablas:

| Tabla | Qué guarda |
| :--- | :--- |
| `guest` | Huéspedes (nombre, documento, teléfono, correo, país) |
| `booking` | Reservas (fechas, número de huéspedes, total, estado, huésped y empleado) |
| `detalle_room` | Habitaciones incluidas en cada reserva y la tarifa por noche cobrada |
| `detalle_service` | Servicios adicionales consumidos en cada reserva |
| `room` | Habitaciones del hotel (número y estado) |
| `room_type` | Tipos de habitación (capacidad, precio base, descripción) |
| `service` | Servicios que ofrece el hotel y su precio |
| `employee` | Empleados del hotel y su cargo |
| `city`, `state`, `country` | Ubicación geográfica de los huéspedes |
| `booking_audit` | Historial de cambios de las reservas |


---



### Scripts de la base de datos

| Archivo | Descripción |
| :--- | :--- |
| `00_master_database_setup.sql` | Script maestro: ejecuta en orden la creación de tablas, triggers, vistas, procedimientos y los datos iniciales. |
| `01_schema_ddl.sql` | Tablas, claves primarias, claves foráneas, restricciones `CHECK` e índices. |
| `02_seed_dml.sql` | Datos iniciales del hotel (habitaciones, tipos, servicios, empleados) y datos de prueba de huéspedes y reservas. |
| `03_test_queries.sql` | Consultas de verificación, disponibilidad de habitaciones y reportes. |
| `04_triggers_business_rules.sql` | Triggers en PL/pgSQL para evitar cruces de fechas, calcular tarifas y mantener los estados. |
| `05_audit_log.sql` | Auditoría automática de las reservas en `booking_audit`. |
| `06_views.sql` | Vistas para que el back consulte la información ya armada. |
| `07_stored_procedures.sql` | Procedimientos almacenados para reservas y consumos. |
| `08_security_roles.sql` | Roles y privilegios del usuario de la aplicación (`hotel_app_user`). |

---

## Instalación y ejecución

### 1. Base de datos en Supabase

1. Crear un proyecto en [supabase.com](https://supabase.com) y guardar la contraseña de la base de datos.
2. En el **SQL Editor** de Supabase, abrir y ejecutar `database/00_master_database_setup.sql`.
3. Verificar que las tablas aparezcan en **Table Editor** y probar:
   ```sql
   SELECT * FROM vw_reservas_completas;
   ```

Si se prefiere una instalación local, crear la base en pgAdmin 4 con `CREATE DATABASE hotel_don_quesada_db;` y ejecutar el mismo script maestro desde el Query Tool.

### 2. Variables de entorno

Copiar `.env.example` a `.env` y llenar los datos de conexión de Supabase (se encuentran en el botón **Connect** del proyecto, usando Session pooler):

```
DB_HOST=
DB_PORT=5432
DB_NAME=postgres
DB_USER=
DB_PASSWORD=
```

El archivo `.env` no se sube al repositorio.

# Backend – Sistema de Gestión Hotelera

API REST en Flask conectada a una base de datos PostgreSQL desplegada en Supabase.
Proyecto del segundo parcial de Bases de Datos.

## Requisitos
- Python 3.10+
- Una base de datos PostgreSQL (Supabase) con el modelo del proyecto ya creado y poblado

## Instalación
```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # y completa las credenciales
python app.py
```
La API queda en `http://127.0.0.1:5000`. Prueba con `GET /api/health`.

## Estructura
```
app.py         Rutas de la API
database.py    Conexión a PostgreSQL (psycopg)
.env.example   Variables de entorno necesarias
```

## Endpoints

| Recurso | Métodos |
|---|---|
| `/api/habitaciones` | GET, POST |
| `/api/habitaciones/<id>` | PUT, DELETE |
| `/api/habitaciones/disponibles` | GET |
| `/api/tipos-habitacion` | GET |
| `/api/huespedes` | GET, POST |
| `/api/huespedes/<id>` | PUT, DELETE |
| `/api/paises` | GET |
| `/api/reservas` | GET, POST |
| `/api/reservas/<id>` | PUT, DELETE |
| `/api/reservas/<id>/estado` | PATCH |
| `/api/reservas/<id>/habitaciones` | GET |
| `/api/reservas/<id>/servicios` | GET |
| `/api/reservas/<id>/detalle` | GET |
| `/api/servicios` | GET, POST |
| `/api/servicios/<id>` | PUT, DELETE |
| `/api/empleados` | GET, POST |
| `/api/empleados/<id>` | PUT, DELETE |

## Datos sintéticos

Los datos de huéspedes y reservas se generaron con IA y se revisaron antes de importarlos con `COPY`. En `datos_sinteticos/` están el prompt inicial, el Excel original, el historial de correcciones y el Excel definitivo. El registro de errores encontrados y las consultas de validación están en el Anexo 1 del documento de especificación.

---
