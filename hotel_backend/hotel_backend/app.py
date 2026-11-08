from flask import Flask, jsonify, request
from datetime import datetime
from database import get_db_connection
from psycopg.rows import dict_row

app = Flask(__name__)


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensaje": "Bienvenido al sistema de gestion hotelera",
        "estado": "Backend funcionando correctamente"
    })


@app.route("/api/health", methods=["GET"])
def verificar_api():
    return jsonify({
        "status": "success",
        "mensaje": "La API del hotel esta funcionando"
    })


# Consultar todas las habitaciones
@app.route("/api/habitaciones", methods=["GET"])
def listar_habitaciones():

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT
                        r.id_room,
                        r.room_number,
                        r.status,
                        rt.name AS room_type,
                        rt.capacity,
                        rt.base_price,
                        rt.description
                    FROM room r
                    INNER JOIN room_type rt
                        ON r.id_room_type = rt.id_room_type
                    ORDER BY r.room_number;
                """)

                habitaciones = cursor.fetchall()

                for habitacion in habitaciones:
                    habitacion["base_price"] = float(
                        habitacion["base_price"]
                    )

        return jsonify({
            "status": "success",
            "total": len(habitaciones),
            "habitaciones": habitaciones
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500
# Consultar todos los servicios del hotel
@app.route("/api/servicios", methods=["GET"])
def listar_servicios():

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT
                        id_service,
                        name,
                        price
                    FROM service
                    ORDER BY id_service;
                """)

                servicios = cursor.fetchall()

                for servicio in servicios:
                    servicio["price"] = float(servicio["price"])

        return jsonify({
            "status": "success",
            "total": len(servicios),
            "servicios": servicios
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500
# Consultar todos los huespedes
@app.route("/api/huespedes", methods=["GET"])
def listar_huespedes():

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT
                        g.id_guest,
                        g.first_name,
                        g.last_name,
                        g.document_number,
                        g.phone,
                        g.email,
                        c.name AS country
                    FROM guest g
                    INNER JOIN country c
                        ON g.id_country = c.id_country
                    ORDER BY g.id_guest;
                """)

                huespedes = cursor.fetchall()

        return jsonify({
            "status": "success",
            "total": len(huespedes),
            "huespedes": huespedes
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500
    # Consultar todas las reservas
@app.route("/api/reservas", methods=["GET"])
def listar_reservas():

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT
                        b.id_booking,
                        b.check_in_date,
                        b.check_out_date,
                        b.number_of_guests,
                        b.total_amount,
                        b.status,

                        g.first_name AS guest_first_name,
                        g.last_name AS guest_last_name,
                        g.document_number,

                        e.name AS employee_name,
                        e.last_name AS employee_last_name

                    FROM booking b

                    INNER JOIN guest g
                        ON b.id_guest = g.id_guest

                    INNER JOIN employee e
                        ON b.id_employee = e.id_employee

                    ORDER BY b.id_booking;
                """)

                reservas = cursor.fetchall()

                for reserva in reservas:
                    reserva["total_amount"] = float(
                        reserva["total_amount"]
                    )

                    reserva["check_in_date"] = str(
                        reserva["check_in_date"]
                    )

                    reserva["check_out_date"] = str(
                        reserva["check_out_date"]
                    )

        return jsonify({
            "status": "success",
            "total": len(reservas),
            "reservas": reservas
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500
    # Consultar habitaciones de una reserva
@app.route("/api/reservas/<int:id_booking>/habitaciones", methods=["GET"])
def habitaciones_reserva(id_booking):

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT
                        dr.id_booking,
                        dr.line_room,
                        r.id_room,
                        r.room_number,
                        rt.name AS room_type,
                        rt.capacity,
                        dr.price_per_night,
                        dr.observations

                    FROM detalle_room dr

                    INNER JOIN room r
                        ON dr.id_room = r.id_room

                    INNER JOIN room_type rt
                        ON r.id_room_type = rt.id_room_type

                    WHERE dr.id_booking = %s

                    ORDER BY dr.line_room;
                """, (id_booking,))

                habitaciones = cursor.fetchall()

                for habitacion in habitaciones:
                    habitacion["price_per_night"] = float(
                        habitacion["price_per_night"]
                    )

        return jsonify({
            "status": "success",
            "id_booking": id_booking,
            "total": len(habitaciones),
            "habitaciones": habitaciones
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500
    # Consultar servicios de una reserva
@app.route("/api/reservas/<int:id_booking>/servicios", methods=["GET"])
def servicios_reserva(id_booking):

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT
                        ds.id_booking,
                        ds.line_service,
                        s.id_service,
                        s.name AS service_name,
                        s.price

                    FROM detalle_service ds

                    INNER JOIN service s
                        ON ds.id_service = s.id_service

                    WHERE ds.id_booking = %s

                    ORDER BY ds.line_service;
                """, (id_booking,))

                servicios = cursor.fetchall()

                for servicio in servicios:
                    servicio["price"] = float(servicio["price"])

        return jsonify({
            "status": "success",
            "id_booking": id_booking,
            "total": len(servicios),
            "servicios": servicios
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500
    
# Consultar el detalle completo de una reserva
@app.route("/api/reservas/<int:id_booking>/detalle", methods=["GET"])
def detalle_completo_reserva(id_booking):

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                # 1. Informacion general de la reserva
                cursor.execute("""
                    SELECT
                        b.id_booking,
                        b.check_in_date,
                        b.check_out_date,
                        b.number_of_guests,
                        b.total_amount,
                        b.status,

                        g.id_guest,
                        g.first_name AS guest_first_name,
                        g.last_name AS guest_last_name,
                        g.document_number,
                        g.phone,
                        g.email,
                        c.name AS country,

                        e.id_employee,
                        e.name AS employee_name,
                        e.last_name AS employee_last_name,
                        e.role AS employee_role

                    FROM booking b

                    INNER JOIN guest g
                        ON b.id_guest = g.id_guest

                    INNER JOIN country c
                        ON g.id_country = c.id_country

                    INNER JOIN employee e
                        ON b.id_employee = e.id_employee

                    WHERE b.id_booking = %s;
                """, (id_booking,))

                reserva = cursor.fetchone()

                # Verificar si existe la reserva
                if reserva is None:
                    return jsonify({
                        "status": "error",
                        "mensaje": "No se encontro la reserva"
                    }), 404

                # Convertir tipos para JSON
                reserva["check_in_date"] = str(reserva["check_in_date"])
                reserva["check_out_date"] = str(reserva["check_out_date"])
                reserva["total_amount"] = float(reserva["total_amount"])

                # Organizar datos del huesped
                huesped = {
                    "id_guest": reserva.pop("id_guest"),
                    "nombre": (
                        reserva.pop("guest_first_name") + " " +
                        reserva.pop("guest_last_name")
                    ),
                    "documento": reserva.pop("document_number"),
                    "telefono": reserva.pop("phone"),
                    "email": reserva.pop("email"),
                    "pais": reserva.pop("country")
                }

                # Organizar datos del empleado
                empleado = {
                    "id_employee": reserva.pop("id_employee"),
                    "nombre": (
                        reserva.pop("employee_name") + " " +
                        reserva.pop("employee_last_name")
                    ),
                    "cargo": reserva.pop("employee_role")
                }

                # 2. Consultar habitaciones
                cursor.execute("""
                    SELECT
                        r.id_room,
                        r.room_number,
                        rt.name AS room_type,
                        rt.capacity,
                        dr.price_per_night,
                        dr.observations

                    FROM detalle_room dr

                    INNER JOIN room r
                        ON dr.id_room = r.id_room

                    INNER JOIN room_type rt
                        ON r.id_room_type = rt.id_room_type

                    WHERE dr.id_booking = %s

                    ORDER BY dr.line_room;
                """, (id_booking,))

                habitaciones = cursor.fetchall()

                for habitacion in habitaciones:
                    habitacion["price_per_night"] = float(
                        habitacion["price_per_night"]
                    )

                # 3. Consultar servicios
                cursor.execute("""
                    SELECT
                        s.id_service,
                        s.name AS service_name,
                        s.price

                    FROM detalle_service ds

                    INNER JOIN service s
                        ON ds.id_service = s.id_service

                    WHERE ds.id_booking = %s

                    ORDER BY ds.line_service;
                """, (id_booking,))

                servicios = cursor.fetchall()

                for servicio in servicios:
                    servicio["price"] = float(servicio["price"])

                # Construir respuesta final
                resultado = {
                    **reserva,
                    "huesped": huesped,
                    "empleado": empleado,
                    "habitaciones": habitaciones,
                    "servicios": servicios
                }

        return jsonify({
            "status": "success",
            "reserva": resultado
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500

# Consultar habitaciones disponibles por fechas
@app.route("/api/habitaciones/disponibles", methods=["GET"])
def habitaciones_disponibles():

    # Recibir fechas desde la URL
    fecha_entrada = request.args.get("fecha_entrada")
    fecha_salida = request.args.get("fecha_salida")

    # Validar que se hayan enviado ambas fechas
    if not fecha_entrada or not fecha_salida:
        return jsonify({
            "status": "error",
            "mensaje": "Debe indicar fecha_entrada y fecha_salida"
        }), 400

    # Validar formato y orden de las fechas
    try:
        entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d").date()
        salida = datetime.strptime(fecha_salida, "%Y-%m-%d").date()

        if salida <= entrada:
            return jsonify({
                "status": "error",
                "mensaje": "La fecha de salida debe ser posterior a la fecha de entrada"
            }), 400

    except ValueError:
        return jsonify({
            "status": "error",
            "mensaje": "Formato de fecha invalido. Utilice YYYY-MM-DD"
        }), 400

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT
                        r.id_room,
                        r.room_number,
                        r.status,
                        rt.name AS room_type,
                        rt.capacity,
                        rt.base_price,
                        rt.description

                    FROM room r

                    INNER JOIN room_type rt
                        ON r.id_room_type = rt.id_room_type

                    WHERE NOT EXISTS (

                        SELECT 1

                        FROM detalle_room dr

                        INNER JOIN booking b
                            ON dr.id_booking = b.id_booking

                        WHERE dr.id_room = r.id_room

                        AND LOWER(b.status) NOT IN (
                            'cancelada',
                            'cancelado'
                        )

                        AND b.check_in_date < %s
                        AND b.check_out_date > %s
                    )

                    ORDER BY r.room_number;
                """, (salida, entrada))

                habitaciones = cursor.fetchall()

                for habitacion in habitaciones:
                    habitacion["base_price"] = float(
                        habitacion["base_price"]
                    )

        return jsonify({
            "status": "success",
            "fecha_entrada": fecha_entrada,
            "fecha_salida": fecha_salida,
            "total": len(habitaciones),
            "habitaciones_disponibles": habitaciones
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500
# Consultar paises registrados
@app.route("/api/paises", methods=["GET"])
def listar_paises():

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT id_country, name
                    FROM country
                    ORDER BY id_country;
                """)

                paises = cursor.fetchall()

        return jsonify({
            "status": "success",
            "total": len(paises),
            "paises": paises
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500
    # Registrar un nuevo huesped
@app.route("/api/huespedes", methods=["POST"])
def registrar_huesped():

    datos = request.get_json(silent=True)

    # Verificar que se reciban datos JSON
    if not datos:
        return jsonify({
            "status": "error",
            "mensaje": "Debe enviar los datos en formato JSON"
        }), 400

    # Campos obligatorios
    campos_obligatorios = [
        "first_name",
        "last_name",
        "document_number",
        "phone",
        "id_country"
    ]

    for campo in campos_obligatorios:
        if campo not in datos or datos[campo] is None or str(datos[campo]).strip() == "":
            return jsonify({
                "status": "error",
                "mensaje": f"El campo {campo} es obligatorio"
            }), 400

    try:
        id_country = int(datos["id_country"])

        if id_country <= 0:
            raise ValueError

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "mensaje": "id_country debe ser un numero entero positivo"
        }), 400

    # Limpiar los datos recibidos
    first_name = str(datos["first_name"]).strip()
    last_name = str(datos["last_name"]).strip()
    document_number = str(datos["document_number"]).strip()
    phone = str(datos["phone"]).strip()
    email = datos.get("email")

    if email is not None:
        email = str(email).strip() or None

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                # Evitar registrar dos veces el mismo documento
                cursor.execute("""
                    SELECT id_guest
                    FROM guest
                    WHERE document_number = %s;
                """, (document_number,))

                existente = cursor.fetchone()

                if existente:
                    return jsonify({
                        "status": "error",
                        "mensaje": "Ya existe un huesped con ese documento"
                    }), 409

                # Insertar el nuevo huesped
                cursor.execute("""
                    INSERT INTO guest (
                        first_name,
                        last_name,
                        document_number,
                        phone,
                        email,
                        id_country
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id_guest;
                """, (
                    first_name,
                    last_name,
                    document_number,
                    phone,
                    email,
                    id_country
                ))

                nuevo_huesped = cursor.fetchone()

        return jsonify({
            "status": "success",
            "mensaje": "Huesped registrado correctamente",
            "id_guest": nuevo_huesped["id_guest"]
        }), 201

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500
    
# Actualizar los datos de un huesped
@app.route("/api/huespedes/<int:id_guest>", methods=["PUT"])
def actualizar_huesped(id_guest):

    datos = request.get_json(silent=True)

    if not datos:
        return jsonify({
            "status": "error",
            "mensaje": "Debe enviar los datos en formato JSON"
        }), 400

    campos_obligatorios = [
        "first_name",
        "last_name",
        "document_number",
        "phone",
        "id_country"
    ]

    for campo in campos_obligatorios:
        if campo not in datos or datos[campo] is None or str(datos[campo]).strip() == "":
            return jsonify({
                "status": "error",
                "mensaje": f"El campo {campo} es obligatorio"
            }), 400

    try:
        id_country = int(datos["id_country"])

        if id_country <= 0:
            raise ValueError

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "mensaje": "id_country debe ser un numero entero positivo"
        }), 400

    first_name = str(datos["first_name"]).strip()
    last_name = str(datos["last_name"]).strip()
    document_number = str(datos["document_number"]).strip()
    phone = str(datos["phone"]).strip()
    email = datos.get("email")

    if email is not None:
        email = str(email).strip() or None

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                # Verificar que el huesped exista
                cursor.execute("""
                    SELECT id_guest
                    FROM guest
                    WHERE id_guest = %s;
                """, (id_guest,))

                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "Huesped no encontrado"
                    }), 404

                # Verificar que el documento no pertenezca a otro huesped
                cursor.execute("""
                    SELECT id_guest
                    FROM guest
                    WHERE document_number = %s
                    AND id_guest <> %s;
                """, (document_number, id_guest))

                if cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "Ese documento ya pertenece a otro huesped"
                    }), 409

                # Actualizar los datos
                cursor.execute("""
                    UPDATE guest
                    SET first_name = %s,
                        last_name = %s,
                        document_number = %s,
                        phone = %s,
                        email = %s,
                        id_country = %s
                    WHERE id_guest = %s;
                """, (
                    first_name,
                    last_name,
                    document_number,
                    phone,
                    email,
                    id_country,
                    id_guest
                ))

        return jsonify({
            "status": "success",
            "mensaje": "Huesped actualizado correctamente",
            "id_guest": id_guest
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500

# Eliminar un huesped
@app.route("/api/huespedes/<int:id_guest>", methods=["DELETE"])
def eliminar_huesped(id_guest):

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                # Verificar que el huesped exista
                cursor.execute("""
                    SELECT id_guest
                    FROM guest
                    WHERE id_guest = %s;
                """, (id_guest,))

                huesped = cursor.fetchone()

                if not huesped:
                    return jsonify({
                        "status": "error",
                        "mensaje": "Huesped no encontrado"
                    }), 404

                # Verificar si tiene reservas asociadas
                cursor.execute("""
                    SELECT id_booking
                    FROM booking
                    WHERE id_guest = %s
                    LIMIT 1;
                """, (id_guest,))

                reserva = cursor.fetchone()

                if reserva:
                    return jsonify({
                        "status": "error",
                        "mensaje": "No se puede eliminar el huesped porque tiene reservas registradas"
                    }), 409

                # Eliminar el huesped
                cursor.execute("""
                    DELETE FROM guest
                    WHERE id_guest = %s;
                """, (id_guest,))

        return jsonify({
            "status": "success",
            "mensaje": "Huesped eliminado correctamente",
            "id_guest": id_guest
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500

# Registrar una nueva reserva
@app.route("/api/reservas", methods=["POST"])
def registrar_reserva():

    datos = request.get_json(silent=True)

    if not datos:
        return jsonify({
            "status": "error",
            "mensaje": "Debe enviar los datos en formato JSON"
        }), 400

    # Validar campos obligatorios
    campos = [
        "check_in_date",
        "check_out_date",
        "number_of_guests",
        "id_guest",
        "id_employee",
        "habitaciones"
    ]

    for campo in campos:
        if campo not in datos or datos[campo] is None:
            return jsonify({
                "status": "error",
                "mensaje": f"El campo {campo} es obligatorio"
            }), 400

    # Validar fechas
    try:
        fecha_entrada = datetime.strptime(
            datos["check_in_date"], "%Y-%m-%d"
        ).date()

        fecha_salida = datetime.strptime(
            datos["check_out_date"], "%Y-%m-%d"
        ).date()

        if fecha_salida <= fecha_entrada:
            return jsonify({
                "status": "error",
                "mensaje": "La fecha de salida debe ser posterior a la entrada"
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "mensaje": "Las fechas deben tener el formato YYYY-MM-DD"
        }), 400

    # Validar cantidades e identificadores
    try:
        numero_huespedes = int(datos["number_of_guests"])
        id_guest = int(datos["id_guest"])
        id_employee = int(datos["id_employee"])

        if numero_huespedes <= 0 or id_guest <= 0 or id_employee <= 0:
            raise ValueError

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "mensaje": "Los identificadores y el número de huéspedes deben ser positivos"
        }), 400

    # Validar habitaciones
    habitaciones = datos["habitaciones"]

    if not isinstance(habitaciones, list) or not habitaciones:
        return jsonify({
            "status": "error",
            "mensaje": "Debe enviar al menos una habitación"
        }), 400

    try:
        ids_habitaciones = [
            int(habitacion["id_room"])
            for habitacion in habitaciones
        ]

        if any(id_room <= 0 for id_room in ids_habitaciones):
            raise ValueError

        if len(ids_habitaciones) != len(set(ids_habitaciones)):
            return jsonify({
                "status": "error",
                "mensaje": "No puede incluir una habitación más de una vez"
            }), 400

    except (ValueError, TypeError, KeyError):
        return jsonify({
            "status": "error",
            "mensaje": "Verifique los identificadores de las habitaciones"
        }), 400

    # Validar servicios (son opcionales)
    servicios = datos.get("servicios", [])

    if not isinstance(servicios, list):
        return jsonify({
            "status": "error",
            "mensaje": "Los servicios deben enviarse en una lista"
        }), 400

    try:
        ids_servicios = [int(id_service) for id_service in servicios]

        if any(id_service <= 0 for id_service in ids_servicios):
            raise ValueError

        if len(ids_servicios) != len(set(ids_servicios)):
            return jsonify({
                "status": "error",
                "mensaje": "No puede incluir un servicio más de una vez"
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "mensaje": "Verifique los identificadores de los servicios"
        }), 400

    noches = (fecha_salida - fecha_entrada).days

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                # Verificar que el huésped exista
                cursor.execute("""
                    SELECT id_guest
                    FROM guest
                    WHERE id_guest = %s;
                """, (id_guest,))

                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "El huésped no existe"
                    }), 404

                # Verificar que el empleado exista
                cursor.execute("""
                    SELECT id_employee
                    FROM employee
                    WHERE id_employee = %s;
                """, (id_employee,))

                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "El empleado no existe"
                    }), 404

                # Consultar habitaciones y sus precios y capacidades
                cursor.execute("""
                    SELECT
                        r.id_room,
                        rt.capacity,
                        rt.base_price
                    FROM room r
                    INNER JOIN room_type rt
                        ON r.id_room_type = rt.id_room_type
                    WHERE r.id_room = ANY(%s);
                """, (ids_habitaciones,))

                habitaciones_db = cursor.fetchall()

                if len(habitaciones_db) != len(ids_habitaciones):
                    return jsonify({
                        "status": "error",
                        "mensaje": "Una o más habitaciones no existen"
                    }), 404

                # Verificar capacidad total
                capacidad_total = sum(
                    habitacion["capacity"]
                    for habitacion in habitaciones_db
                )

                if numero_huespedes > capacidad_total:
                    return jsonify({
                        "status": "error",
                        "mensaje": "La capacidad de las habitaciones es insuficiente"
                    }), 400

                # Verificar disponibilidad en las fechas solicitadas
                cursor.execute("""
                    SELECT dr.id_room
                    FROM detalle_room dr
                    INNER JOIN booking b
                        ON dr.id_booking = b.id_booking
                    WHERE dr.id_room = ANY(%s)
                      AND b.check_in_date < %s
                      AND b.check_out_date > %s
                      AND LOWER(b.status) NOT IN ('cancelada', 'cancelado');
                """, (
                    ids_habitaciones,
                    fecha_salida,
                    fecha_entrada
                ))

                habitaciones_ocupadas = cursor.fetchall()

                if habitaciones_ocupadas:
                    return jsonify({
                        "status": "error",
                        "mensaje": "Una o más habitaciones no están disponibles para esas fechas",
                        "habitaciones_ocupadas": [
                            habitacion["id_room"]
                            for habitacion in habitaciones_ocupadas
                        ]
                    }), 409

                # Consultar servicios y sus precios
                precios_servicios = []

                if ids_servicios:
                    cursor.execute("""
                        SELECT id_service, price
                        FROM service
                        WHERE id_service = ANY(%s);
                    """, (ids_servicios,))

                    precios_servicios = cursor.fetchall()

                    if len(precios_servicios) != len(ids_servicios):
                        return jsonify({
                            "status": "error",
                            "mensaje": "Uno o más servicios no existen"
                        }), 404

                # Calcular total de habitaciones
                total_habitaciones = sum(
                    habitacion["base_price"]
                    for habitacion in habitaciones_db
                ) * noches

                # Calcular total de servicios
                total_servicios = sum(
                    servicio["price"]
                    for servicio in precios_servicios
                )

                total_reserva = (
                    total_habitaciones + total_servicios
                )

                # Crear la reserva
                cursor.execute("""
                    INSERT INTO booking (
                        check_in_date,
                        check_out_date,
                        number_of_guests,
                        total_amount,
                        id_guest,
                        id_employee
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id_booking;
                """, (
                    fecha_entrada,
                    fecha_salida,
                    numero_huespedes,
                    total_reserva,
                    id_guest,
                    id_employee
                ))

                nueva_reserva = cursor.fetchone()
                id_booking = nueva_reserva["id_booking"]

                # Registrar habitaciones
                for linea, habitacion in enumerate(
                    habitaciones_db, start=1
                ):
                    cursor.execute("""
                        INSERT INTO detalle_room (
                            id_booking,
                            line_room,
                            id_room,
                            price_per_night
                        )
                        VALUES (%s, %s, %s, %s);
                    """, (
                        id_booking,
                        linea,
                        habitacion["id_room"],
                        habitacion["base_price"]
                    ))

                # Registrar servicios
                for linea, servicio in enumerate(
                    precios_servicios, start=1
                ):
                    cursor.execute("""
                        INSERT INTO detalle_service (
                            id_booking,
                            line_service,
                            id_service
                        )
                        VALUES (%s, %s, %s);
                    """, (
                        id_booking,
                        linea,
                        servicio["id_service"]
                    ))

        return jsonify({
            "status": "success",
            "mensaje": "Reserva registrada correctamente",
            "id_booking": id_booking,
            "noches": noches,
            "total_amount": float(total_reserva)
        }), 201

    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": str(error)
        }), 500

