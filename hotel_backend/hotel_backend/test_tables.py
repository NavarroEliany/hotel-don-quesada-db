from database import get_db_connection

try:
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)

    tables = cursor.fetchall()

    print("\nTABLAS DE LA BASE DE DATOS DEL HOTEL:\n")

    for table in tables:
        print("-", table[0])

    cursor.close()
    connection.close()

except Exception as error:
    print("Error:", error)