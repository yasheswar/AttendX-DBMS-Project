-- AttendX Database Schema
-- Normalization: Up to 3NF

CREATE DATABASE IF NOT EXISTS attendx_db;
USE attendx_db;

-- 1. users
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('ADMIN', 'FACULTY', 'STUDENT') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. students
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    registration_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    department VARCHAR(50) NOT NULL,
    semester INT CHECK (semester BETWEEN 1 AND 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 3. faculty
CREATE TABLE faculty (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    faculty_code VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(50) NOT NULL,
    designation VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 4. courses
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    credits INT CHECK (credits > 0),
    department VARCHAR(50) NOT NULL
);

-- 5. sections
CREATE TABLE sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    section_name VARCHAR(20) NOT NULL,
    semester INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    department VARCHAR(50) NOT NULL,
    UNIQUE (section_name, semester, academic_year, department)
);

-- 6. student_section
CREATE TABLE student_section (
    student_section_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    section_id INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
    UNIQUE (student_id, section_id, academic_year)
);

-- 7. course_offerings
CREATE TABLE course_offerings (
    offering_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    section_id INT NOT NULL,
    faculty_id INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    semester INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE,
    UNIQUE (course_id, section_id, academic_year, semester)
);

-- 8. class_sessions
CREATE TABLE class_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    offering_id INT NOT NULL,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    topic_covered VARCHAR(255),
    session_status ENUM('SCHEDULED', 'COMPLETED', 'CANCELLED', 'MAKEUP') DEFAULT 'SCHEDULED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id) ON DELETE CASCADE,
    CHECK (end_time > start_time),
    UNIQUE (offering_id, session_date, start_time)
);

-- 9. attendance
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    student_id INT NOT NULL,
    attendance_status ENUM('PRESENT', 'ABSENT', 'LATE', 'EXCUSED') NOT NULL,
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    remarks VARCHAR(255),
    FOREIGN KEY (session_id) REFERENCES class_sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    UNIQUE (session_id, student_id)
);

-- 10. leave_types
CREATE TABLE leave_types (
    leave_type_id INT AUTO_INCREMENT PRIMARY KEY,
    leave_type_name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    max_days INT CHECK (max_days > 0),
    requires_document BOOLEAN DEFAULT FALSE
);

-- 11. leave_applications
CREATE TABLE leave_applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    leave_type_id INT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    reason TEXT NOT NULL,
    application_status ENUM('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED') DEFAULT 'PENDING',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (leave_type_id) REFERENCES leave_types(leave_type_id) ON DELETE CASCADE,
    CHECK (from_date <= to_date)
);

-- 12. leave_approvals
CREATE TABLE leave_approvals (
    approval_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL,
    faculty_id INT NOT NULL,
    approval_status ENUM('APPROVED', 'REJECTED') NOT NULL,
    remarks VARCHAR(255),
    approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES leave_applications(application_id) ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE
);

-- 13. makeup_sessions
CREATE TABLE makeup_sessions (
    makeup_id INT AUTO_INCREMENT PRIMARY KEY,
    original_session_id INT NOT NULL,
    makeup_session_id INT NOT NULL,
    reason VARCHAR(255),
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (original_session_id) REFERENCES class_sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (makeup_session_id) REFERENCES class_sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES faculty(faculty_id) ON DELETE CASCADE,
    CHECK (original_session_id != makeup_session_id)
);

-- 14. alerts
CREATE TABLE alerts (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    offering_id INT NOT NULL,
    alert_type ENUM('SHORTAGE', 'CRITICAL_SHORTAGE', 'LEAVE_NOTIFICATION') NOT NULL,
    attendance_percentage DECIMAL(5, 2) CHECK (attendance_percentage BETWEEN 0 AND 100),
    message VARCHAR(255) NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id) ON DELETE CASCADE
);

-- 15. attendance_thresholds
CREATE TABLE attendance_thresholds (
    threshold_id INT AUTO_INCREMENT PRIMARY KEY,
    minimum_percentage DECIMAL(5, 2) NOT NULL,
    critical_percentage DECIMAL(5, 2) NOT NULL,
    applicable_from DATE NOT NULL,
    CHECK (minimum_percentage > critical_percentage)
);

-- ==========================================
-- INDEXES
-- ==========================================
-- To improve query performance for frequent lookups

-- Search student by registration number
CREATE INDEX idx_student_registration ON students(registration_number);
-- Search course by code
CREATE INDEX idx_course_code ON courses(course_code);
-- Sessions lookup by date
CREATE INDEX idx_session_date ON class_sessions(session_date);
-- Leave lookups
CREATE INDEX idx_leave_status ON leave_applications(application_status);
CREATE INDEX idx_leave_dates ON leave_applications(from_date, to_date);
-- Alert lookups
CREATE INDEX idx_alert_unresolved ON alerts(is_resolved) WHERE is_resolved = FALSE;
