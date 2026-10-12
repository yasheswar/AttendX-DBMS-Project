from config.database import execute_query, execute_transaction

def get_leave_types():
    query = "SELECT * FROM leave_types"
    return execute_query(query, fetch_all=True)

def apply_for_leave(student_id, leave_type_id, from_date, to_date, reason):
    query = """
        INSERT INTO leave_applications (student_id, leave_type_id, from_date, to_date, reason)
        VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (student_id, leave_type_id, from_date, to_date, reason), commit=True)

def get_student_leaves(student_id):
    query = """
        SELECT la.application_id, lt.leave_type_name, la.from_date, la.to_date, la.reason, la.application_status, la.submitted_at
        FROM leave_applications la
        JOIN leave_types lt ON la.leave_type_id = lt.leave_type_id
        WHERE la.student_id = %s
        ORDER BY la.submitted_at DESC
    """
    return execute_query(query, (student_id,), fetch_all=True)

def get_pending_leaves_for_faculty(faculty_id):
    # Faculty can approve leaves for students in their courses
    query = """
        SELECT DISTINCT la.application_id, s.registration_number, s.first_name, s.last_name, 
               lt.leave_type_name, la.from_date, la.to_date, la.reason, la.submitted_at
        FROM leave_applications la
        JOIN students s ON la.student_id = s.student_id
        JOIN leave_types lt ON la.leave_type_id = lt.leave_type_id
        JOIN student_section ss ON s.student_id = ss.student_id
        JOIN course_offerings co ON ss.section_id = co.section_id AND ss.academic_year = co.academic_year
        WHERE co.faculty_id = %s AND la.application_status = 'PENDING'
        ORDER BY la.submitted_at ASC
    """
    return execute_query(query, (faculty_id,), fetch_all=True)

def process_leave_application(application_id, faculty_id, status, remarks):
    """Transaction to update application status and insert approval record."""
    queries = [
        ("UPDATE leave_applications SET application_status = %s WHERE application_id = %s", (status, application_id)),
        ("INSERT INTO leave_approvals (application_id, faculty_id, approval_status, remarks) VALUES (%s, %s, %s, %s)",
         (application_id, faculty_id, status, remarks))
    ]
    return execute_transaction(queries)
