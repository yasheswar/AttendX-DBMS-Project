import mysql.connector

password = "yash"

def run_sql_file(filename, cursor):
    print(f"Executing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Remove comments and split by semicolon
    statements = []
    current_statement = []
    for line in sql.split('\n'):
        if line.strip().startswith('--') or not line.strip():
            continue
        current_statement.append(line)
        if line.strip().endswith(';'):
            statements.append('\n'.join(current_statement))
            current_statement = []

    for statement in statements:
        if statement.strip():
            try:
                cursor.execute(statement)
            except Exception as e:
                print(f"Error executing statement:\n{statement}\nError: {e}")
                
    print(f"Successfully finished {filename}")

try:
    conn = mysql.connector.connect(host="localhost", user="root", password=password)
    cursor = conn.cursor()
    
    run_sql_file("database/database.sql", cursor)
    conn.commit()
    
    conn.database = "attendx_db"
    
    run_sql_file("database/views.sql", cursor)
    conn.commit()
    
    run_sql_file("database/sample_data.sql", cursor)
    conn.commit()
    
    print("Database setup complete!")

except Exception as e:
    print(f"Database connection failed: {e}")
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
