from config.database import execute_query, execute_transaction

def get_sessions_by_offering(offering_id):
    query = "SELECT * FROM class_sessions WHERE offering_id = %s ORDER BY session_date DESC, start_time DESC"
    return execute_query(query, (offering_id,), fetch_all=True)

def create_session(offering_id, session_date, start_time, end_time, topic, status='SCHEDULED'):
    query = """
        INSERT INTO class_sessions (offering_id, session_date, start_time, end_time, topic_covered, session_status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    execute_query(query, (offering_id, session_date, start_time, end_time, topic, status), commit=True)

def get_students_in_offering(offering_id):
    query = """
        SELECT s.student_id, s.registration_number, s.first_name, s.last_name
        FROM students s
        JOIN student_section ss ON s.student_id = ss.student_id
        JOIN course_offerings co ON ss.section_id = co.section_id AND ss.academic_year = co.academic_year
        WHERE co.offering_id = %s
        ORDER BY s.registration_number
    """
    return execute_query(query, (offering_id,), fetch_all=True)

def get_attendance_for_session(session_id):
    query = "SELECT student_id, attendance_status, remarks FROM attendance WHERE session_id = %s"
    records = execute_query(query, (session_id,), fetch_all=True)
    return {r['student_id']: r for r in records} if records else {}

def mark_attendance(session_id, attendance_data):
    """
    attendance_data is a list of dicts: [{'student_id': 1, 'status': 'PRESENT', 'remarks': ''}, ...]
    Demonstrates transaction management.
    """
    queries = []
    
    # First, delete existing records for this session to handle updates
    queries.append(("DELETE FROM attendance WHERE session_id = %s", (session_id,)))
    
    # Insert new records
    for data in attendance_data:
        q = """
            INSERT INTO attendance (session_id, student_id, attendance_status, remarks)
            VALUES (%s, %s, %s, %s)
        """
        params = (session_id, data['student_id'], data['status'], data.get('remarks', ''))
        queries.append((q, params))
        
    # Mark session as completed
    queries.append(("UPDATE class_sessions SET session_status = 'COMPLETED' WHERE session_id = %s", (session_id,)))
    
    return execute_transaction(queries)

def create_makeup_session(original_session_id, makeup_date, start_time, end_time, reason, faculty_id):
    # Fetch original session offering
    orig = execute_query("SELECT offering_id FROM class_sessions WHERE session_id = %s", (original_session_id,), fetch_one=True)
    if not orig:
        raise ValueError("Original session not found")
        
    queries = []
    # 1. Create new session
    q1 = """
        INSERT INTO class_sessions (offering_id, session_date, start_time, end_time, topic_covered, session_status)
        VALUES (%s, %s, %s, %s, %s, 'MAKEUP')
    """
    # Since we need the new session ID, we can't easily do it in execute_transaction without a stored proc or manual handling.
    # Let's do it sequentially safely.
    import mysql.connector
    from config.database import DatabaseConnection
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        cursor.execute(q1, (orig['offering_id'], makeup_date, start_time, end_time, "MAKEUP: " + reason))
        new_session_id = cursor.lastrowid
        
        q2 = """
            INSERT INTO makeup_sessions (original_session_id, makeup_session_id, reason, created_by)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(q2, (original_session_id, new_session_id, reason, faculty_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
