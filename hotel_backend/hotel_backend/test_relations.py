from database import get_db_connection

try:
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            tc.table_name,
            tc.constraint_type,
            kcu.column_name,
            ccu.table_name AS foreign_table,
            ccu.column_name AS foreign_column
        FROM information_schema.table_constraints tc

        LEFT JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema

        LEFT JOIN information_schema.constraint_column_usage ccu
            ON tc.constraint_name = ccu.constraint_name
            AND tc.table_schema = ccu.table_schema

        WHERE tc.table_schema = 'public'
        AND tc.constraint_type IN ('PRIMARY KEY', 'FOREIGN KEY')

        ORDER BY tc.table_name, tc.constraint_type;
    """)

    relations = cursor.fetchall()

    print("\nRELACIONES DE LA BASE DE DATOS:\n")

    for relation in relations:
        table, constraint, column, foreign_table, foreign_column = relation

        if constraint == "PRIMARY KEY":
            print(f"{table}: PK -> {column}")
        else:
            print(
                f"{table}: FK -> {column} "
                f"referencia a {foreign_table}.{foreign_column}"
            )

    cursor.close()
    connection.close()

except Exception as error:
    print("Error:", error)