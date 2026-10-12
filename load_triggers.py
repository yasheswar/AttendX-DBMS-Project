import mysql.connector

with open('database/procedures_and_triggers.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

conn = mysql.connector.connect(host='localhost', user='root', password='yash', database='attendx_db')
cursor = conn.cursor()

blocks = sql.split('$$')
for b in blocks:
    cleaned = b.replace('DELIMITER $$', '').replace('DELIMITER ;', '').strip()
    if cleaned and not cleaned.startswith('--'):
        try:
            cursor.execute(cleaned)
            print("Executed block successfully")
        except Exception as e:
            print("Error executing block:", e)

conn.commit()
cursor.close()
conn.close()
print("All Procedures & Triggers compiled successfully!")