@app.route("/api/reservas/<int:id_booking>", methods=["PUT"])
def actualizar_reserva(id_booking):
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "mensaje": "Debe enviar los datos de la reserva"
        }), 400

    campos = [
        "check_in_date",
        "check_out_date",
        "number_of_guests",
        "id_guest",
        "id_employee"
    ]

    for campo in campos:
        if campo not in data:
            return jsonify({
                "status": "error",
                "mensaje": f"Falta el campo {campo}"
            }), 400

    try:
        fecha_entrada = datetime.strptime(
            data["check_in_date"], "%Y-%m-%d"
        ).date()

        fecha_salida = datetime.strptime(
            data["check_out_date"], "%Y-%m-%d"
        ).date()

        numero_huespedes = int(data["number_of_guests"])
        id_guest = int(data["id_guest"])
        id_employee = int(data["id_employee"])

        if fecha_salida <= fecha_entrada:
            return jsonify({
                "status": "error",
                "mensaje": "La fecha de salida debe ser posterior a la entrada"
            }), 400

        if numero_huespedes <= 0 or id_guest <= 0 or id_employee <= 0:
            return jsonify({
                "status": "error",
                "mensaje": "Los identificadores y el número de huéspedes deben ser positivos"
            }), 400

        noches = (fecha_salida - fecha_entrada).days

        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                # Verificar que la reserva exista
                cursor.execute("""
                    SELECT id_booking, status
                    FROM booking
                    WHERE id_booking = %s
                """, (id_booking,))

                reserva = cursor.fetchone()

                if not reserva:
                    return jsonify({
                        "status": "error",
                        "mensaje": "La reserva no existe"
                    }), 404

                if reserva["status"].lower() in ("cancelada", "cancelado"):
                    return jsonify({
                        "status": "error",
                        "mensaje": "No se puede modificar una reserva cancelada"
                    }), 400

                # Verificar huésped
                cursor.execute("""
                    SELECT id_guest
                    FROM guest
                    WHERE id_guest = %s
                """, (id_guest,))

                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "El huésped no existe"
                    }), 404

                # Verificar empleado
                cursor.execute("""
                    SELECT id_employee
                    FROM employee
                    WHERE id_employee = %s
                """, (id_employee,))

                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "El empleado no existe"
                    }), 404

                # Consultar habitaciones asociadas a la reserva
                cursor.execute("""
                    SELECT dr.id_room, dr.price_per_night, rt.capacity
                    FROM detalle_room dr
                    INNER JOIN room r ON dr.id_room = r.id_room
                    INNER JOIN room_type rt
                        ON r.id_room_type = rt.id_room_type
                    WHERE dr.id_booking = %s
                """, (id_booking,))

                habitaciones = cursor.fetchall()

                if not habitaciones:
                    return jsonify({
                        "status": "error",
                        "mensaje": "La reserva no tiene habitaciones asignadas"
                    }), 400

                ids_habitaciones = [
                    habitacion["id_room"]
                    for habitacion in habitaciones
                ]

                capacidad_total = sum(
                    habitacion["capacity"]
                    for habitacion in habitaciones
                )

                if numero_huespedes > capacidad_total:
                    return jsonify({
                        "status": "error",
                        "mensaje": "La capacidad de las habitaciones es insuficiente"
                    }), 400

                # Verificar disponibilidad excluyendo la reserva actual
                cursor.execute("""
                    SELECT COUNT(*) AS ocupadas
                    FROM detalle_room dr
                    INNER JOIN booking b
                        ON dr.id_booking = b.id_booking
                    WHERE dr.id_room = ANY(%s)
                    AND b.id_booking <> %s
                    AND b.check_in_date < %s
                    AND b.check_out_date > %s
                    AND LOWER(b.status) NOT IN ('cancelada', 'cancelado')
                """, (
                    ids_habitaciones,
                    id_booking,
                    fecha_salida,
                    fecha_entrada
                ))

                if cursor.fetchone()["ocupadas"] > 0:
                    return jsonify({
                        "status": "error",
                        "mensaje": "Una o más habitaciones no están disponibles para esas fechas"
                    }), 409

                # Calcular el precio de las habitaciones
                precio_habitaciones = sum(
                    habitacion["price_per_night"]
                    for habitacion in habitaciones
                )

                # Calcular el precio de los servicios
                cursor.execute("""
                    SELECT COALESCE(SUM(s.price), 0) AS total_servicios
                    FROM detalle_service ds
                    INNER JOIN service s
                        ON ds.id_service = s.id_service
                    WHERE ds.id_booking = %s
                """, (id_booking,))

                total_servicios = cursor.fetchone()["total_servicios"]

                total = (
                    precio_habitaciones * noches
                    + total_servicios
                )

                # Actualizar reserva
                cursor.execute("""
                    UPDATE booking
                    SET check_in_date = %s,
                        check_out_date = %s,
                        number_of_guests = %s,
                        total_amount = %s,
                        id_guest = %s,
                        id_employee = %s
                    WHERE id_booking = %s
                """, (
                    fecha_entrada,
                    fecha_salida,
                    numero_huespedes,
                    total,
                    id_guest,
                    id_employee,
                    id_booking
                ))

        return jsonify({
            "status": "success",
            "mensaje": "Reserva actualizada correctamente",
            "id_booking": id_booking,
            "noches": noches,
            "total_amount": float(total)
        }), 200

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "mensaje": "Verifique el formato de las fechas y los valores numéricos"
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": "Error al actualizar la reserva",
            "detalle": str(e)
        }), 500

