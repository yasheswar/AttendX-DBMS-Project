-- AttendX Required Queries

USE attendx_db;

-- ==========================================
-- CATEGORY 1: BASIC RETRIEVAL
-- ==========================================

-- 1. Display all students
SELECT registration_number, first_name, last_name, department, semester FROM students;

-- 2. Display all courses
SELECT course_code, course_name, credits, department FROM courses;

-- 3. Display all faculty
SELECT faculty_code, first_name, last_name, department, designation FROM faculty;

-- 4. Display all sections
SELECT section_name, semester, academic_year, department FROM sections;

-- 5. Display course offerings
SELECT offering_id, course_id, section_id, faculty_id FROM course_offerings;


-- ==========================================
-- CATEGORY 2: JOINS
-- ==========================================

-- 1. Student attendance with student and course details
SELECT s.first_name, s.last_name, c.course_name, a.attendance_status, cs.session_date
FROM attendance a
INNER JOIN students s ON a.student_id = s.student_id
INNER JOIN class_sessions cs ON a.session_id = cs.session_id
INNER JOIN course_offerings co ON cs.offering_id = co.offering_id
INNER JOIN courses c ON co.course_id = c.course_id;

-- 2. Faculty course assignments
SELECT f.first_name, f.last_name, c.course_name, sec.section_name
FROM course_offerings co
INNER JOIN faculty f ON co.faculty_id = f.faculty_id
INNER JOIN courses c ON co.course_id = c.course_id
INNER JOIN sections sec ON co.section_id = sec.section_id;

-- 3. Student leave history
SELECT s.first_name, lt.leave_type_name, la.from_date, la.to_date, la.application_status
FROM leave_applications la
INNER JOIN students s ON la.student_id = s.student_id
INNER JOIN leave_types lt ON la.leave_type_id = lt.leave_type_id;

-- 4. Approved leave applications with faculty remarks
SELECT s.first_name, la.reason, lap.approval_status, lap.remarks, f.first_name AS approver
FROM leave_approvals lap
INNER JOIN leave_applications la ON lap.application_id = la.application_id
INNER JOIN students s ON la.student_id = s.student_id
INNER JOIN faculty f ON lap.faculty_id = f.faculty_id
WHERE lap.approval_status = 'APPROVED';

-- 5. Course-wise attendance records
SELECT c.course_name, cs.session_date, a.attendance_status, COUNT(a.student_id) AS student_count
FROM attendance a
INNER JOIN class_sessions cs ON a.session_id = cs.session_id
INNER JOIN course_offerings co ON cs.offering_id = co.offering_id
INNER JOIN courses c ON co.course_id = c.course_id
GROUP BY c.course_name, cs.session_date, a.attendance_status;

-- 6. Session-wise attendance
SELECT cs.topic_covered, cs.session_date, sec.section_name, COUNT(a.student_id) AS present_count
FROM class_sessions cs
INNER JOIN course_offerings co ON cs.offering_id = co.offering_id
INNER JOIN sections sec ON co.section_id = sec.section_id
LEFT JOIN attendance a ON cs.session_id = a.session_id AND a.attendance_status = 'PRESENT'
GROUP BY cs.session_id;

-- 7. Makeup session details
SELECT ms.reason, cs1.session_date AS original_date, cs2.session_date AS makeup_date, f.first_name AS created_by
FROM makeup_sessions ms
INNER JOIN class_sessions cs1 ON ms.original_session_id = cs1.session_id
INNER JOIN class_sessions cs2 ON ms.makeup_session_id = cs2.session_id
INNER JOIN faculty f ON ms.created_by = f.faculty_id;

-- 8. Shortage alerts with student details
SELECT s.registration_number, s.first_name, c.course_name, al.attendance_percentage, al.alert_type
FROM alerts al
INNER JOIN students s ON al.student_id = s.student_id
INNER JOIN course_offerings co ON al.offering_id = co.offering_id
INNER JOIN courses c ON co.course_id = c.course_id;

