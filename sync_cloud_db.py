import mysql.connector
import sqlite3
import os

def export_mysql_to_sqlite():
    print("Connecting to local MySQL...")
    mconn = mysql.connector.connect(host='localhost', user='root', password='yash', database='attendx_db')
    mcur = mconn.cursor(dictionary=True)

    db_path = os.path.join(os.path.dirname(__file__), 'attendx_cloud.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    print(f"Creating SQLite database at: {db_path}")

    sconn = sqlite3.connect(db_path)
    scur = sconn.cursor()

    # DDL for SQLite tables matching MySQL 8.0 schema
    ddl_statements = [
        """
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            registration_number TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            department TEXT NOT NULL,
            semester INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE faculty (
            faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            faculty_code TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            designation TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT UNIQUE NOT NULL,
            course_name TEXT NOT NULL,
            credits INTEGER,
            department TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE sections (
            section_id INTEGER PRIMARY KEY AUTOINCREMENT,
            section_name TEXT NOT NULL,
            semester INTEGER NOT NULL,
            academic_year TEXT NOT NULL,
            department TEXT NOT NULL,
            UNIQUE(section_name, semester, academic_year, department)
        );
        """,
        """
        CREATE TABLE student_section (
            student_section_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            section_id INTEGER NOT NULL,
            academic_year TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
            UNIQUE(student_id, section_id, academic_year)
        );
        """,
        """
        CREATE TABLE course_offerings (
            offering_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            section_id INTEGER NOT NULL,
            faculty_id INTEGER NOT NULL,
            academic_year TEXT NOT NULL,
            semester INTEGER NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
            FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
            FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE,
            UNIQUE(course_id, section_id, academic_year, semester)
        );
        """,
        """
        CREATE TABLE class_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            offering_id INTEGER NOT NULL,
            session_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            topic_covered TEXT,
            session_status TEXT DEFAULT 'SCHEDULED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id) ON DELETE CASCADE,
            UNIQUE(offering_id, session_date, start_time)
        );
        """,
        """
        CREATE TABLE attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            attendance_status TEXT NOT NULL,
            marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            remarks TEXT,
            FOREIGN KEY (session_id) REFERENCES class_sessions(session_id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            UNIQUE(session_id, student_id)
        );
        """,
        """
        CREATE TABLE leave_types (
            leave_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            leave_type_name TEXT UNIQUE NOT NULL,
            description TEXT,
            max_days INTEGER,
            requires_document INTEGER DEFAULT 0
        );
        """,
        """
        CREATE TABLE leave_applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            leave_type_id INTEGER NOT NULL,
            from_date TEXT NOT NULL,
            to_date TEXT NOT NULL,
            reason TEXT NOT NULL,
            application_status TEXT DEFAULT 'PENDING',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (leave_type_id) REFERENCES leave_types(leave_type_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE leave_approvals (
            approval_id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            faculty_id INTEGER NOT NULL,
            approval_status TEXT NOT NULL,
            remarks TEXT,
            approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (application_id) REFERENCES leave_applications(application_id) ON DELETE CASCADE,
            FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE makeup_sessions (
            makeup_id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_session_id INTEGER NOT NULL,
            makeup_session_id INTEGER NOT NULL,
            reason TEXT,
            created_by INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (original_session_id) REFERENCES class_sessions(session_id) ON DELETE CASCADE,
            FOREIGN KEY (makeup_session_id) REFERENCES class_sessions(session_id) ON DELETE CASCADE,
            FOREIGN KEY (created_by) REFERENCES faculty(faculty_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE alerts (
            alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            offering_id INTEGER NOT NULL,
            alert_type TEXT NOT NULL,
            attendance_percentage REAL,
            message TEXT NOT NULL,
            is_resolved INTEGER DEFAULT 0,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE attendance_thresholds (
            threshold_id INTEGER PRIMARY KEY AUTOINCREMENT,
            minimum_percentage REAL NOT NULL,
            critical_percentage REAL NOT NULL,
            applicable_from TEXT NOT NULL
        );
        """
    ]

    for stmt in ddl_statements:
        scur.execute(stmt)

    # Copy data for each table
    tables = [
        'users', 'students', 'faculty', 'courses', 'sections',
        'student_section', 'course_offerings', 'class_sessions',
        'attendance', 'leave_types', 'leave_applications',
        'leave_approvals', 'makeup_sessions', 'alerts', 'attendance_thresholds'
    ]

    for t in tables:
        mcur.execute(f"SELECT * FROM {t}")
        rows = mcur.fetchall()
        if not rows:
            print(f"Table {t}: 0 rows")
            continue
        cols = list(rows[0].keys())
        placeholders = ", ".join(["?"] * len(cols))
        col_names = ", ".join(cols)
        sql = f"INSERT INTO {t} ({col_names}) VALUES ({placeholders})"
        data_to_insert = []
        for r in rows:
            row_vals = []
            for col in cols:
                val = r[col]
                # convert dates/decimals/timestamps to strings/floats/ints
                if val is not None and not isinstance(val, (int, float, str, bytes)):
                    val = str(val)
                row_vals.append(val)
            data_to_insert.append(row_vals)
        scur.executemany(sql, data_to_insert)
        print(f"Table {t}: copied {len(rows)} rows.")

    # Create Views in SQLite
    views = [
        """
        CREATE VIEW IF NOT EXISTS vw_student_attendance_percentage AS
        SELECT 
            s.student_id,
            s.registration_number,
            (s.first_name || ' ' || s.last_name) AS student_name,
            c.course_code,
            c.course_name,
            sec.section_name,
            co.offering_id,
            COUNT(cs.session_id) AS total_completed_sessions,
            SUM(CASE WHEN a.attendance_status IN ('PRESENT', 'EXCUSED', 'LATE') THEN 1 ELSE 0 END) AS attended_sessions,
            ROUND(IFNULL(
                (CAST(SUM(CASE WHEN a.attendance_status IN ('PRESENT', 'EXCUSED', 'LATE') THEN 1 ELSE 0 END) AS FLOAT) / COUNT(cs.session_id)) * 100, 
                0.0
            ), 2) AS attendance_percentage
        FROM students s
        JOIN student_section ss ON s.student_id = ss.student_id
        JOIN sections sec ON ss.section_id = sec.section_id
        JOIN course_offerings co ON sec.section_id = co.section_id
        JOIN courses c ON co.course_id = c.course_id
        JOIN class_sessions cs ON co.offering_id = cs.offering_id AND cs.session_status = 'COMPLETED'
        LEFT JOIN attendance a ON cs.session_id = a.session_id AND s.student_id = a.student_id
        GROUP BY s.student_id, c.course_id, co.offering_id;
        """,
        """
        CREATE VIEW IF NOT EXISTS vw_attendance_shortage AS
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
        """,
        """
        CREATE VIEW IF NOT EXISTS vw_leave_history AS
        SELECT 
            la.application_id,
            s.student_id,
            s.registration_number,
            (s.first_name || ' ' || s.last_name) AS student_name,
            lt.leave_type_name,
            la.from_date,
            la.to_date,
            CAST(julianday(la.to_date) - julianday(la.from_date) + 1 AS INT) AS num_days,
            la.reason,
            la.application_status,
            (f.first_name || ' ' || f.last_name) AS approver_name,
            lap.remarks,
            lap.approved_at
        FROM leave_applications la
        JOIN students s ON la.student_id = s.student_id
        JOIN leave_types lt ON la.leave_type_id = lt.leave_type_id
        LEFT JOIN leave_approvals lap ON la.application_id = lap.application_id
        LEFT JOIN faculty f ON lap.faculty_id = f.faculty_id;
        """,
        """
        CREATE VIEW IF NOT EXISTS vw_course_attendance_summary AS
        SELECT 
            c.course_code,
            c.course_name,
            sec.section_name,
            (f.first_name || ' ' || f.last_name) AS faculty_name,
            COUNT(DISTINCT ss.student_id) AS total_students,
            COUNT(DISTINCT cs.session_id) AS total_sessions,
            ROUND(AVG(v.attendance_percentage), 2) AS average_attendance
        FROM course_offerings co
        JOIN courses c ON co.course_id = c.course_id
        JOIN sections sec ON co.section_id = sec.section_id
        JOIN faculty f ON co.faculty_id = f.faculty_id
        LEFT JOIN student_section ss ON sec.section_id = ss.section_id
        LEFT JOIN class_sessions cs ON co.offering_id = cs.offering_id AND cs.session_status = 'COMPLETED'
        LEFT JOIN vw_student_attendance_percentage v ON co.offering_id = v.offering_id AND ss.student_id = v.student_id
        GROUP BY co.offering_id;
        """,
        """
        CREATE VIEW IF NOT EXISTS vw_monthly_attendance_trends AS
        SELECT 
            strftime('%Y-%m', cs.session_date) AS month,
            c.course_code,
            c.course_name,
            s.student_id,
            (s.first_name || ' ' || s.last_name) AS student_name,
            COUNT(cs.session_id) AS total_sessions,
            SUM(CASE WHEN a.attendance_status IN ('PRESENT', 'EXCUSED', 'LATE') THEN 1 ELSE 0 END) AS attended_sessions,
            ROUND(IFNULL(
                (CAST(SUM(CASE WHEN a.attendance_status IN ('PRESENT', 'EXCUSED', 'LATE') THEN 1 ELSE 0 END) AS FLOAT) / COUNT(cs.session_id)) * 100, 
                0.0
            ), 2) AS attendance_percentage
        FROM class_sessions cs
        JOIN course_offerings co ON cs.offering_id = co.offering_id
        JOIN courses c ON co.course_id = c.course_id
        JOIN attendance a ON cs.session_id = a.session_id
        JOIN students s ON a.student_id = s.student_id
        WHERE cs.session_status = 'COMPLETED'
        GROUP BY month, c.course_id, s.student_id;
        """
    ]

    for v in views:
        scur.execute(v)
    print("All 5 views created successfully in SQLite!")

    sconn.commit()
    scur.close()
    sconn.close()
    mcur.close()
    mconn.close()
    print("Export complete: attendx_cloud.db is ready for deployment!")

if __name__ == '__main__':
    export_mysql_to_sqlite()
