-- Views for AttendX

USE attendx_db;

-- VIEW 1: vw_student_attendance_percentage
CREATE OR REPLACE VIEW vw_student_attendance_percentage AS
SELECT 
    s.student_id,
    s.registration_number,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    c.course_code,
    c.course_name,
    sec.section_name,
    co.offering_id,
    COUNT(cs.session_id) AS total_completed_sessions,
    SUM(CASE WHEN a.attendance_status IN ('PRESENT', 'EXCUSED', 'LATE') THEN 1 ELSE 0 END) AS attended_sessions,
    IFNULL(
        (SUM(CASE WHEN a.attendance_status IN ('PRESENT', 'EXCUSED', 'LATE') THEN 1 ELSE 0 END) / COUNT(cs.session_id)) * 100, 
        0
    ) AS attendance_percentage
FROM students s
JOIN student_section ss ON s.student_id = ss.student_id
JOIN sections sec ON ss.section_id = sec.section_id
JOIN course_offerings co ON sec.section_id = co.section_id
JOIN courses c ON co.course_id = c.course_id
JOIN class_sessions cs ON co.offering_id = cs.offering_id AND cs.session_status = 'COMPLETED'
LEFT JOIN attendance a ON cs.session_id = a.session_id AND s.student_id = a.student_id
GROUP BY s.student_id, c.course_id, co.offering_id;


-- VIEW 2: vw_attendance_shortage
CREATE OR REPLACE VIEW vw_attendance_shortage AS
SELECT 
    v.student_id,
    v.offering_id,
    v.registration_number,
    v.student_name,
    v.course_code,
    v.course_name,
    v.attendance_percentage,
    CASE 
        WHEN v.attendance_percentage < t.critical_percentage THEN 'CRITICAL_SHORTAGE'
        WHEN v.attendance_percentage >= t.critical_percentage AND v.attendance_percentage < t.minimum_percentage THEN 'SHORTAGE'
        ELSE 'GOOD'
    END AS shortage_level
FROM vw_student_attendance_percentage v
CROSS JOIN (SELECT minimum_percentage, critical_percentage FROM attendance_thresholds ORDER BY applicable_from DESC LIMIT 1) t;


-- VIEW 3: vw_leave_history
CREATE OR REPLACE VIEW vw_leave_history AS
SELECT 
    la.application_id,
    s.student_id,
    s.registration_number,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    lt.leave_type_name,
    la.from_date,
    la.to_date,
    DATEDIFF(la.to_date, la.from_date) + 1 AS num_days,
    la.reason,
    la.application_status,
    CONCAT(f.first_name, ' ', f.last_name) AS approver_name,
    lap.remarks,
    lap.approved_at
FROM leave_applications la
JOIN students s ON la.student_id = s.student_id
JOIN leave_types lt ON la.leave_type_id = lt.leave_type_id
LEFT JOIN leave_approvals lap ON la.application_id = lap.application_id
LEFT JOIN faculty f ON lap.faculty_id = f.faculty_id;


-- VIEW 4: vw_course_attendance_summary
CREATE OR REPLACE VIEW vw_course_attendance_summary AS
SELECT 
    c.course_code,
    c.course_name,
    sec.section_name,
    CONCAT(f.first_name, ' ', f.last_name) AS faculty_name,
    COUNT(DISTINCT ss.student_id) AS total_students,
    COUNT(DISTINCT cs.session_id) AS total_sessions,
    AVG(v.attendance_percentage) AS average_attendance
FROM course_offerings co
JOIN courses c ON co.course_id = c.course_id
JOIN sections sec ON co.section_id = sec.section_id
JOIN faculty f ON co.faculty_id = f.faculty_id
LEFT JOIN student_section ss ON sec.section_id = ss.section_id
LEFT JOIN class_sessions cs ON co.offering_id = cs.offering_id AND cs.session_status = 'COMPLETED'
LEFT JOIN vw_student_attendance_percentage v ON co.offering_id = v.offering_id AND ss.student_id = v.student_id
GROUP BY co.offering_id;


-- VIEW 5: vw_monthly_attendance_trends
CREATE OR REPLACE VIEW vw_monthly_attendance_trends AS
SELECT 
    DATE_FORMAT(cs.session_date, '%Y-%m') AS month,
    c.course_code,
    c.course_name,
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    COUNT(cs.session_id) AS total_sessions,
    SUM(CASE WHEN a.attendance_status IN ('PRESENT', 'EXCUSED', 'LATE') THEN 1 ELSE 0 END) AS attended_sessions,
    IFNULL(
        (SUM(CASE WHEN a.attendance_status IN ('PRESENT', 'EXCUSED', 'LATE') THEN 1 ELSE 0 END) / COUNT(cs.session_id)) * 100, 
        0
    ) AS attendance_percentage
FROM class_sessions cs
JOIN course_offerings co ON cs.offering_id = co.offering_id
JOIN courses c ON co.course_id = c.course_id
JOIN attendance a ON cs.session_id = a.session_id
JOIN students s ON a.student_id = s.student_id
WHERE cs.session_status = 'COMPLETED'
GROUP BY month, c.course_id, s.student_id;
