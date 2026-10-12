import mysql.connector

try:
    conn = mysql.connector.connect(host='localhost', user='root', password='yash', database='attendx_db')
    cursor = conn.cursor()
    
    # Update Admin
    cursor.execute("UPDATE users SET password_hash='e86f78a8a3caf0b60d8e74e5942aa6d86dc150cd3c03338aef25b7d2d7e3acc7' WHERE role='ADMIN'")
    # Update Faculty
    cursor.execute("UPDATE users SET password_hash='9859bcef2187144a16f11447b17129443780817a119496650b96bf354a65739e' WHERE role='FACULTY'")
    # Update Student
    cursor.execute("UPDATE users SET password_hash='b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54' WHERE role='STUDENT'")
    
    conn.commit()
    print("Hashes updated successfully")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
