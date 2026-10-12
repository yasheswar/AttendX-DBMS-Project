from config.database import execute_query

def get_all_faculty():
    query = "SELECT * FROM faculty ORDER BY first_name"
    return execute_query(query, fetch_all=True)

def get_faculty_by_id(faculty_id):
    query = "SELECT * FROM faculty WHERE faculty_id = %s"
    return execute_query(query, (faculty_id,), fetch_one=True)

def get_faculty_courses(faculty_id):
    query = """
        SELECT co.offering_id, c.course_code, c.course_name, s.section_name, co.semester, co.academic_year
        FROM course_offerings co
        JOIN courses c ON co.course_id = c.course_id
        JOIN sections s ON co.section_id = s.section_id
        WHERE co.faculty_id = %s
    """
    return execute_query(query, (faculty_id,), fetch_all=True)

def search_faculty(search_term):
    term = f"%{search_term}%"
    query = """
        SELECT * FROM faculty 
        WHERE faculty_code LIKE %s 
        OR first_name LIKE %s 
        OR last_name LIKE %s
    """
    return execute_query(query, (term, term, term), fetch_all=True)
