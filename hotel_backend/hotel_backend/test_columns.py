from database import get_db_connection

try:
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            table_name,
            column_name,
            data_type,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)

    columns = cursor.fetchall()

    current_table = ""

    for column in columns:
        table, name, data_type, nullable, default = column

        if table != current_table:
            current_table = table
            print(f"\n--- TABLA: {table} ---")

        print(
            f"Columna: {name} | "
            f"Tipo: {data_type} | "
            f"Permite NULL: {nullable} | "
            f"Default: {default}"
        )

    cursor.close()
    connection.close()

except Exception as error:
    print("Error:", error)