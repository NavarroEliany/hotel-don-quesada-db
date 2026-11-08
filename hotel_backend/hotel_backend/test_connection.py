from database import get_db_connection

try:
    connection = get_db_connection()

    print("¡Conexión exitosa con Supabase!")

    cursor = connection.cursor()
    cursor.execute("SELECT version();")

    version = cursor.fetchone()
    print("Versión de PostgreSQL:")
    print(version[0])

    cursor.close()
    connection.close()

except Exception as error:
    print("Error al conectar con la base de datos:")
    print(error)