from config.database import execute_query, execute_transaction

def get_all_students():
    query = "SELECT * FROM students ORDER BY first_name"
    return execute_query(query, fetch_all=True)

def get_student_by_id(student_id):
    query = "SELECT * FROM students WHERE student_id = %s"
    return execute_query(query, (student_id,), fetch_one=True)

def search_students(search_term):
    term = f"%{search_term}%"
    query = """
        SELECT * FROM students 
        WHERE registration_number LIKE %s 
        OR first_name LIKE %s 
        OR last_name LIKE %s
        OR email LIKE %s
    """
    return execute_query(query, (term, term, term, term), fetch_all=True)

def get_student_attendance_summary(student_id):
    query = """
        SELECT course_code, course_name, section_name, 
               total_completed_sessions, attended_sessions, attendance_percentage
        FROM vw_student_attendance_percentage
        WHERE student_id = %s
    """
    return execute_query(query, (student_id,), fetch_all=True)

def get_student_alerts(student_id):
    query = """
        SELECT a.alert_id, c.course_name, a.alert_type, a.attendance_percentage, a.message, a.generated_at
        FROM alerts a
        JOIN course_offerings co ON a.offering_id = co.offering_id
        JOIN courses c ON co.course_id = c.course_id
        WHERE a.student_id = %s AND a.is_resolved = FALSE
        ORDER BY a.generated_at DESC
    """
    return execute_query(query, (student_id,), fetch_all=True)