-- 9. Student section information
SELECT s.registration_number, s.first_name, sec.section_name, sec.academic_year
FROM student_section ss
INNER JOIN students s ON ss.student_id = s.student_id
INNER JOIN sections sec ON ss.section_id = sec.section_id;

-- 10. Course offering summary
SELECT c.course_code, c.course_name, sec.section_name, f.first_name AS faculty_name, co.semester
FROM course_offerings co
LEFT JOIN courses c ON co.course_id = c.course_id
LEFT JOIN sections sec ON co.section_id = sec.section_id
LEFT JOIN faculty f ON co.faculty_id = f.faculty_id;


-- ==========================================
-- CATEGORY 3: AGGREGATE FUNCTIONS
-- ==========================================

-- 1. Total absences per student
SELECT student_id, SUM(CASE WHEN attendance_status = 'ABSENT' THEN 1 ELSE 0 END) AS total_absences
FROM attendance
GROUP BY student_id
HAVING total_absences > 0;

-- 2. Course-wise attendance average (using view)
SELECT course_name, AVG(attendance_percentage) AS avg_attendance
FROM vw_student_attendance_percentage
GROUP BY course_name;

-- 3. Number of leave applications by type
SELECT lt.leave_type_name, COUNT(la.application_id) AS total_applications
FROM leave_applications la
INNER JOIN leave_types lt ON la.leave_type_id = lt.leave_type_id
GROUP BY lt.leave_type_name;

-- 4. Faculty workload (sessions taught)
SELECT f.first_name, f.last_name, COUNT(cs.session_id) AS sessions_taught
FROM faculty f
INNER JOIN course_offerings co ON f.faculty_id = co.faculty_id
INNER JOIN class_sessions cs ON co.offering_id = cs.offering_id
WHERE cs.session_status = 'COMPLETED'
GROUP BY f.faculty_id;

-- 5. Shortage student count per course
SELECT c.course_name, COUNT(v.student_id) AS shortage_students
FROM vw_attendance_shortage v
INNER JOIN courses c ON v.course_code = c.course_code
WHERE v.shortage_level IN ('SHORTAGE', 'CRITICAL_SHORTAGE')
GROUP BY c.course_name;


-- ==========================================
-- CATEGORY 4: SUBQUERIES
-- ==========================================

-- 1. Students below required attendance (using subquery on threshold)
SELECT student_name, course_name, attendance_percentage 
FROM vw_student_attendance_percentage 
WHERE attendance_percentage < (SELECT minimum_percentage FROM attendance_thresholds LIMIT 1);

-- 2. Student with lowest attendance in a specific course (e.g. CS301)
SELECT student_name, attendance_percentage
FROM vw_student_attendance_percentage
WHERE course_code = 'CS301'
  AND attendance_percentage = (
      SELECT MIN(attendance_percentage) 
      FROM vw_student_attendance_percentage 
      WHERE course_code = 'CS301'
  );

-- 3. Courses with above-average absence rate
SELECT course_code, course_name
FROM vw_course_attendance_summary
WHERE average_attendance < (SELECT AVG(average_attendance) FROM vw_course_attendance_summary);

-- 4. Faculty handling maximum sessions
SELECT first_name, last_name
FROM faculty
WHERE faculty_id = (
    SELECT co.faculty_id
    FROM class_sessions cs
    JOIN course_offerings co ON cs.offering_id = co.offering_id
    GROUP BY co.faculty_id
    ORDER BY COUNT(cs.session_id) DESC
    LIMIT 1
);

-- 5. Students who have applied for leave more than the average number of applications
SELECT s.first_name, s.last_name
FROM students s
WHERE s.student_id IN (
    SELECT student_id 
    FROM leave_applications 
    GROUP BY student_id 
    HAVING COUNT(*) > (
        SELECT AVG(app_count) 
        FROM (SELECT COUNT(*) AS app_count FROM leave_applications GROUP BY student_id) AS temp
    )
);