@app.route("/api/reservas/<int:id_booking>", methods=["DELETE"])
def cancelar_reserva(id_booking):
    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT id_booking, status
                    FROM booking
                    WHERE id_booking = %s
                """, (id_booking,))

                reserva = cursor.fetchone()

                if not reserva:
                    return jsonify({
                        "status": "error",
                        "mensaje": "La reserva no existe"
                    }), 404

                if reserva["status"].lower() in ("cancelada", "cancelado"):
                    return jsonify({
                        "status": "error",
                        "mensaje": "La reserva ya está cancelada"
                    }), 400

                cursor.execute("""
                    UPDATE booking
                    SET status = 'Cancelada'
                    WHERE id_booking = %s
                """, (id_booking,))

        return jsonify({
            "status": "success",
            "mensaje": "Reserva cancelada correctamente",
            "id_booking": id_booking
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": "Error al cancelar la reserva",
            "detalle": str(e)
        }), 500

@app.route("/api/reservas/<int:id_booking>/estado", methods=["PATCH"])
def cambiar_estado_reserva(id_booking):
    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({
            "status": "error",
            "mensaje": "Debe enviar el nuevo estado"
        }), 400

    nuevo_estado = str(data["status"]).strip().capitalize()

    estados_validos = [
        "Pendiente",
        "Confirmada",
        "Cancelada",
        "Finalizada"
    ]

    if nuevo_estado not in estados_validos:
        return jsonify({
            "status": "error",
            "mensaje": "Estado no válido",
            "estados_permitidos": estados_validos
        }), 400

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT id_booking, status
                    FROM booking
                    WHERE id_booking = %s
                """, (id_booking,))

                reserva = cursor.fetchone()

                if not reserva:
                    return jsonify({
                        "status": "error",
                        "mensaje": "La reserva no existe"
                    }), 404

                if reserva["status"].lower() in ("cancelada", "cancelado"):
                    return jsonify({
                        "status": "error",
                        "mensaje": "No se puede cambiar el estado de una reserva cancelada"
                    }), 400

                cursor.execute("""
                    UPDATE booking
                    SET status = %s
                    WHERE id_booking = %s
                """, (nuevo_estado, id_booking))

        return jsonify({
            "status": "success",
            "mensaje": "Estado actualizado correctamente",
            "id_booking": id_booking,
            "nuevo_estado": nuevo_estado
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": "Error al cambiar el estado",
            "detalle": str(e)
        }), 500

