import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=60, bottom=60, left=90, right=90):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level):
    h = doc.add_paragraph()
    if level == 1:
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        r = h.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = RGBColor(160, 20, 30)
    elif level == 2:
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(3)
        r = h.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 58, 138)
    elif level == 3:
        h.paragraph_format.space_before = Pt(7)
        h.paragraph_format.space_after = Pt(2)
        r = h.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(55, 65, 81)
    return h

def add_body_p(doc, text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    return p

def add_compact_table(doc, headers, data, col_widths=None):
    t = doc.add_table(rows=len(data) + 1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = 'Table Grid'
    
    # Headers
    for c_i, h in enumerate(headers):
        cell = t.cell(0, c_i)
        cell.text = h
        set_cell_background(cell, "E0E7FF")
        set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
        for p in cell.paragraphs:
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.bold = True
                r.font.size = Pt(9.5)
                
    # Data Rows
    for r_i, row in enumerate(data):
        bg = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
        for c_i, val in enumerate(row):
            cell = t.cell(r_i + 1, c_i)
            cell.text = str(val)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=90, right=90)
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(0)
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(9)
                    
    if col_widths:
        for row in t.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)
                
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(2)
    p_spacer.paragraph_format.space_after = Pt(4)

def add_code_snippet(doc, code_str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(code_str)
    r.font.name = 'Consolas'
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(30, 41, 59)

def build_perfect_report():
    doc = docx.Document()
    
    # Page setup - 0.85 inch margins for perfect layout density
    for s in doc.sections:
        s.top_margin = Inches(0.85)
        s.bottom_margin = Inches(0.85)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)
        s.page_width = Inches(8.5)
        s.page_height = Inches(11.0)

    # Base Normal Style
    normal = doc.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(11)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    p_cov = doc.add_paragraph()
    p_cov.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_cov.add_run("Woxsen University\n")
    r1.font.size = Pt(22)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(160, 20, 30)

    r2 = p_cov.add_run("School of Technology\nDEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n\n")
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(60, 60, 60)

    r3 = p_cov.add_run("PROJECT BASED LEARNING (PBL) REPORT\n")
    r3.font.size = Pt(15)
    r3.font.bold = True
    r3.font.underline = True

    r4 = p_cov.add_run("Course: Database Management Systems (DBMS) | Academic Year: 2026–27\n\n")
    r4.font.size = Pt(12)
    r4.font.italic = True

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(16)
    p_t.paragraph_format.space_after = Pt(24)
    r_t1 = p_t.add_run("PROJECT TITLE:\n")
    r_t1.font.size = Pt(12)
    r_t1.font.bold = True
    r_t2 = p_t.add_run("DESIGN AND IMPLEMENTATION OF A DATABASE MANAGEMENT SYSTEM FOR STUDENT ATTENDANCE AND LEAVE APPROVAL MANAGEMENT SYSTEM (AttendX)")
    r_t2.font.size = Pt(15)
    r_t2.font.bold = True
    r_t2.font.color.rgb = RGBColor(160, 20, 30)

    t_cov = doc.add_table(rows=1, cols=2)
    t_cov.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cov.columns[0].width = Inches(3.4)
    t_cov.columns[1].width = Inches(3.4)
    cl = t_cov.cell(0, 0).paragraphs[0]
    cl.add_run("Submitted by:\n").bold = True
    cl.add_run("Name: Yasheswar Kataria\n")
    cl.add_run("Roll Number: 25WU0101156\n")
    cl.add_run("Program: B.Tech – CSE\n")
    cl.add_run("Section: CSE - Panthers\n")
    
    cr = t_cov.cell(0, 1).paragraphs[0]
    cr.add_run("Under the Guidance of:\n").bold = True
    cr.add_run("Faculty Guide:\n")
    cr.add_run("Dr. Sahithi Chennamadhavuni\n").bold = True
    cr.add_run("Associate Professor\n")
    cr.add_run("Dept. of Computer Science and Engineering\n")

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(60)
    p_foot.add_run("October, 2026\nWoxsen University, Hyderabad").bold = True

    doc.add_page_break()

    # =========================================================================
    # PRELIMINARY PAGES: CERTIFICATE & DECLARATION
    # =========================================================================
    add_styled_heading(doc, "CERTIFICATE", 1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c = doc.add_paragraph()
    p_c.paragraph_format.space_before = Pt(14)
    p_c.paragraph_format.line_spacing = 1.25
    p_c.add_run("This is to certify that the Project-Based Learning report titled ")
    p_c.add_run("“DESIGN AND IMPLEMENTATION OF A DATABASE MANAGEMENT SYSTEM FOR STUDENT ATTENDANCE AND LEAVE APPROVAL MANAGEMENT SYSTEM (AttendX)”").bold = True
    p_c.add_run(" is a bonafide work carried out by ")
    p_c.add_run("Mr. Yasheswar Kataria (Roll No: 25WU0101156)").bold = True
    p_c.add_run(", student of B.Tech – Computer Science and Engineering at Woxsen University, during the Academic Year 2026–27, in partial fulfillment of the academic curriculum for the course ")
    p_c.add_run("Database Management Systems (DBMS)").bold = True
    p_c.add_run(" under my supervision and guidance.\n\n\n\n\n\n")
    p_c.add_run("_________________________________________\n(Dr. Sahithi Chennamadhavuni)\nAssociate Professor, Dept. of CSE\nSchool of Technology, Woxsen University").bold = True

    doc.add_page_break()

    add_styled_heading(doc, "DECLARATION", 1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_d = doc.add_paragraph()
    p_d.paragraph_format.space_before = Pt(14)
    p_d.paragraph_format.line_spacing = 1.25
    p_d.add_run("I hereby declare that the project entitled ")
    p_d.add_run("“AttendX — Smart Student Attendance & Leave Management System”").bold = True
    p_d.add_run(" submitted to Woxsen University is an authentic record of original work carried out by me under the mentorship of Dr. Sahithi Chennamadhavuni. This work has not been submitted in part or full for any other diploma or degree. All external concepts, algorithms, and references have been properly cited.\n\n\n")
    p_d.add_run("Place: Hyderabad\nDate: 12th October 2026\n\n\n\n_________________________________________\nSignature of the Candidate\nName: Yasheswar Kataria (25WU0101156)").bold = True

    doc.add_page_break()

    # =========================================================================
    # PRELIMINARY: ACKNOWLEDGEMENT & ABSTRACT
    # =========================================================================
    add_styled_heading(doc, "ACKNOWLEDGEMENT", 1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_body_p(doc, "I express my sincere gratitude to my faculty guide, Dr. Sahithi Chennamadhavuni, Associate Professor, Department of Computer Science and Engineering, School of Technology, Woxsen University, for her invaluable guidance, constructive suggestions, and encouragement throughout this project. Her emphasis on rigorous 3NF normalization, relational constraints, transaction management, and active database triggers fundamentally shaped the quality of this work.")
    add_body_p(doc, "I also thank the Dean and faculty members of the School of Technology for providing the laboratory environment and resources required to complete this Project-Based Learning activity. Finally, I thank my peers and family for their continuous support.")

    add_styled_heading(doc, "ABSTRACT", 1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_body_p(doc, "Higher educational institutions depend on accurate student attendance monitoring to evaluate academic engagement and uphold university examination eligibility standards (e.g., minimum 75% attendance). However, traditional attendance processes relying on manual paper registers and disconnected spreadsheets introduce arithmetic errors, duplicate records, lost leave forms, and late shortage identification. This project designs and implements AttendX, a database-centered web application developed using Python, Streamlit, and MySQL 8.0 (InnoDB).")
    add_body_p(doc, "The system architecture is grounded in a 15-table relational schema fully normalized up to the Third Normal Form (3NF) and Boyce-Codd Normal Form (BCNF). Entity and domain integrity are enforced via primary keys, composite unique constraints (preventing duplicate attendance entries), foreign keys with ON DELETE CASCADE, and CHECK constraints. Active database triggers automate institutional business rules: 'trg_after_attendance_insert' evaluates live attendance percentages and creates shortage alerts when attendance falls below 75% or 65%; 'trg_after_leave_approval' automatically flips past absences to EXCUSED status upon faculty leave approval. Five production views provide real-time aggregation without storing derived data. The prototype provides dedicated role-based consoles for Admins, Faculty, and Students, verified through end-to-end testing against real university workflows.")
    add_body_p(doc, "Keywords: Database Management Systems, Normalization (3NF/BCNF), MySQL 8.0, Triggers, Stored Procedures, Role-Based Access Control, Attendance Management.", "KEYWORDS: ")

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    add_styled_heading(doc, "TABLE OF CONTENTS", 1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    toc_data = [
        ["1. INTRODUCTION", "1"],
        ["   1.1 Background & Real-World Motivation", "1"],
        ["   1.2 Scope & Organisation of the Report", "2"],
        ["2. PROBLEM STATEMENT AND OBJECTIVES", "3"],
        ["   2.1 Problem Definition & Measurable Objectives", "3"],
        ["   2.2 Constraints, Assumptions & Solution Strategy", "4"],
        ["   2.3 Functional Requirements Specification", "5"],
        ["3. LITERATURE REVIEW", "6"],
        ["   3.1 Relational Theory, Normalization & Active Databases", "6"],
        ["   3.2 Literature Comparison & Research Gap", "7"],
        ["4. METHODOLOGY AND SYSTEM DESIGN", "8"],
        ["   4.1 Three-Tier System Architecture", "8"],
        ["   4.2 Entity-Relationship (ER) Modeling & Cardinality", "9"],
        ["   4.3 Process Flow & Algorithmic Logic", "11"],
        ["   4.4 Data Flow Diagrams (Level-0 and Level-1)", "12"],
        ["5. LOGICAL DATABASE DESIGN & IMPLEMENTATION", "13"],
        ["   5.1 Relational Schema & Functional Dependencies", "13"],
        ["   5.2 Normalization Analysis up to 3NF and BCNF", "15"],
        ["   5.3 Data Dictionary (15 Relational Tables)", "17"],
        ["   5.4 Triggers, Stored Procedures & Analytical Views", "21"],
        ["   5.5 Application Modules & CRUD Operations", "23"],
        ["   5.6 Dataset Description & Screen Verifications", "25"],
        ["6. RESULTS AND DISCUSSION", "27"],
        ["   6.1 Functional Verification & Test Cases", "27"],
        ["   6.2 Database Integrity & Constraint Verification", "28"],
        ["   6.3 Analytical Performance Graphs & Interpretation", "29"],
        ["   6.4 Comparison with Project Objectives", "30"],
        ["7. CONCLUSION AND FUTURE SCOPE", "31"],
        ["REFERENCES & APPENDICES", "32"]
    ]
    add_compact_table(doc, ["Chapter / Section", "Page"], toc_data, col_widths=[5.5, 1.2])

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 1: INTRODUCTION", 1)
    add_styled_heading(doc, "1.1 Background & Real-World Motivation", 2)
    add_body_p(doc, "In modern university education, maintaining systematic student presence records is an institutional necessity. Regulatory university bodies enforce strict policies requiring students to attend a minimum of 75% of class sessions to remain eligible for end-semester examinations. Despite this importance, attendance tracking in many institutions is still handled manually through paper registers, attendance slips, or isolated Excel spreadsheets.")
    add_body_p(doc, "These traditional channels suffer from four core vulnerabilities: (1) Data Redundancy and Calculation Errors: Manually calculating cumulative attendance percentages across multiple subjects leads to arithmetic errors and lost records. (2) Absence of Real-Time Shortage Alerts: Students only discover their attendance shortage at the end of the term when examination admit cards are withheld. (3) Disjointed Leave Governance: Paper leave applications take days to approve and are rarely reflected back into daily registers, causing legitimate leaves to be counted as unexcused absences. (4) Untracked Makeup Sessions: Classes rescheduled to compensate for cancellations lack structured linking to the original session.")
    add_body_p(doc, "AttendX addresses these challenges by introducing a centralized, relational database management system where every student, class session, attendance record, and leave application is modeled as a normalized relation. Database constraints guarantee data integrity, while active database triggers dynamically compute shortages and reconcile leave absences.")

    add_styled_heading(doc, "1.2 Scope & Organisation of the Report", 2)
    add_body_p(doc, "The scope of AttendX encompasses: (a) Academic Master Administration (Courses, Sections, Faculty, Students, and Course Offerings); (b) Class Session Tracking (Scheduling, Completed, Cancelled, and Makeup linkage); (c) Real-time Attendance Recording with composite uniqueness; (d) Automated Shortage Alert Generation (<75% and <65% thresholds); (e) End-to-End Digital Leave Approval Workflow with automatic absence excusal; (f) Dynamic Analytical Views and Interactive Plotly Dashboards.")
    add_body_p(doc, "Exclusions: Fee processing, examination grading, hostel management, and hardware biometric sensors are kept out of scope to focus deeply on relational modeling, normalization, and database-level business logic.")

    # =========================================================================
    # CHAPTER 2: PROBLEM STATEMENT AND OBJECTIVES
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 2: PROBLEM STATEMENT AND OBJECTIVES", 1)
    add_styled_heading(doc, "2.1 Problem Definition & Measurable Objectives", 2)
    add_body_p(doc, "Problem Statement: To design and implement a secure, 3NF-normalized relational database system that centralizes student attendance tracking, class session scheduling, digital leave approval workflows, and automated shortage alerting, ensuring data integrity through database constraints and active triggers.")
    add_body_p(doc, "The project accomplishes the following seven measurable objectives:")
    add_body_p(doc, "1. Architect a 15-table relational schema fully normalized up to 3NF/BCNF without data redundancy.\n"
                    "2. Enforce database constraints: Composite UNIQUE keys, CHECK constraints, and ON DELETE CASCADE referential integrity.\n"
                    "3. Implement dynamic SQL views to compute live course percentages without storing derived attributes.\n"
                    "4. Develop active database triggers to automatically evaluate attendance percentages and insert shortage alerts.\n"
                    "5. Implement triggers to automatically convert unexcused absences to EXCUSED status upon faculty leave approval.\n"
                    "6. Provide secure Role-Based Access Control (RBAC) consoles for Admin, Faculty, and Student users.\n"
                    "7. Deliver interactive analytical dashboards with Plotly visualizations for institutional decision support.")

    add_styled_heading(doc, "2.2 Constraints, Assumptions & Solution Strategy", 2)
    scope_data = [
        ["DBMS Engine", "MySQL 8.0 with InnoDB Storage Engine for ACID transaction compliance."],
        ["Normalization", "Mandatory compliance up to Third Normal Form (3NF) and BCNF."],
        ["Platform", "Runs locally on student workstations using open-source Python, Streamlit, and MySQL."],
        ["Exclusions", "Fees, exam grading, hostel management, and hardware biometric integrations."],
        ["Assumptions", "One attendance status per student per session; all dates follow valid chronological order."]
    ]
    add_compact_table(doc, ["Parameter", "Description"], scope_data, col_widths=[2.0, 4.7])

    add_styled_heading(doc, "2.3 Functional Requirements Specification", 2)
    fr_data = [
        ["FR-01", "Role-Based Authentication with SHA-256 password hashing.", "All", "High"],
        ["FR-02", "CRUD operations for Students, Faculty, Courses, and Sections.", "Admin", "High"],
        ["FR-03", "Configuration of ternary Course Offerings (Course + Section + Faculty).", "Admin", "High"],
        ["FR-04", "Class session scheduling and makeup class mapping.", "Faculty", "High"],
        ["FR-05", "Batch attendance marking with duplicate entry prevention.", "Faculty", "High"],
        ["FR-06", "Digital multi-day leave application submission.", "Student", "High"],
        ["FR-07", "Leave review, remarks logging, and approval/rejection.", "Faculty", "High"],
        ["FR-08", "Automatic absence excusal trigger upon leave approval.", "DB Trigger", "High"],
        ["FR-09", "Automated shortage alert generation trigger for <75% and <65%.", "DB Trigger", "High"],
        ["FR-10", "Dynamic attendance analytics, charts, and stored procedure console.", "Admin/Fac", "Medium"]
    ]
    add_compact_table(doc, ["Req ID", "Requirement Description", "Role", "Priority"], fr_data, col_widths=[0.9, 3.8, 1.1, 0.9])

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: LITERATURE REVIEW
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 3: LITERATURE REVIEW", 1)
    add_styled_heading(doc, "3.1 Relational Theory, Normalization & Active Databases", 2)
    add_body_p(doc, "Codd (1970) [3] established the mathematical foundation of relational databases, representing data as n-ary relations and operations through relational algebra. In AttendX, academic entities are structured as relational tables linked by keys. Chen (1976) [4] introduced the Entity-Relationship (ER) model, providing the visual blueprint for identifying entities, attributes, and relationships. Normalization theory by Codd (1972) [5] formalized 1NF, 2NF, and 3NF to eliminate insertion, update, and deletion anomalies. Haerder & Reuter (1983) [8] formalized ACID properties, ensuring atomic execution during batch attendance marking. Sandhu et al. (1996) [10] defined Role-Based Access Control (RBAC), applied in AttendX to strictly separate student, faculty, and administrative privileges. Furthermore, active database concepts (ECA rules) were used to implement MySQL triggers that enforce business rules directly inside the database kernel.")

    add_styled_heading(doc, "3.2 Literature Comparison & Research Gap", 2)
    lit_data = [
        ["Codd (1970) [3]", "Relational Model", "Foundation for all tables & keys.", "Theoretical; lacks application workflows."],
        ["Chen (1976) [4]", "ER Modeling", "Conceptual entity & relationship design.", "Models structure only; no trigger behavior."],
        ["Codd (1972) [5]", "Normalization", "Decomposition to 2NF & 3NF.", "Methodology; requires domain application."],
        ["Haerder (1983) [8]", "ACID Transactions", "Atomic attendance & leave commits.", "Engine recovery; lacks academic rules."],
        ["Sandhu (1996) [10]", "RBAC Model", "Admin, Faculty, Student console separation.", "Access policy; lacks trigger integration."],
        ["AttendX (This Work)", "Integrated Academic DBMS", "15 tables in 3NF, active triggers, views, RBAC.", "Full-stack institutional prototype."]
    ]
    add_compact_table(doc, ["Author / Reference", "Core Focus", "Application to AttendX", "Identified Gap Addressed"], lit_data, col_widths=[1.5, 1.4, 2.0, 1.8])

    # =========================================================================
    # CHAPTER 4: METHODOLOGY AND SYSTEM DESIGN
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 4: METHODOLOGY AND SYSTEM DESIGN", 1)
    add_styled_heading(doc, "4.1 Three-Tier System Architecture", 2)
    add_body_p(doc, "AttendX follows a decoupled Three-Tier Architecture: (1) Presentation Tier: Built with Python and Streamlit, featuring reactive role-specific dashboards and interactive Plotly visualizations. (2) Application Tier: Houses modular Python services (`auth_service`, `attendance_service`, `leave_service`) providing connection pooling, transaction orchestration, input sanitization, and SHA-256 hashing. (3) Data Tier: MySQL 8.0 (InnoDB) executing referential constraints, production views, stored procedures, and automated triggers.")

    add_styled_heading(doc, "4.2 Entity-Relationship (ER) Modeling & Cardinality", 2)
    add_body_p(doc, "The conceptual schema models 15 principal entities. Many-to-Many (M:N) relationships are formally resolved: (a) Students and Class Sessions (M:N) is decomposed into two 1:M relationships using the associative entity `ATTENDANCE` with a composite unique constraint on (session_id, student_id). (b) Students and Sections (M:N) is resolved via `STUDENT_SECTION`. (c) Courses, Sections, and Faculty form a ternary association resolved via `COURSE_OFFERINGS`.")
    
    er_data = [
        ["USERS -> STUDENTS / FACULTY", "1:1", "Unique FK user_id", "Specializes generic user account into role profile."],
        ["COURSES -> COURSE_OFFERINGS", "1:M", "FK course_id", "A course is offered across multiple sections/terms."],
        ["SECTIONS -> COURSE_OFFERINGS", "1:M", "FK section_id", "A cohort section enrolls in multiple course offerings."],
        ["FACULTY -> COURSE_OFFERINGS", "1:M", "FK faculty_id", "An instructor is assigned to teach multiple offerings."],
        ["COURSE_OFFERINGS -> CLASS_SESSIONS", "1:M", "FK offering_id", "An offering conducts multiple daily lecture sessions."],
        ["CLASS_SESSIONS -> ATTENDANCE", "1:M", "FK session_id", "A session generates attendance records for enrolled students."],
        ["STUDENTS -> ATTENDANCE", "1:M", "FK student_id", "A student receives an attendance entry per session."],
        ["CLASS_SESSIONS -> MAKEUP_SESSIONS", "1:1", "FK original_session_id", "A cancelled lecture is compensated by one makeup session."],
        ["LEAVE_TYPES -> LEAVE_APPLICATIONS", "1:M", "FK leave_type_id", "Classifies leave requests into formal policy types."],
        ["STUDENTS -> LEAVE_APPLICATIONS", "1:M", "FK student_id", "A student submits multiple leave applications."],
        ["LEAVE_APPLICATIONS -> LEAVE_APPROVALS", "1:1", "FK application_id", "An application receives a faculty approval/rejection audit record."]
    ]
    add_compact_table(doc, ["Relationship", "Card.", "Implementation", "Semantic Rule"], er_data, col_widths=[2.2, 0.6, 1.7, 2.2])

    add_styled_heading(doc, "4.3 Process Flow & Algorithmic Logic", 2)
    add_body_p(doc, "The system implements atomic batch transactions and event-driven triggers. Below is the algorithmic logic for real-time shortage evaluation implemented in MySQL:")
    code_trg = (
        "TRIGGER trg_after_attendance_insert (AFTER INSERT ON attendance):\n"
        "1. Identify offering_id from class_sessions WHERE session_id = NEW.session_id\n"
        "2. Retrieve active thresholds: min_pct (75%), crit_pct (65%) from attendance_thresholds\n"
        "3. Count total completed sessions for offering; count attended sessions for NEW.student_id\n"
        "4. Calculate attendance_percentage = (attended / total_completed) * 100\n"
        "5. IF attendance_percentage < crit_pct THEN:\n"
        "      INSERT INTO alerts (student_id, offering_id, 'CRITICAL_SHORTAGE', percentage, message)\n"
        "   ELSE IF attendance_percentage < min_pct THEN:\n"
        "      INSERT INTO alerts (student_id, offering_id, 'SHORTAGE', percentage, message)\n"
        "   END IF"
    )
    add_code_snippet(doc, code_trg)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: LOGICAL DATABASE DESIGN & IMPLEMENTATION
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 5: LOGICAL DATABASE DESIGN & IMPLEMENTATION", 1)
    add_styled_heading(doc, "5.1 Relational Schema & Functional Dependencies", 2)
    add_body_p(doc, "The logical relational schema contains 15 tables with explicit primary and foreign keys:")
    schema_summary = [
        ["users", "user_id", "username (U)", "password_hash, role, is_active, created_at"],
        ["students", "student_id", "reg_number (U), email (U)", "FK: user_id -> users; first_name, last_name, dept, semester"],
        ["faculty", "faculty_id", "faculty_code (U), email (U)", "FK: user_id -> users; first_name, last_name, dept, designation"],
        ["courses", "course_id", "course_code (U)", "course_name, credits, department"],
        ["sections", "section_id", "(name, sem, year, dept) (U)", "section_name, semester, academic_year, department"],
        ["student_section", "student_section_id", "(student, section, year) (U)", "FK: student_id, section_id; academic_year"],
        ["course_offerings", "offering_id", "(course, sec, year, sem) (U)", "FK: course_id, section_id, faculty_id; year, semester"],
        ["class_sessions", "session_id", "(offering, date, start) (U)", "FK: offering_id; session_date, start_time, end_time, status"],
        ["attendance", "attendance_id", "(session_id, student_id) (U)", "FK: session_id, student_id; status, marked_at, remarks"],
        ["leave_types", "leave_type_id", "leave_type_name (U)", "description, max_days, requires_document"],
        ["leave_applications", "application_id", "PK", "FK: student_id, leave_type_id; from_date, to_date, reason, status"],
        ["leave_approvals", "approval_id", "PK", "FK: application_id, faculty_id; approval_status, remarks, approved_at"],
        ["makeup_sessions", "makeup_id", "PK", "FK: original_session_id, makeup_session_id, created_by; reason"],
        ["alerts", "alert_id", "PK", "FK: student_id, offering_id; alert_type, percentage, message, is_resolved"],
        ["attendance_thresholds", "threshold_id", "PK", "minimum_percentage (75%), critical_percentage (65%), applicable_from"]
    ]
    add_compact_table(doc, ["Table Name", "Primary Key", "Candidate / Unique Keys", "Foreign Keys & Core Attributes"], schema_summary, col_widths=[1.5, 1.1, 1.7, 2.4])

    add_styled_heading(doc, "5.2 Normalization Analysis up to 3NF and BCNF", 2)
    add_body_p(doc, "Every table was analyzed against the three normal forms:")
    add_body_p(doc, "• 1NF: All attributes contain indivisible, atomic domain values. No multivalued composite columns or repeating groups exist.\n"
                    "• 2NF: The schema is in 1NF and contains no partial functional dependencies. In all composite candidate keys (e.g., attendance_status in attendance), attributes depend strictly on the complete composite key (session_id, student_id).\n"
                    "• 3NF & BCNF: The schema contains no transitive dependencies (X -> Y -> Z where Z is non-prime). In every non-trivial functional dependency X -> Y, determinant X is a superkey. For example, leave approval details are decoupled from leave_applications into leave_approvals, eliminating null anomalies.")

    add_styled_heading(doc, "5.3 Data Dictionary (All 15 Relational Tables)", 2)
    add_body_p(doc, "The comprehensive data dictionary across all 15 relations is consolidated below:")
    dd_data = [
        ["users.user_id", "INT", "PK, AUTO_INCREMENT", "Unique identifier for authentication credentials."],
        ["users.username", "VARCHAR(50)", "NOT NULL, UNIQUE", "User login handle."],
        ["users.role", "ENUM", "ADMIN, FACULTY, STUDENT", "Access control role."],
        ["students.student_id", "INT", "PK, AUTO_INCREMENT", "Unique student identifier."],
        ["students.user_id", "INT", "FK -> users (CASCADE)", "Reference to authentication account."],
        ["students.reg_number", "VARCHAR(20)", "NOT NULL, UNIQUE", "Institutional student roll number."],
        ["faculty.faculty_id", "INT", "PK, AUTO_INCREMENT", "Unique faculty identifier."],
        ["faculty.faculty_code", "VARCHAR(20)", "NOT NULL, UNIQUE", "Official faculty code."],
        ["courses.course_id", "INT", "PK, AUTO_INCREMENT", "Unique course catalog identifier."],
        ["courses.credits", "INT", "CHECK (credits > 0)", "Academic credit weighting."],
        ["sections.section_id", "INT", "PK, AUTO_INCREMENT", "Unique student cohort section ID."],
        ["student_section.id", "INT", "PK, AUTO_INCREMENT", "Enrollment bridge mapping student to section."],
        ["course_offerings.id", "INT", "PK, AUTO_INCREMENT", "Ternary bridge mapping Course + Section + Faculty."],
        ["class_sessions.id", "INT", "PK, AUTO_INCREMENT", "Class lecture instance; CHECK (end_time > start_time)."],
        ["attendance.id", "INT", "PK, UNIQUE(sess, stu)", "Presence record; status: PRESENT, ABSENT, LATE, EXCUSED."],
        ["leave_types.id", "INT", "PK, AUTO_INCREMENT", "Category definition: Medical, Academic, Personal, Emergency."],
        ["leave_applications.id", "INT", "PK, CHECK(from <= to)", "Multi-day leave request submitted by student."],
        ["leave_approvals.id", "INT", "PK, AUTO_INCREMENT", "Faculty review action and audit remarks."],
        ["makeup_sessions.id", "INT", "PK, CHECK(orig != make)", "Compensatory mapping of cancelled lecture to makeup."],
        ["alerts.alert_id", "INT", "PK, CHECK(pct 0-100)", "Warning alert row generated by database trigger."],
        ["thresholds.id", "INT", "PK, CHECK(min > crit)", "Policy table storing 75% min and 65% critical limits."]
    ]
    add_compact_table(doc, ["Table.Column", "Data Type", "Integrity Constraints", "Functional Description"], dd_data, col_widths=[1.7, 1.0, 1.8, 2.2])

    add_styled_heading(doc, "5.4 Triggers, Stored Procedures & Analytical Views", 2)
    add_body_p(doc, "AttendX implements native database routines: (1) `trg_after_attendance_insert`: Evaluates live percentage and generates shortage warnings. (2) `trg_after_leave_approval`: Automatically updates unexcused absences to EXCUSED status across approved leave dates. (3) `sp_batch_schedule_sessions`: Stored procedure for batch semester scheduling. (4) `sp_get_student_summary`: Computes consolidated student metrics. (5) Five Production Views: `vw_student_attendance_percentage`, `vw_attendance_shortage`, `vw_leave_history`, `vw_course_attendance_summary`, and `vw_monthly_attendance_trends`.")

    add_styled_heading(doc, "5.5 Application Modules & CRUD Operations", 2)
    crud_data = [
        ["Create", "Add Student / Schedule Session", "users, students, class_sessions", "Atomic record creation with SHA-256 password."],
        ["Read", "View Live Attendance Percentage", "vw_student_attendance_percentage", "On-the-fly percentage calculation via SQL view."],
        ["Update", "Batch Mark / Edit Attendance", "attendance, class_sessions", "Grid update; fires shortage evaluation trigger."],
        ["Update", "Faculty Leave Review", "leave_approvals, leave_applications", "Approval triggers automatic absence conversion."],
        ["Delete", "Student De-registration", "students, enrollments, attendance", "Referential integrity maintained via CASCADE."]
    ]
    add_compact_table(doc, ["Operation", "Application Feature", "Tables Affected", "Integrity Verification"], crud_data, col_widths=[0.9, 1.8, 2.0, 2.0])

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: RESULTS AND DISCUSSION
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 6: RESULTS AND DISCUSSION", 1)
    add_styled_heading(doc, "6.1 Functional Verification & Test Cases", 2)
    test_data = [
        ["TC-01", "User Authentication", "users", "Session token granted for valid role.", "Pass"],
        ["TC-02", "Session Scheduling", "class_sessions", "Session created with SCHEDULED status.", "Pass"],
        ["TC-03", "Atomic Attendance Marking", "attendance", "216 student records committed in batch.", "Pass"],
        ["TC-04", "Shortage Alert Trigger", "alerts", "Trigger generated alert for student <75%.", "Pass"],
        ["TC-05", "Makeup Class Mapping", "makeup_sessions", "Makeup class linked to cancelled session.", "Pass"],
        ["TC-06", "Leave Application", "leave_applications", "Request recorded with PENDING status.", "Pass"],
        ["TC-07", "Leave Approval Trigger", "leave_approvals", "Absence flipped to EXCUSED via trigger.", "Pass"],
        ["TC-08", "Dynamic SQL View", "vw_attendance_shortage", "Computed shortage level without anomalies.", "Pass"]
    ]
    add_compact_table(doc, ["Test ID", "Test Scenario", "Entity", "Observed Outcome", "Status"], test_data, col_widths=[0.8, 1.8, 1.6, 2.0, 0.5])

    add_styled_heading(doc, "6.2 Database Integrity & Constraint Verification", 2)
    neg_data = [
        ["NC-01", "UNIQUE(session_id, student_id)", "Insert duplicate attendance for same student.", "Rejected: Error 1062 (Duplicate entry).", "Pass"],
        ["NC-02", "CHECK(end_time > start_time)", "Session end_time before start_time.", "Rejected: Error 3819 (Check violated).", "Pass"],
        ["NC-03", "CHECK(from_date <= to_date)", "Leave from_date after to_date.", "Rejected: Error 3819 (Check violated).", "Pass"],
        ["NC-04", "CHECK(original != makeup)", "Makeup class mapped to itself.", "Rejected: Error 3819 (Check violated).", "Pass"],
        ["NC-05", "ON DELETE CASCADE", "Delete student with attendance records.", "Success: All child rows cleanly removed.", "Pass"]
    ]
    add_compact_table(doc, ["Test ID", "Constraint Under Test", "Applied Negative Input", "Database Response", "Status"], neg_data, col_widths=[0.8, 1.9, 1.8, 1.7, 0.5])

    add_styled_heading(doc, "6.3 Analytical Performance Graphs & Interpretation", 2)
    add_body_p(doc, "From the seed dataset (65 class sessions, 216 attendance records), analytical views generated clear institutional findings: (1) Course Average Standing: Computer Networks (IT302) achieved the highest attendance at 93.8%, while Operating Systems (CS302) sat at 75.0%, highlighting subjects needing academic counseling. (2) Shortage Severity Distribution: 73.7% of students maintain good standing (>=75%), 15.8% sit in the warning shortage band (65%–75%), and 10.5% are in critical shortage (<65%). (3) Leave Categorization: Medical leaves represented 50% of submissions, with emergency leaves lacking documentation being systematically rejected.")

    add_styled_heading(doc, "6.4 Comparison with Project Objectives", 2)
    obj_data = [
        ["1. 3NF Relational Architecture", "15 normalized tables; zero update or deletion anomalies.", "Achieved"],
        ["2. Database-Level Integrity", "Composite keys, foreign keys with CASCADE, and CHECK rules.", "Achieved"],
        ["3. Automated Percentage Views", "Live view queries eliminate stored derived attributes.", "Achieved"],
        ["4. Active Shortage Alert Trigger", "trg_after_attendance_insert inserts warnings automatically.", "Achieved"],
        ["5. Active Absence Excusal Trigger", "trg_after_leave_approval flips past unexcused absences.", "Achieved"],
        ["6. Role-Based Access Control", "Segregated Admin, Faculty, and Student consoles with SHA-256.", "Achieved"],
        ["7. Interactive Data Analytics", "Plotly visual dashboards with live SQL stored procedure console.", "Achieved"]
    ]
    add_compact_table(doc, ["Stated Objective", "Achieved Technical Deliverable", "Status"], obj_data, col_widths=[2.1, 3.8, 0.8])

    # =========================================================================
    # CHAPTER 7: CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    add_styled_heading(doc, "CHAPTER 7: CONCLUSION AND FUTURE SCOPE", 1)
    add_styled_heading(doc, "7.1 Summary & Key Learning Outcomes", 2)
    add_body_p(doc, "The AttendX project successfully replaced manual attendance registers with an automated, 3NF-normalized relational database management system. Key academic learning outcomes include: (1) Conceptual-to-Relational Modeling: Decomposing Many-to-Many relationships into associative entities with composite keys. (2) Mathematical Normalization: Proving schema adherence to 1NF, 2NF, 3NF, and BCNF. (3) Active Database Automation: Implementing MySQL triggers and stored procedures to enforce institutional business rules directly at the data tier.")

    add_styled_heading(doc, "7.2 Limitations & Future Enhancements", 2)
    add_body_p(doc, "Limitations: The current system operates locally with simulated session credentials and does not directly connect to physical campus RFID turnstiles.\n"
                    "Future Enhancements: (1) Hardware RFID/Biometric Integration: Logging presence directly via IoT gateways; (2) SMS Notification Gateway: Automated alerts to guardians via Twilio; (3) Predictive Machine Learning Analytics: Early forecasting of at-risk students.")

    # =========================================================================
    # REFERENCES & APPENDICES
    # =========================================================================
    add_styled_heading(doc, "REFERENCES", 1)
    refs = [
        "[1] B. Atkin and A. Brooks, Total Facility Management, 4th ed. Chichester, U.K.: Wiley-Blackwell, 2015.",
        "[2] I. Lopes et al., 'Requirements specification of a computerized maintenance management system,' Procedia CIRP, vol. 52, pp. 268–273, 2016.",
        "[3] E. F. Codd, 'A relational model of data for large shared data banks,' Commun. ACM, vol. 13, no. 6, pp. 377–387, Jun. 1970.",
        "[4] P. P. Chen, 'The entity-relationship model—Toward a unified view of data,' ACM Trans. Database Syst., vol. 1, no. 1, pp. 9–36, Mar. 1976.",
        "[5] E. F. Codd, 'Further normalization of the data base relational model,' in Data Base Systems, Prentice-Hall, 1972, pp. 33–64.",
        "[6] R. Elmasri and S. B. Navathe, Fundamentals of Database Systems, 7th ed. Hoboken, NJ, USA: Pearson, 2016.",
        "[7] A. Silberschatz, H. F. Korth, and S. Sudarshan, Database System Concepts, 7th ed. McGraw-Hill, 2019.",
        "[8] T. Haerder and A. Reuter, 'Principles of transaction-oriented database recovery,' ACM Comput. Surv., vol. 15, no. 4, pp. 287–317, 1983.",
        "[9] D. F. Ferraiolo and D. R. Kuhn, 'Role-based access controls,' in Proc. 15th NIST-NCSC Nat. Comput. Security Conf., pp. 554–563, 1992.",
        "[10] R. S. Sandhu et al., 'Role-based access control models,' IEEE Computer, vol. 29, no. 2, pp. 38–47, 1996.",
        "[11] J. H. Saltzer and M. D. Schroeder, 'The protection of information in computer systems,' Proc. IEEE, vol. 63, no. 9, pp. 1278–1308, 1975.",
        "[12] OWASP Foundation, 'OWASP Top 10:2021 Security Risks,' https://owasp.org/Top10/, 2026.",
        "[13] R. T. Fielding, 'Architectural styles and the design of network-based software architectures,' Ph.D. dissertation, UC Irvine, 2000.",
        "[14] Oracle Corporation, 'MySQL 8.0 Reference Manual: Triggers & Stored Programs,' https://dev.mysql.com/doc/, 2026.",
        "[15] Python Software Foundation, 'Python Database API Specification v2.0 (PEP 249),' https://peps.python.org/, 2026."
    ]
    for r in refs:
        add_body_p(doc, r)

    add_styled_heading(doc, "APPENDICES: CORE SQL DDL SCRIPT", 1)
    ddl_summary = (
        "-- AttendX Schema DDL (Extract of Primary Core Tables)\n"
        "CREATE TABLE users (user_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, role ENUM('ADMIN','FACULTY','STUDENT') NOT NULL);\n"
        "CREATE TABLE students (student_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, registration_number VARCHAR(20) UNIQUE NOT NULL, first_name VARCHAR(50) NOT NULL, email VARCHAR(100) UNIQUE NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE);\n"
        "CREATE TABLE courses (course_id INT AUTO_INCREMENT PRIMARY KEY, course_code VARCHAR(20) UNIQUE NOT NULL, course_name VARCHAR(100) NOT NULL, credits INT CHECK(credits > 0));\n"
        "CREATE TABLE course_offerings (offering_id INT AUTO_INCREMENT PRIMARY KEY, course_id INT NOT NULL, section_id INT NOT NULL, faculty_id INT NOT NULL, UNIQUE(course_id, section_id, academic_year, semester));\n"
        "CREATE TABLE class_sessions (session_id INT AUTO_INCREMENT PRIMARY KEY, offering_id INT NOT NULL, session_date DATE NOT NULL, start_time TIME NOT NULL, end_time TIME NOT NULL, CHECK(end_time > start_time));\n"
        "CREATE TABLE attendance (attendance_id INT AUTO_INCREMENT PRIMARY KEY, session_id INT NOT NULL, student_id INT NOT NULL, attendance_status ENUM('PRESENT','ABSENT','LATE','EXCUSED') NOT NULL, UNIQUE(session_id, student_id));\n"
        "CREATE TABLE leave_applications (application_id INT AUTO_INCREMENT PRIMARY KEY, student_id INT NOT NULL, leave_type_id INT NOT NULL, from_date DATE NOT NULL, to_date DATE NOT NULL, CHECK(from_date <= to_date));\n"
        "CREATE TABLE leave_approvals (approval_id INT AUTO_INCREMENT PRIMARY KEY, application_id INT NOT NULL, faculty_id INT NOT NULL, approval_status ENUM('APPROVED','REJECTED') NOT NULL);\n"
        "CREATE TABLE alerts (alert_id INT AUTO_INCREMENT PRIMARY KEY, student_id INT NOT NULL, offering_id INT NOT NULL, alert_type ENUM('SHORTAGE','CRITICAL_SHORTAGE') NOT NULL, attendance_percentage DECIMAL(5,2));"
    )
    add_code_snippet(doc, ddl_summary)

    output_docx = "docs/AttendX_PBL_Report_Final.docx"
    doc.save(output_docx)
    print(f"Optimal report written to: {output_docx}")

if __name__ == "__main__":
    build_perfect_report()
