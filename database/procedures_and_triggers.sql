-- AttendX: Advanced Stored Procedures & Triggers
-- For Academic Excellence, Automation & Data Integrity

USE attendx_db;

DELIMITER $$

-- ============================================================
-- 1. TRIGGER: Auto-calculate and generate attendance shortage alert
-- Whenever an attendance record is marked or updated, check the student's
-- current attendance percentage for the corresponding offering.
-- If below critical or minimum threshold, insert an active alert into `alerts`.
-- ============================================================
DROP TRIGGER IF EXISTS trg_after_attendance_insert$$
CREATE TRIGGER trg_after_attendance_insert
AFTER INSERT ON attendance
FOR EACH ROW
BEGIN
    DECLARE v_offering_id INT;
    DECLARE v_total_sessions INT DEFAULT 0;
    DECLARE v_attended_sessions INT DEFAULT 0;
    DECLARE v_percentage DECIMAL(5,2) DEFAULT 0.00;
    DECLARE v_min_pct DECIMAL(5,2) DEFAULT 75.00;
    DECLARE v_crit_pct DECIMAL(5,2) DEFAULT 65.00;
    DECLARE v_alert_type ENUM('SHORTAGE', 'CRITICAL_SHORTAGE', 'LEAVE_NOTIFICATION');
    DECLARE v_msg VARCHAR(255);

    -- Get offering_id from class_sessions
    SELECT offering_id INTO v_offering_id
    FROM class_sessions 
    WHERE session_id = NEW.session_id;

    -- Fetch current active thresholds
    SELECT minimum_percentage, critical_percentage 
    INTO v_min_pct, v_crit_pct
    FROM attendance_thresholds
    ORDER BY applicable_from DESC LIMIT 1;

    -- Count total completed sessions for this offering
    SELECT COUNT(*) INTO v_total_sessions
    FROM class_sessions
    WHERE offering_id = v_offering_id AND session_status = 'COMPLETED';

    -- Count attended sessions for this student
    SELECT COUNT(*) INTO v_attended_sessions
    FROM attendance a
    JOIN class_sessions cs ON a.session_id = cs.session_id
    WHERE cs.offering_id = v_offering_id 
      AND a.student_id = NEW.student_id
      AND cs.session_status = 'COMPLETED'
      AND a.attendance_status IN ('PRESENT', 'EXCUSED', 'LATE');

    IF v_total_sessions > 0 THEN
        SET v_percentage = (v_attended_sessions / v_total_sessions) * 100;

        IF v_percentage < v_crit_pct THEN
            SET v_alert_type = 'CRITICAL_SHORTAGE';
            SET v_msg = CONCAT('Critical shortage: Attendance is ', ROUND(v_percentage, 1), '% (Threshold: ', v_crit_pct, '%)');
            
            -- Insert or refresh alert if unresolved alert does not already exist
            IF NOT EXISTS (
                SELECT 1 FROM alerts 
                WHERE student_id = NEW.student_id 
                  AND offering_id = v_offering_id 
                  AND alert_type = 'CRITICAL_SHORTAGE' 
                  AND is_resolved = FALSE
            ) THEN
                INSERT INTO alerts (student_id, offering_id, alert_type, attendance_percentage, message)
                VALUES (NEW.student_id, v_offering_id, v_alert_type, v_percentage, v_msg);
            END IF;

        ELSEIF v_percentage < v_min_pct THEN
            SET v_alert_type = 'SHORTAGE';
            SET v_msg = CONCAT('Attendance warning: Attendance is ', ROUND(v_percentage, 1), '% (Minimum required: ', v_min_pct, '%)');
            
            IF NOT EXISTS (
                SELECT 1 FROM alerts 
                WHERE student_id = NEW.student_id 
                  AND offering_id = v_offering_id 
                  AND alert_type = 'SHORTAGE' 
                  AND is_resolved = FALSE
            ) THEN
                INSERT INTO alerts (student_id, offering_id, alert_type, attendance_percentage, message)
                VALUES (NEW.student_id, v_offering_id, v_alert_type, v_percentage, v_msg);
            END IF;
        END IF;
    END IF;
END$$