@app.route("/api/tipos-habitacion", methods=["GET"])
def listar_tipos_habitacion():
    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT id_room_type, name, capacity,
                           base_price, description
                    FROM room_type
                    ORDER BY id_room_type
                """)

                tipos = cursor.fetchall()

        return jsonify({
            "status": "success",
            "total": len(tipos),
            "tipos_habitacion": tipos
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": "Error al consultar los tipos de habitación",
            "detalle": str(e)
        }), 500

@app.route("/api/habitaciones", methods=["POST"])
def registrar_habitacion():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "mensaje": "Debe enviar los datos de la habitación"
        }), 400

    room_number = str(data.get("room_number", "")).strip()
    id_room_type = data.get("id_room_type")
    status = str(data.get("status", "Disponible")).strip()

    if not room_number or id_room_type is None:
        return jsonify({
            "status": "error",
            "mensaje": "El número y el tipo de habitación son obligatorios"
        }), 400

    try:
        id_room_type = int(id_room_type)

        if id_room_type <= 0:
            raise ValueError()

        if not status:
            return jsonify({
                "status": "error",
                "mensaje": "El estado no puede estar vacío"
            }), 400

        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT id_room_type
                    FROM room_type
                    WHERE id_room_type = %s
                """, (id_room_type,))

                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "El tipo de habitación no existe"
                    }), 404

                cursor.execute("""
                    SELECT id_room
                    FROM room
                    WHERE room_number = %s
                """, (room_number,))

                if cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "El número de habitación ya existe"
                    }), 409

                cursor.execute("""
                    INSERT INTO room (room_number, status, id_room_type)
                    VALUES (%s, %s, %s)
                    RETURNING id_room
                """, (room_number, status, id_room_type))

                nueva = cursor.fetchone()

        return jsonify({
            "status": "success",
            "mensaje": "Habitación registrada correctamente",
            "id_room": nueva["id_room"]
        }), 201

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "mensaje": "El ID del tipo de habitación debe ser un número válido"
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": "Error al registrar la habitación",
            "detalle": str(e)
        }), 500

