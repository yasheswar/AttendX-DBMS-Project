# AttendX: Smart Student Attendance & Leave Management System
### Full Academic DBMS Implementation (Production Quality)

AttendX is a full-stack, enterprise-grade academic Relational Database Management System developed to automate student presence tracking, course scheduling, leave application workflows, and automated shortage alerting for universities.

Designed specifically to demonstrate rigorous database architecture concepts, relational integrity, 3NF/BCNF normalization, views, triggers, and stored procedures for DBMS viva and PBL evaluations.

---

## 🌟 Key Functional Pillars

1. **Academic Master Management**:
   - Courses, Sections, Faculty assignments, and Academic terms.
   - `course_offerings` ternary associative relationship connecting Course + Section + Faculty.
2. **Session & Presence Management**:
   - Class sessions tracking topics, schedules, and statuses (`SCHEDULED`, `COMPLETED`, `CANCELLED`, `MAKEUP`).
   - Session-by-session student presence recording (`PRESENT`, `ABSENT`, `LATE`, `EXCUSED`).
   - Strict `UNIQUE(session_id, student_id)` constraints preventing duplicate entries.
3. **Automated Triggers & Stored Procedures**:
   - `trg_after_attendance_insert`: Automatically calculates dynamic attendance percentages and triggers shortage warnings in real-time.
   - `trg_after_leave_approval`: Automatically flips previously recorded `ABSENT` attendances to `EXCUSED` across the approved leave date range.
   - `sp_batch_schedule_sessions`: Stored procedure to batch generate an entire semester's lecture schedules with a single call.
   - `sp_get_student_summary`: Complex analytical stored procedure with subqueries.
4. **End-to-End Digital Leave Workflow**:
   - Leave Types, dynamic document requirements, multi-day requests, and faculty approval audit trails.
5. **Makeup Session Linkage**:
   - Links newly scheduled makeup lectures back to cancelled classes with integrity checks (`CHECK(original_session_id != makeup_session_id)`).
6. **Analytics & Views**:
   - 5 Production-grade Database Views providing live aggregation without dirty reads.

---

## 🏗️ Architecture & Technology Stack

- **Frontend / Application Engine**: Python, Streamlit (Custom UI with interactive Plotly dashboards)
- **Database Server**: MySQL 8.0+
- **Driver**: `mysql-connector-python`
- **Security**: SHA-256 password hashing with role-based session tokens
- **Data Normalization Level**: 3NF & BCNF certified

---

## 🚀 Step-by-Step Installation & Run Guide

### 1. Database Setup in MySQL:
Execute the scripts in order in MySQL Workbench or Command Line:
```sql
SOURCE database/database.sql;
SOURCE database/views.sql;
SOURCE database/procedures_and_triggers.sql;
SOURCE database/sample_data.sql;
```

### 2. Environment Configuration:
Verify or update your `.env` file in the project root:
```ini
DB_HOST=localhost
DB_PORT=3306
DB_NAME=attendx_db
DB_USER=root
DB_PASSWORD=your_mysql_password
```

### 3. Launch the Application:
```powershell
pip install -r requirements.txt
python -m streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 🔑 Demo Role Accounts

| Role | Username | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `Admin@123` | System Master CRUD, View/SQL Sandboxes, Analytics, Global Metrics |
| **Faculty** | `faculty1` | `Faculty@123` | Session Creation, Grid Attendance, Leave Approvals, Makeup Classes |
| **Student** | `student1` | `Student@123` | Live Standing, Leave Applications, Shortage Alerts, Session History |

---

## 🎓 Academic Viva Cheat-Sheet
- **Number of Tables**: 15 Normalized Relations
- **M:N Resolutions**:
  - `STUDENTS` ↔ `CLASS_SESSIONS` resolved via associative entity `ATTENDANCE`.
  - `STUDENTS` ↔ `SECTIONS` resolved via `STUDENT_SECTION`.
  - `COURSES` ↔ `SECTIONS` ↔ `FACULTY` resolved via `COURSE_OFFERINGS`.
- **Primary Keys**: Surrogate auto-increment integers ensuring referential immutability.
- **Constraints**:
  - `CHECK (end_time > start_time)`
  - `CHECK (from_date <= to_date)`
  - `CHECK (minimum_percentage > critical_percentage)`
  - `UNIQUE (session_id, student_id)`
  - `ON DELETE CASCADE` on all foreign key links.
