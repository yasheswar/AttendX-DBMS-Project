from config.database import execute_query

def get_dashboard_metrics():
    """Get metrics for Admin Dashboard"""
    metrics = {}
    metrics['total_students'] = execute_query("SELECT COUNT(*) as c FROM students", fetch_one=True)['c']
    metrics['total_faculty'] = execute_query("SELECT COUNT(*) as c FROM faculty", fetch_one=True)['c']
    metrics['total_courses'] = execute_query("SELECT COUNT(*) as c FROM courses", fetch_one=True)['c']
    metrics['total_sessions'] = execute_query("SELECT COUNT(*) as c FROM class_sessions", fetch_one=True)['c']
    metrics['pending_leaves'] = execute_query("SELECT COUNT(*) as c FROM leave_applications WHERE application_status='PENDING'", fetch_one=True)['c']
    
    avg_att = execute_query("SELECT AVG(attendance_percentage) as a FROM vw_student_attendance_percentage", fetch_one=True)['a']
    metrics['avg_attendance'] = float(avg_att) if avg_att else 0.0
    
    shortages = execute_query("SELECT COUNT(*) as c FROM vw_attendance_shortage WHERE shortage_level IN ('SHORTAGE', 'CRITICAL_SHORTAGE')", fetch_one=True)['c']
    metrics['shortage_students'] = shortages
    
    return metrics

def get_course_attendance_summary():
    return execute_query("SELECT * FROM vw_course_attendance_summary", fetch_all=True)

def get_shortage_report():
    return execute_query("SELECT * FROM vw_attendance_shortage WHERE shortage_level IN ('SHORTAGE', 'CRITICAL_SHORTAGE') ORDER BY attendance_percentage ASC", fetch_all=True)

def get_leave_history_report():
    return execute_query("SELECT * FROM vw_leave_history ORDER BY approved_at DESC LIMIT 100", fetch_all=True)