@app.route("/api/habitaciones/<int:id_room>", methods=["PUT"])
def actualizar_habitacion(id_room):
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "mensaje": "Debe enviar los datos de la habitación"
        }), 400

    room_number = str(data.get("room_number", "")).strip()
    status = str(data.get("status", "")).strip()
    id_room_type = data.get("id_room_type")

    if not room_number or not status or id_room_type is None:
        return jsonify({
            "status": "error",
            "mensaje": "Todos los campos son obligatorios"
        }), 400

    try:
        id_room_type = int(id_room_type)

        if id_room_type <= 0:
            raise ValueError()

        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT id_room
                    FROM room
                    WHERE id_room = %s
                """, (id_room,))

                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "La habitación no existe"
                    }), 404

                cursor.execute("""
                    SELECT id_room
                    FROM room
                    WHERE room_number = %s
                    AND id_room <> %s
                """, (room_number, id_room))

                if cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "Ese número de habitación ya está registrado"
                    }), 409

                cursor.execute("""
                    SELECT id_room_type
                    FROM room_type
                    WHERE id_room_type = %s
                """, (id_room_type,))

                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "El tipo de habitación no existe"
                    }), 404

                cursor.execute("""
                    UPDATE room
                    SET room_number = %s,
                        status = %s,
                        id_room_type = %s
                    WHERE id_room = %s
                """, (room_number, status, id_room_type, id_room))

        return jsonify({
            "status": "success",
            "mensaje": "Habitación actualizada correctamente",
            "id_room": id_room
        }), 200

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "mensaje": "El ID del tipo de habitación debe ser válido"
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": "Error al actualizar la habitación",
            "detalle": str(e)
        }), 500

@app.route("/api/habitaciones/<int:id_room>", methods=["DELETE"])
def eliminar_habitacion(id_room):
    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT id_room
                    FROM room
                    WHERE id_room = %s
                """, (id_room,))

                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "La habitación no existe"
                    }), 404

                cursor.execute("""
                    SELECT id_room
                    FROM detalle_room
                    WHERE id_room = %s
                    LIMIT 1
                """, (id_room,))

                if cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "No se puede eliminar la habitación porque tiene reservas asociadas"
                    }), 409

                cursor.execute("""
                    DELETE FROM room
                    WHERE id_room = %s
                """, (id_room,))

        return jsonify({
            "status": "success",
            "mensaje": "Habitación eliminada correctamente",
            "id_room": id_room
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": "Error al eliminar la habitación",
            "detalle": str(e)
        }), 500

