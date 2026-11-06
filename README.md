# Sistema de Gestión de Reservas y Hospedaje
## Hotel Don Quesada Boutique — Ocaña, Norte de Santander

* **Asignatura:** Base de Datos
* **Docente:** Byron Cuesta Quintero
* **Institución:** Universidad Francisco de Paula Santander Seccional Ocaña (UFPS)
* **Integrantes:**
  * Eliany Liseth Navarro Barbosa — 0192234
  * Agna Sharik Vega León — 0192289

---

## 📌 Descripción del Proyecto
Este repositorio contiene la implementación técnica de la base de datos relacional para el **Don Quesada Hotel Boutique**, desarrollada sobre **PostgreSQL 14+**. El sistema administra de manera estructurada e íntegra el flujo de información de huéspedes, tipos de habitaciones, reservas, auditoría histórica y servicios complementarios.

---

## 📁 Estructura del Repositorio

| Archivo | Descripción |
| :--- | :--- |
| **`00_master_database_setup.sql`** | **Script maestro:** Ejecuta en orden completo la creación de tablas, triggers, vistas, procedimientos e inserción de datos semilla. |
| **`01_schema_ddl.sql`** | Definición de las 10 tablas relacionales, claves primarias (`SERIAL`), claves foráneas (`FK`), restricciones `CHECK` e índices `INDEX`. |
| **`02_seed_dml.sql`** | Datos de prueba contextualizados en Ocaña (habitaciones, huéspedes, servicios típicos y reservas). |
| **`03_test_queries.sql`** | Consultas SQL de verificación, disponibilidad de habitaciones y reportes financieros. |
| **`04_triggers_business_rules.sql`** | Disparadores PL/pgSQL para control de solapamiento de fechas, cálculo de tarifas y sincronización de estados. |
| **`05_audit_log.sql`** | Sistema de auditoría automática (`booking_audit`) que registra inserciones, cancelaciones y modificaciones de reservas. |
| **`06_views.sql`** | Vistas de negocio optimizadas para el consumo del Frontend y Backend. |
| **`07_stored_procedures.sql`** | Procedimientos almacenados para transacciones seguras de reservas y consumos. |
| **`08_security_roles.sql`** | Configuración de roles y privilegios de usuario (`hotel_app_user`) para el despliegue seguro. |

---

## 🚀 Guía de Despliegue en PostgreSQL (pgAdmin 4)

1. Abrir **pgAdmin 4** y conectarse al servidor local o en la nube.
2. Crear una nueva base de datos llamada:
   ```sql
   CREATE DATABASE hotel_don_quesada_db;
   ```
3. Abrir el **Query Tool** sobre la base de datos `hotel_don_quesada_db`.
4. Cargar y ejecutar el archivo **`00_master_database_setup.sql`** presionando **F5**.
5. Para verificar la instalación, ejecutar:
   ```sql
   SELECT * FROM vw_reservas_completas;
   ```