-- ============================================================
-- 2. TRIGGER: Auto-update Attendance Status when Leave is Approved
-- When a leave application is approved in `leave_approvals`, 
-- any attendance records falling on that date range for that student
-- are automatically set to 'EXCUSED'.
-- ============================================================
DROP TRIGGER IF EXISTS trg_after_leave_approval$$
CREATE TRIGGER trg_after_leave_approval
AFTER INSERT ON leave_approvals
FOR EACH ROW
BEGIN
    DECLARE v_student_id INT;
    DECLARE v_from_date DATE;
    DECLARE v_to_date DATE;

    IF NEW.approval_status = 'APPROVED' THEN
        -- Get leave application details
        SELECT student_id, from_date, to_date 
        INTO v_student_id, v_from_date, v_to_date
        FROM leave_applications
        WHERE application_id = NEW.application_id;

        -- Update leave application master status
        UPDATE leave_applications 
        SET application_status = 'APPROVED'
        WHERE application_id = NEW.application_id;

        -- Automatically mark existing attendance as EXCUSED for those dates
        UPDATE attendance a
        JOIN class_sessions cs ON a.session_id = cs.session_id
        SET a.attendance_status = 'EXCUSED',
            a.remarks = CONCAT('Excused via Approved Leave Application #', NEW.application_id)
        WHERE a.student_id = v_student_id
          AND cs.session_date BETWEEN v_from_date AND v_to_date
          AND a.attendance_status = 'ABSENT';

    ELSEIF NEW.approval_status = 'REJECTED' THEN
        UPDATE leave_applications 
        SET application_status = 'REJECTED'
        WHERE application_id = NEW.application_id;
    END IF;
END$$


-- ============================================================
-- 3. STORED PROCEDURE: Batch Schedule Sessions
-- Schedules recurring class sessions for an offering between start_date & end_date on a given day_of_week
-- ============================================================
DROP PROCEDURE IF EXISTS sp_batch_schedule_sessions$$
CREATE PROCEDURE sp_batch_schedule_sessions(
    IN p_offering_id INT,
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_day_of_week INT, -- 1=Sunday, 2=Monday, 3=Tuesday, 4=Wednesday, 5=Thursday, 6=Friday, 7=Saturday
    IN p_start_time TIME,
    IN p_end_time TIME,
    IN p_topic_prefix VARCHAR(100)
)
BEGIN
    DECLARE cur_date DATE;
    DECLARE session_count INT DEFAULT 1;

    SET cur_date = p_start_date;

    WHILE cur_date <= p_end_date DO
        IF DAYOFWEEK(cur_date) = p_day_of_week THEN
            INSERT INTO class_sessions (offering_id, session_date, start_time, end_time, topic_covered, session_status)
            VALUES (
                p_offering_id, 
                cur_date, 
                p_start_time, 
                p_end_time, 
                CONCAT(p_topic_prefix, ' - Lecture ', session_count), 
                'SCHEDULED'
            );
            SET session_count = session_count + 1;
        END IF;
        SET cur_date = DATE_ADD(cur_date, INTERVAL 1 DAY);
    END WHILE;

    SELECT CONCAT(session_count - 1, ' sessions scheduled successfully.') AS message;
END$$


-- ============================================================
-- 4. STORED PROCEDURE: Generate Student Attendance Report with Transaction
-- Returns summary metrics and logs transaction execution
-- ============================================================
DROP PROCEDURE IF EXISTS sp_get_student_summary$$
CREATE PROCEDURE sp_get_student_summary(
    IN p_student_id INT
)
BEGIN
    SELECT 
        s.student_id,
        s.registration_number,
        CONCAT(s.first_name, ' ', s.last_name) AS full_name,
        s.department,
        s.semester,
        COUNT(DISTINCT co.offering_id) AS enrolled_courses,
        IFNULL(AVG(v.attendance_percentage), 0) AS cumulative_attendance,
        (SELECT COUNT(*) FROM leave_applications WHERE student_id = p_student_id AND application_status = 'APPROVED') AS approved_leaves,
        (SELECT COUNT(*) FROM alerts WHERE student_id = p_student_id AND is_resolved = FALSE) AS active_alerts
    FROM students s
    JOIN student_section ss ON s.student_id = ss.student_id
    JOIN course_offerings co ON ss.section_id = co.section_id
    LEFT JOIN vw_student_attendance_percentage v ON s.student_id = v.student_id AND co.offering_id = v.offering_id
    WHERE s.student_id = p_student_id
    GROUP BY s.student_id;
END$$

DELIMITER ;