@app.route("/api/servicios", methods=["POST"])
def registrar_servicio():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "mensaje": "Debe enviar los datos del servicio"
        }), 400

    nombre = str(data.get("name", "")).strip()

    try:
        precio = float(data.get("price"))

        if not nombre or precio < 0:
            return jsonify({
                "status": "error",
                "mensaje": "El nombre es obligatorio y el precio no puede ser negativo"
            }), 400

        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    INSERT INTO service (name, price)
                    VALUES (%s, %s)
                    RETURNING id_service
                """, (nombre, precio))

                nuevo = cursor.fetchone()

        return jsonify({
            "status": "success",
            "mensaje": "Servicio registrado correctamente",
            "id_service": nuevo["id_service"]
        }), 201

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "mensaje": "El precio debe ser un número válido"
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": "Error al registrar el servicio",
            "detalle": str(e)
        }), 500

@app.route("/api/servicios/<int:id_service>", methods=["PUT"])
def actualizar_servicio(id_service):
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "mensaje": "Debe enviar los datos del servicio"
        }), 400

    nombre = str(data.get("name", "")).strip()

    try:
        precio = float(data.get("price"))

        if not nombre or precio < 0:
            return jsonify({
                "status": "error",
                "mensaje": "El nombre es obligatorio y el precio no puede ser negativo"
            }), 400

        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT id_service
                    FROM service
                    WHERE id_service = %s
                """, (id_service,))

                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "El servicio no existe"
                    }), 404

                cursor.execute("""
                    UPDATE service
                    SET name = %s, price = %s
                    WHERE id_service = %s
                """, (nombre, precio, id_service))

        return jsonify({
            "status": "success",
            "mensaje": "Servicio actualizado correctamente",
            "id_service": id_service
        }), 200

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "mensaje": "El precio debe ser un número válido"
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": "Error al actualizar el servicio",
            "detalle": str(e)
        }), 500

