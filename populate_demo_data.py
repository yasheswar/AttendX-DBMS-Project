import mysql.connector
import datetime
import random

conn = mysql.connector.connect(host='localhost', user='root', password='yash', database='attendx_db')
cursor = conn.cursor(dictionary=True)

print("Populating rich realistic demo data...")

# 1. Clear existing sessions and attendance if any to prevent conflicts
cursor.execute("DELETE FROM attendance")
cursor.execute("DELETE FROM makeup_sessions")
cursor.execute("DELETE FROM class_sessions")
cursor.execute("DELETE FROM leave_approvals")
cursor.execute("DELETE FROM leave_applications")
cursor.execute("DELETE FROM alerts")

# Offerings map:
# 1: CS301 (DBMS) -> Section 1 (CS-A) -> Faculty 1
# 2: CS302 (OS) -> Section 1 (CS-A) -> Faculty 2
# 3: IT301 (Web Tech) -> Section 2 (IT-A) -> Faculty 2
# 4: IT302 (CN) -> Section 2 (IT-A) -> Faculty 1
# 5: EC301 (DSP) -> Section 3 (EC-A) -> Faculty 3

# Section 1 students: [1, 2, 6, 9]
# Section 2 students: [3, 4, 7, 10]
# Section 3 students: [5, 8]

# 2. Generate 12 sessions for each offering over the past 6 weeks
topics = {
    1: ["Relational Algebra", "SQL Basics & DDL", "DML & Integrity Constraints", "Nested Queries & Joins", "Normalization 1NF & 2NF", "Normalization 3NF & BCNF", "ER Modeling", "Transactions & ACID", "Indexing & B+ Trees", "Concurrency Control", "Stored Procedures", "Triggers & Views"],
    2: ["Process Management & PCB", "CPU Scheduling Algorithms", "Threads & Concurrency", "Deadlocks & Banker's Algorithm", "Memory Management Paging", "Virtual Memory & Page Replacement", "File System Architecture", "Disk Scheduling", "I/O Hardware & Drivers", "Security & Protection", "Virtual Machines", "Linux Kernel Architecture"],
    3: ["HTML5 & Semantic Markup", "CSS3 Flexbox & Grid", "JavaScript ES6 Essentials", "DOM Manipulation & Events", "Asynchronous JS & Fetch API", "Node.js & Express Basics", "RESTful API Design", "Authentication & JWT", "React Component Lifecycle", "React Hooks & State", "Database Integration", "Deployment & CI/CD"],
    4: ["OSI & TCP/IP Reference Models", "Physical Layer & Media", "Data Link Framing & CRC", "Ethernet & MAC Protocols", "Network Layer IPv4/IPv6", "Routing Algorithms Dijkstra", "Transport Layer TCP/UDP", "Flow & Congestion Control", "DNS & Application Layer", "HTTP/HTTPS & Web Protocols", "Network Security & Firewalls", "Wireless & Mobile Networks"],
    5: ["Signals & Systems Classification", "Z-Transform & Properties", "Fourier Transform & Spectra", "Discrete Fourier Transform DFT", "Fast Fourier Transform FFT", "IIR Filter Design", "FIR Filter Design", "Windowing Techniques", "Multirate Signal Processing", "DSP Hardware Architectures", "Adaptive Filtering", "Applications in Audio/Speech"]
}

start_date = datetime.date(2023, 9, 1)

