from config.database import execute_query, execute_transaction

def check_and_generate_alerts():
    """
    Checks all student attendance against thresholds and generates alerts.
    Demonstrates business logic in application layer.
    """
    # 1. Get thresholds
    thresholds = execute_query("SELECT minimum_percentage, critical_percentage FROM attendance_thresholds ORDER BY applicable_from DESC LIMIT 1", fetch_one=True)
    if not thresholds:
        return
    
    min_pct = float(thresholds['minimum_percentage'])
    crit_pct = float(thresholds['critical_percentage'])
    
    # 2. Get current percentages
    percentages = execute_query("SELECT student_id, offering_id, attendance_percentage FROM vw_student_attendance_percentage", fetch_all=True)
    
    # 3. Generate alerts
    queries = []
    for p in percentages:
        att = float(p['attendance_percentage'])
        alert_type = None
        message = ""
        
        if att < crit_pct:
            alert_type = 'CRITICAL_SHORTAGE'
            message = f"Critical shortage detected: {att:.2f}% (Below {crit_pct}%)"
        elif att < min_pct:
            alert_type = 'SHORTAGE'
            message = f"Attendance shortage: {att:.2f}% (Below {min_pct}%)"
            
        if alert_type:
            # Check if active alert already exists for this offering/student
            check_q = "SELECT alert_id FROM alerts WHERE student_id=%s AND offering_id=%s AND is_resolved=FALSE"
            existing = execute_query(check_q, (p['student_id'], p['offering_id']), fetch_one=True)
            
            if not existing:
                q = """
                    INSERT INTO alerts (student_id, offering_id, alert_type, attendance_percentage, message)
                    VALUES (%s, %s, %s, %s, %s)
                """
                queries.append((q, (p['student_id'], p['offering_id'], alert_type, att, message)))
            else:
                # Update existing alert percentage
                q = "UPDATE alerts SET attendance_percentage=%s, message=%s, alert_type=%s WHERE alert_id=%s"
                queries.append((q, (att, message, alert_type, existing['alert_id'])))
                
    if queries:
        execute_transaction(queries)

def resolve_alert(alert_id):
    execute_query("UPDATE alerts SET is_resolved=TRUE WHERE alert_id=%s", (alert_id,), commit=True)