@app.route("/api/servicios/<int:id_service>", methods=["DELETE"])
def eliminar_servicio(id_service):
    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT id_service
                    FROM service
                    WHERE id_service = %s
                """, (id_service,))

                if not cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "El servicio no existe"
                    }), 404

                cursor.execute("""
                    SELECT id_service
                    FROM detalle_service
                    WHERE id_service = %s
                    LIMIT 1
                """, (id_service,))

                if cursor.fetchone():
                    return jsonify({
                        "status": "error",
                        "mensaje": "No se puede eliminar el servicio porque está asociado a reservas"
                    }), 409

                cursor.execute("""
                    DELETE FROM service
                    WHERE id_service = %s
                """, (id_service,))

        return jsonify({
            "status": "success",
            "mensaje": "Servicio eliminado correctamente",
            "id_service": id_service
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": "Error al eliminar el servicio",
            "detalle": str(e)
        }), 500
@app.route("/api/empleados", methods=["GET"])
def obtener_empleados():
    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT
                        id_employee,
                        name,
                        last_name,
                        role
                    FROM employee
                    ORDER BY id_employee;
                """)

                empleados = cursor.fetchall()

        return jsonify({
            "empleados": empleados,
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({
            "mensaje": str(e),
            "status": "error"
        }), 500
@app.route("/api/empleados", methods=["POST"])
def registrar_empleado():
    datos = request.get_json()

    if not datos:
        return jsonify({
            "mensaje": "Debes enviar los datos del empleado",
            "status": "error"
        }), 400

    name = datos.get("name")
    last_name = datos.get("last_name")
    role = datos.get("role")

    if not name or not last_name or not role:
        return jsonify({
            "mensaje": "Todos los campos son obligatorios",
            "status": "error"
        }), 400

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    INSERT INTO employee (name, last_name, role)
                    VALUES (%s, %s, %s)
                    RETURNING id_employee;
                """, (name, last_name, role))

                empleado = cursor.fetchone()

        return jsonify({
            "id_employee": empleado["id_employee"],
            "mensaje": "Empleado registrado correctamente",
            "status": "success"
        }), 201

    except Exception as e:
        return jsonify({
            "mensaje": str(e),
            "status": "error"
        }), 500
@app.route("/api/empleados/<int:id_employee>", methods=["PUT"])
def actualizar_empleado(id_employee):
    datos = request.get_json()

    if not datos:
        return jsonify({
            "mensaje": "Debes enviar los datos del empleado",
            "status": "error"
        }), 400

    name = datos.get("name")
    last_name = datos.get("last_name")
    role = datos.get("role")

    if not name or not last_name or not role:
        return jsonify({
            "mensaje": "Todos los campos son obligatorios",
            "status": "error"
        }), 400

    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    UPDATE employee
                    SET name = %s,
                        last_name = %s,
                        role = %s
                    WHERE id_employee = %s
                    RETURNING id_employee;
                """, (name, last_name, role, id_employee))

                empleado = cursor.fetchone()

        if not empleado:
            return jsonify({
                "mensaje": "El empleado no existe",
                "status": "error"
            }), 404

        return jsonify({
            "id_employee": empleado["id_employee"],
            "mensaje": "Empleado actualizado correctamente",
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({
            "mensaje": str(e),
            "status": "error"
        }), 500
@app.route("/api/empleados/<int:id_employee>", methods=["DELETE"])
def eliminar_empleado(id_employee):
    try:
        with get_db_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""
                    SELECT id_employee
                    FROM employee
                    WHERE id_employee = %s;
                """, (id_employee,))

                empleado = cursor.fetchone()

                if not empleado:
                    return jsonify({
                        "mensaje": "El empleado no existe",
                        "status": "error"
                    }), 404

                cursor.execute("""
                    SELECT id_booking
                    FROM booking
                    WHERE id_employee = %s
                    LIMIT 1;
                """, (id_employee,))

                reserva = cursor.fetchone()

                if reserva:
                    return jsonify({
                        "mensaje": "No se puede eliminar el empleado porque tiene reservas asociadas",
                        "status": "error"
                    }), 409

                cursor.execute("""
                    DELETE FROM employee
                    WHERE id_employee = %s;
                """, (id_employee,))

        return jsonify({
            "mensaje": "Empleado eliminado correctamente",
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({
            "mensaje": str(e),
            "status": "error"
        }), 500
if __name__ == "__main__":
    app.run(debug=True)