session_records = []
for offering_id in range(1, 6):
    cur_date = start_date
    session_idx = 0
    while session_idx < 12:
        # Mon, Wed, Fri
        if cur_date.weekday() in (0, 2, 4):
            topic = topics[offering_id][session_idx]
            status = 'COMPLETED'
            # Let session 8 be cancelled and have a makeup
            if session_idx == 8:
                status = 'CANCELLED'
            
            cursor.execute("""
                INSERT INTO class_sessions (offering_id, session_date, start_time, end_time, topic_covered, session_status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (offering_id, cur_date, '10:00:00', '11:00:00', topic, status))
            sess_id = cursor.lastrowid
            session_records.append({
                'session_id': sess_id,
                'offering_id': offering_id,
                'session_date': cur_date,
                'status': status,
                'session_idx': session_idx
            })
            session_idx += 1
        cur_date += datetime.timedelta(days=1)

print(f"Created {len(session_records)} class sessions.")

# 3. Add Makeup sessions for cancelled sessions
for s in session_records:
    if s['status'] == 'CANCELLED':
        makeup_date = s['session_date'] + datetime.timedelta(days=7)
        cursor.execute("""
            INSERT INTO class_sessions (offering_id, session_date, start_time, end_time, topic_covered, session_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (s['offering_id'], makeup_date, '14:00:00', '15:00:00', f"Makeup for {s['session_date']}", 'COMPLETED'))
        makeup_id = cursor.lastrowid
        
        # Link in makeup_sessions
        # Created by faculty 1 or 2
        fac_id = 1 if s['offering_id'] in (1, 4) else (2 if s['offering_id'] in (2, 3) else 3)
        cursor.execute("""
            INSERT INTO makeup_sessions (original_session_id, makeup_session_id, reason, created_by)
            VALUES (%s, %s, %s, %s)
        """, (s['session_id'], makeup_id, 'Faculty emergency leave', fac_id))
        
        s_makeup = {
            'session_id': makeup_id,
            'offering_id': s['offering_id'],
            'session_date': makeup_date,
            'status': 'COMPLETED',
            'session_idx': 99
        }
        session_records.append(s_makeup)

# 4. Enrolled students mapping
offering_students = {
    1: [1, 2, 6, 9],  # CS-A
    2: [1, 2, 6, 9],  # CS-A
    3: [3, 4, 7, 10], # IT-A
    4: [3, 4, 7, 10], # IT-A
    5: [5, 8]         # EC-A
}

# Student profiles for realistic variation:
# Student 1 (Rahul Verma): Good student (90% attendance)
# Student 2 (Priya Patel): Critical Shortage (<60% attendance) -> demonstrate Shortage Alert!
# Student 6 (Sneha Reddy): Warning Shortage (70% attendance) -> demonstrate Alert!
# Student 9 (Rohan Desai): 85% attendance
# Other students varying between 75% and 95%

random.seed(42)

total_attendance_marked = 0
for s in session_records:
    if s['status'] != 'COMPLETED':
        continue
    
    stus = offering_students[s['offering_id']]
    for sid in stus:
        if sid == 1:
            # High attendance
            status = 'PRESENT' if random.random() < 0.92 else 'ABSENT'
        elif sid == 2:
            # Critical Shortage student!
            status = 'ABSENT' if random.random() < 0.45 else 'PRESENT'
        elif sid == 6:
            # Warning Shortage student
            status = 'ABSENT' if random.random() < 0.32 else 'PRESENT'
        else:
            status = 'PRESENT' if random.random() < 0.85 else ('LATE' if random.random() < 0.5 else 'ABSENT')
            
        cursor.execute("""
            INSERT INTO attendance (session_id, student_id, attendance_status, remarks)
            VALUES (%s, %s, %s, %s)
        """, (s['session_id'], sid, status, 'Regular attendance' if status == 'PRESENT' else ('Late entry by 10 mins' if status == 'LATE' else 'Absent without notice')))
        total_attendance_marked += 1

print(f"Recorded {total_attendance_marked} attendance records.")

# 5. Populate Leave Applications & Approvals
leave_samples = [
    # student 1: Medical leave (Approved)
    (1, 1, '2023-09-08', '2023-09-10', 'Viral fever and doctor prescribed rest', 'APPROVED', 1, 'Medical certificate verified. Approved.'),
    # student 2: Personal leave (Approved)
    (2, 2, '2023-09-15', '2023-09-16', 'Attending sister wedding ceremony in hometown', 'APPROVED', 2, 'Approved. Please collect notes.'),
    # student 6: Academic leave (Approved)
    (6, 3, '2023-09-20', '2023-09-22', 'Participating in National Hackathon 2023', 'APPROVED', 1, 'Outstanding initiative. Leave granted.'),
    # student 3: Emergency leave (Rejected)
    (3, 4, '2023-09-25', '2023-09-26', 'Family emergency at home', 'REJECTED', 2, 'Attendance too low. Application rejected.'),
    # student 4: Medical leave (Pending)
    (4, 1, '2023-10-02', '2023-10-04', 'Dental surgery follow-up treatment', 'PENDING', None, None),
    # student 1: Personal leave (Pending)
    (1, 2, '2023-10-10', '2023-10-11', 'Family travel commitment', 'PENDING', None, None),
]

for stu_id, lt_id, f_date, t_date, reason, app_status, fac_id, remarks in leave_samples:
    cursor.execute("""
        INSERT INTO leave_applications (student_id, leave_type_id, from_date, to_date, reason, application_status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (stu_id, lt_id, f_date, t_date, reason, app_status))
    app_id = cursor.lastrowid
    
    if app_status in ('APPROVED', 'REJECTED') and fac_id:
        cursor.execute("""
            INSERT INTO leave_approvals (application_id, faculty_id, approval_status, remarks)
            VALUES (%s, %s, %s, %s)
        """, (app_id, fac_id, app_status, remarks))

print("Populated realistic leave applications & approvals.")

# 6. Generate Alerts using the database view
cursor.execute("""
    INSERT INTO alerts (student_id, offering_id, alert_type, attendance_percentage, message, is_resolved)
    SELECT 
        v.student_id,
        v.offering_id,
        v.shortage_level,
        v.attendance_percentage,
        CONCAT('Attendance is ', ROUND(v.attendance_percentage, 1), '% in ', v.course_code, ' - ', v.course_name),
        FALSE
    FROM vw_attendance_shortage v
    WHERE v.shortage_level != 'GOOD'
""")

conn.commit()
cursor.close()
conn.close()
print("All demo data committed successfully!")
