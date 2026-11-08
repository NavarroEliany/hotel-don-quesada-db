# Sistema de Gestión de Reservas y Hospedaje
## Hotel Don Quesada Boutique, Ocaña (Norte de Santander)

- **Asignatura:** Base de Datos
- **Docente:** Byron Cuesta Quintero
- **Institución:** Universidad Francisco de Paula Santander, Seccional Ocaña (UFPS)
- **Integrantes:**
  - Eliany Liseth Navarro Barbosa (0192234)
  - Agna Sharik Vega León (0192289)

---

## Descripción del proyecto

Este proyecto es un sistema para administrar las reservas y el hospedaje del Hotel Don Quesada Boutique. Guarda la información de huéspedes, habitaciones y sus tipos, reservas, servicios adicionales y empleados, y deja un registro de auditoría de los cambios que se hacen sobre las reservas.

La base de datos está en PostgreSQL y desplegada en Supabase. El back es una API hecha con Flask (Python) que se conecta a esa base y entrega los datos en JSON al front.

Los datos del hotel (27 habitaciones, tarifas, servicios y personal) fueron suministrados por el establecimiento. Los datos de huéspedes y reservas son sintéticos, generados con IA y validados antes de cargarlos (ver `datos_sinteticos/`).

---

## Tecnologías

| Capa | Tecnología |
| :--- | :--- |
| Base de datos | PostgreSQL (administrada con pgAdmin 4) |
| Despliegue de la base | Supabase |
| Back | Python con Flask |

---

## Arquitectura

```
Back  ->  API Flask (Python)  ->  PostgreSQL en Supabase
```

Los diagramas del modelo C4 (contexto y contenedores) están en `docs/diagramas/`.

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

El diagrama entidad-relación conceptual y el lógico están en `docs/diagramas/`.

---

## Estructura del repositorio

> Ajustar esta sección a los archivos que de verdad estén en el repo.

```
hotel-don-quesada/
├── README.md
├── database/
│   ├── 00_master_database_setup.sql
│   ├── 01_schema_ddl.sql
│   ├── 02_seed_dml.sql
│   ├── 03_test_queries.sql
│   ├── 04_triggers_business_rules.sql
│   ├── 05_audit_log.sql
│   ├── 06_views.sql
│   ├── 07_stored_procedures.sql
│   └── 08_security_roles.sql
├── backend/
│   ├── app.py            (completar con el nombre real)
│   ├── requirements.txt
│   └── ...
├── frontend/             (completar)
├── datos_sinteticos/
├── docs/
│   ├── documento_especificacion.pdf
│   ├── pruebas_aceptacion.md
│   └── diagramas/
├── .env.example
└── .gitignore
```

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

### 3. Back (Flask)

> Confirmar los comandos con el nombre real del archivo principal.

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # en Linux o Mac: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

La API queda disponible en `http://localhost:5000` (completar si usan otro puerto).

### 4. Front

(Completar: cómo se abre o ejecuta, y a qué dirección de la API apunta.)

---

## Endpoints de la API

> Completar con los endpoints reales del back.

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| GET | `/api/...` | (completar) |
| POST | `/api/...` | (completar) |
| PUT | `/api/...` | (completar) |
| DELETE | `/api/...` | (completar) |

---

## Datos sintéticos

Los datos de huéspedes y reservas se generaron con IA y se revisaron antes de importarlos con `COPY`. En `datos_sinteticos/` están el prompt inicial, el Excel original, el historial de correcciones y el Excel definitivo. El registro de errores encontrados y las consultas de validación están en el Anexo 1 del documento de especificación.

---

## Pruebas

Las pruebas de aceptación, con sus escenarios, resultados esperados y evidencias, están en `docs/pruebas_aceptacion.md`.

---

## Documentación

- Documento de especificación: `docs/documento_especificacion.pdf`
- Diagramas (ER conceptual, ER lógico, tablas y C4): `docs/diagramas/`
