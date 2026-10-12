# Woxsen University
## School of Technology
### DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING

---

# PROJECT BASED LEARNING REPORT
### Course Name: Database Management Systems
### Academic Year: 2026–27

## PROJECT TITLE:
# DESIGN AND IMPLEMENTATION OF A DATABASE MANAGEMENT SYSTEM FOR STUDENT ATTENDANCE AND LEAVE APPROVAL MANAGEMENT SYSTEM (AttendX)

---

**Submitted by:**
- **Name:** Yasheswar Kataria
- **Roll Number:** 25WU0101156
- **Program:** B.Tech – Computer Science and Engineering
- **Section:** CSE - Panthers
- **Institution:** Woxsen University, Hyderabad

**Under the Guidance of:**
- **Faculty Guide:** Dr. Sahithi Chennamadhavuni
- **Designation:** Associate Professor
- **Department:** Department of Computer Science and Engineering, School of Technology

**Date of Submission:** October, 2026

---
\pagebreak

## CERTIFICATE

This is to certify that the Project-Based Learning report entitled **"DESIGN AND IMPLEMENTATION OF A DATABASE MANAGEMENT SYSTEM FOR STUDENT ATTENDANCE AND LEAVE APPROVAL MANAGEMENT SYSTEM (AttendX)"** is a bonafide work carried out by **Mr. Yasheswar Kataria (Roll No: 25WU0101156)**, student of B.Tech in Computer Science and Engineering at Woxsen University, during the Academic Year 2026–27, in partial fulfillment of the academic requirements for the course **Database Management Systems (DBMS)** under my supervision and guidance.

<br><br><br>

______________________________________  
**(Dr. Sahithi Chennamadhavuni)**  
Associate Professor  
Department of Computer Science and Engineering  
School of Technology, Woxsen University  

---
\pagebreak

## DECLARATION

I hereby declare that the project entitled **"DESIGN AND IMPLEMENTATION OF A DATABASE MANAGEMENT SYSTEM FOR STUDENT ATTENDANCE AND LEAVE APPROVAL MANAGEMENT SYSTEM (AttendX)"**, submitted to the School of Technology, Woxsen University, Hyderabad, for the Project-Based Learning evaluation in the course **Database Management Systems**, is an authentic record of original work carried out by me under the guidance of **Dr. Sahithi Chennamadhavuni**.

I confirm that this work has not been previously submitted in part or full for the award of any other degree, diploma, or academic certificate in this or any other institution. All technical concepts, algorithms, literature references, and datasets used have been properly acknowledged and cited in accordance with university academic standards.

I further declare that the content adheres strictly to academic integrity and ethical guidelines.

<br><br>

**Place:** Hyderabad  
**Date:** 12th October 2026  

<br><br>

______________________________________  
**Signature of the Candidate**  
**Name:** Yasheswar Kataria  
**Roll Number:** 25WU0101156  
**Program:** B.Tech – Computer Science and Engineering  

---
\pagebreak

## ACKNOWLEDGEMENT

I express my deepest gratitude and sincere appreciation to my esteemed faculty guide, **Dr. Sahithi Chennamadhavuni**, Associate Professor, Department of Computer Science and Engineering, School of Technology, Woxsen University, for her invaluable mentorship, constructive feedback, technical guidance, and constant encouragement throughout the design and realization of this Project-Based Learning endeavor. Her emphasis on rigorous mathematical normalization (3NF/BCNF), schema constraints, transaction safety, and clean software architecture fundamentally shaped the quality of this work.

I extend my heartfelt thanks to the **Dean and the Faculty Members** of the School of Technology, Woxsen University, for cultivating an exceptional learning environment, providing state-of-the-art laboratory infrastructure, and fostering academic inquiry through experiential Project-Based Learning.

I also extend my gratitude to my peers and colleagues for their productive feedback during the testing of the application consoles, and to the open-source software engineering communities behind **MySQL 8.0, Python, Streamlit, and Plotly**, whose comprehensive documentation and tooling served as an indispensable foundation.

Finally, I am profoundly grateful to my parents and family for their unconditional support, patience, and motivation, without which this academic milestone would not have been possible.

<br><br>

**Yasheswar Kataria**  
Roll Number: 25WU0101156  

---
\pagebreak

## ABSTRACT

Higher education institutions depend heavily on continuous and accurate attendance monitoring to evaluate student performance, meet university regulatory standards, and maintain academic discipline. Traditionally, attendance and leave management have relied on physical registers, fragmented spreadsheets, and manual paper-based leave slips. These legacy channels suffer from critical structural weaknesses, including lost records, unauthorized proxy attendance, slow aggregation, arithmetic inaccuracies in percentage calculations, lack of auditability, and delayed leave processing. Most critically, institutions fail to provide real-time warning alerts to students at risk of attendance shortages before end-semester examinations.

This report presents the design and full-stack implementation of **AttendX (Student Attendance and Leave Approval Management System)**, a robust, database-centered software solution developed to digitalize the complete lifecycle of university presence tracking and leave governance. The system is engineered on a foundational **MySQL 8.0 (InnoDB)** relational database composed of **15 core tables normalized up to the Third Normal Form (3NF) and Boyce-Codd Normal Form (BCNF)**. The database schema strictly guarantees referential integrity, entity integrity, and business rules through composite foreign keys, `CHECK` constraints, `UNIQUE` key definitions, and `ON DELETE CASCADE` triggers.

Beyond standard data storage, the database acts as an active computing engine: custom **database views** compute dynamic course-level attendance percentages; **automated triggers** (`trg_after_attendance_insert`) detect attendance shortage thresholds ($<75\%$ and $<65\%$) and dynamically generate shortage alert records; a dedicated trigger (`trg_after_leave_approval`) automatically transforms past unexcused absences into `EXCUSED` records across approved date intervals; and **stored procedures** allow batch session scheduling and analytical evaluation. A multi-console web application built with **Python, Streamlit, and Plotly** provides strictly segregated role-based access control (RBAC) across three distinct actors: **Admin, Faculty, and Student**. The prototype was rigorously tested against positive, negative, and edge test cases, proving that database-enforced constraints eliminate data anomalies and provide institutional-grade transparency.

**Keywords:** Database Management Systems (DBMS), Relational Database, Normalization (3NF/BCNF), MySQL 8.0, Triggers, Stored Procedures, Role-Based Access Control (RBAC), Attendance Management, Streamlit.

---
\pagebreak

## TABLE OF CONTENTS

- **Certificate** ............................................................................................................ ii
- **Declaration** ........................................................................................................... iii
- **Acknowledgement** ................................................................................................. iv
- **Abstract** ................................................................................................................ v
- **List of Tables** ........................................................................................................ viii
- **List of Figures** ....................................................................................................... ix
- **List of Acronyms** ................................................................................................... x

### 1. INTRODUCTION ................................................................................................ 1
- 1.1 Background ........................................................................................................ 1
- 1.2 Motivation and Relevance to Real-World Problem ................................................ 2
- 1.3 Scope and Organisation of the Report ................................................................. 3

### 2. PROBLEM STATEMENT AND OBJECTIVES ....................................................... 4
- 2.1 Problem Definition .............................................................................................. 4
- 2.2 Objectives .......................................................................................................... 4
- 2.3 Constraints and Assumptions ............................................................................... 5
- 2.4 Proposed Solution Strategy ................................................................................. 6

### 3. LITERATURE REVIEW ....................................................................................... 7
- 3.1 Data Modeling and Relational Algebra ................................................................ 7
- 3.2 Database Normalization and Anomaly Mitigation .................................................. 8
- 3.3 Transactions, ACID Properties, and Database-Level Integrity ................................ 8
- 3.4 Access Control, Authentication, and Security Principles ....................................... 9
- 3.5 Automated Database Triggers and Active Databases ............................................ 10
- 3.6 Comparison of Reviewed Literature and Research Gap ........................................ 11

### 4. METHODOLOGY AND SYSTEM DESIGN ........................................................ 12
- 4.1 Overall Three-Tier System Architecture ............................................................. 12
- 4.2 Entity-Relationship (ER) Modeling ....................................................................... 13
- 4.3 Entity and Relationship Cardinality Analysis ....................................................... 14
- 4.4 Process Flow & Lifecycle of Attendance and Leaves ............................................. 16
- 4.5 Algorithmic Logic and Stored Routine Design ...................................................... 17
- 4.6 Tools and Technologies ...................................................................................... 19
- 4.7 Use-Case and Data Flow Design (DFD Level-0 & Level-1) ..................................... 20

### 5. LOGICAL DATABASE DESIGN & IMPLEMENTATION ...................................... 22
- 5.1 Relational Schema .............................................................................................. 22
- 5.2 Functional Dependencies (FD) ............................................................................. 23
- 5.3 Normalization Analysis up to 3NF and BCNF ......................................................... 25
- 5.4 Data Dictionary (All 15 Core Relations) ............................................................... 27
- 5.5 Database Triggers and Stored Procedures Implementation ..................................... 33
- 5.6 Analytical Views Implementation ......................................................................... 35
- 5.7 Representative SQL Queries (Joins, Aggregates, Subqueries) ................................. 36
- 5.8 Application Development & Module-to-Database Mapping ................................... 38
- 5.9 CRUD Operations and Business Rule Verification ................................................ 39
- 5.10 Dataset Description & Seed Population ............................................................. 40
- 5.11 Application Screens & Output Verification .......................................................... 41

### 6. RESULTS AND DISCUSSION ........................................................................... 45
- 6.1 Functional Verification & End-to-End Test Cases ................................................. 45
- 6.2 Database Integrity & Constraint Verification ....................................................... 47
- 6.3 Analytical Performance Graphs & Interpretations ................................................. 48
- 6.4 Comparison with Project Objectives .................................................................... 50

### 7. CONCLUSION AND FUTURE SCOPE ............................................................... 52
- 7.1 Summary ............................................................................................................ 52
- 7.2 Key Academic Learning Outcomes ..................................................................... 52
- 7.3 Limitations and Future Enhancements ................................................................ 53

### REFERENCES ....................................................................................................... 54
### APPENDICES ........................................................................................................ 56
- Appendix A: Complete Database DDL Script (`database.sql`) ................................... 56
- Appendix B: Procedures, Triggers, and Analytical Views ........................................... 57
- Appendix C: Representative Analytical Queries (`queries.sql`) ................................. 58

---
\pagebreak

## LIST OF TABLES

| Table No. | Table Title | Page No. |
| :--- | :--- | :--- |
| Table 2.1 | Scope and Boundary Assumptions | 5 |
| Table 2.2 | Proposed Solution Strategy & Modules | 6 |
| Table 2.3 | Functional Requirements Specification | 6 |
| Table 3.1 | Comparison of Reviewed Works and AttendX System | 11 |
| Table 4.1 | Entity, Identifier, and Purpose Summary | 13 |
| Table 4.2 | Relationship Cardinality and Bridge Implementation | 15 |
| Table 4.3 | Tools, Libraries, and Technology Stack | 19 |
| Table 5.1 | Relational Schema of AttendX (15 Tables) | 22 |
| Table 5.2 | Summary of Normalization Status (1NF to 3NF/BCNF) | 27 |
| Table 5.3 to 5.17 | Data Dictionary for Tables 1 to 15 | 28–32 |
| Table 5.18 | Summary of Active Triggers and Stored Procedures | 34 |
| Table 5.19 | Summary of Production Database Analytical Views | 35 |
| Table 5.20 | Application Module to Database Mapping | 38 |
| Table 5.21 | CRUD Operations Evidence Matrix | 39 |
| Table 5.22 | Business Rules, Validation, and Constraint Mapping | 40 |
| Table 5.23 | Seed Dataset Breakdown across Core Entities | 41 |
| Table 6.1 | End-to-End Lifecycle Test Execution Results | 46 |
| Table 6.2 | Negative Constraint and Integrity Test Cases | 47 |
| Table 6.3 | Achievement of Project Objectives Evaluation | 50 |

---

## LIST OF FIGURES

| Figure No. | Figure Title | Page No. |
| :--- | :--- | :--- |
| Figure 4.1 | Three-Tier Architecture of AttendX System | 12 |
| Figure 4.2 | Complete Entity-Relationship Diagram (Crow's Foot Notation) | 14 |
| Figure 4.3 | Flowchart of Attendance Recording and Leave Approval Lifecycles | 16 |
| Figure 4.4 | Use-Case Diagram for Admin, Faculty, and Student Actors | 20 |
| Figure 4.5 | Level-1 Data Flow Diagram (DFD) of AttendX | 21 |
| Figure 5.1 | Representative DDL Execution in MySQL 8.0 Command Line | 33 |
| Figure 5.2 | Admin Analytical Dashboard with Summary Metrics | 41 |
| Figure 5.3 | Course-wise Attendance Analytics and Interactive Distribution | 42 |
| Figure 5.4 | Faculty Console: Session Scheduling & Real-Time Presence Marking | 42 |
| Figure 5.5 | Faculty Leave Processing and Decision Interface | 43 |
| Figure 5.6 | Student Console: Live Percentage Tracking & Threshold Bars | 43 |
| Figure 5.7 | Student Digital Leave Application Interface | 44 |
| Figure 5.8 | Shortage Alerts Generated Automatically by Database Trigger | 44 |
| Figure 6.1 | Course Attendance Distribution (Average % Across Courses) | 48 |
| Figure 6.2 | Attendance Shortage Severity Ratio (Critical vs Warning vs Good) | 49 |
| Figure 6.3 | Leave Application Distribution Categorized by Leave Type | 49 |

---

## LIST OF ACRONYMS

| Acronym | Expansion |
| :--- | :--- |
| **DBMS** | Database Management System |
| **RDBMS** | Relational Database Management System |
| **SQL** | Structured Query Language |
| **DDL** | Data Definition Language |
| **DML** | Data Manipulation Language |
| **ER / ERD** | Entity-Relationship / Entity-Relationship Diagram |
| **PK** | Primary Key |
| **FK** | Foreign Key |
| **1NF / 2NF / 3NF** | First / Second / Third Normal Form |
| **BCNF** | Boyce-Codd Normal Form |
| **FD** | Functional Dependency |
| **ACID** | Atomicity, Consistency, Isolation, Durability |
| **RBAC** | Role-Based Access Control |
| **CRUD** | Create, Read, Update, Delete |
| **DFD** | Data Flow Diagram |
| **API** | Application Programming Interface |
| **UI / UX** | User Interface / User Experience |
| **PBL** | Project-Based Learning |

---
\pagebreak

# CHAPTER 1: INTRODUCTION

## 1.1 Background
In contemporary universities and professional educational institutions, the academic schedule is highly structured. An institution accommodates thousands of students across dozens of disciplines, multiple academic years, and specialized sections. Courses are delivered through scheduled lectures, laboratory sessions, and tutorial hours conducted by designated faculty members. Under university academic guidelines, student attendance is not merely a formality; it directly correlates with academic performance, practical skill development, and examination eligibility. Most accredited universities enforce a strict regulatory threshold (typically a minimum of 75% attendance) as an absolute prerequisite for appearing in final end-semester examinations.

Despite the digital transformation of modern campuses, attendance recording and leave governance in many universities remain remarkably manual or fragmented. Faculty members routinely record attendance on physical paper registers or isolated Excel spreadsheets. Paper registers are vulnerable to damage, loss, illegibility, and proxy marking. Excel sheets stored on individual faculty laptops create severe data silos where no central authority can verify consistency. Furthermore, when a student falls ill or attends an approved academic conference, the leave application process requires physical paperwork—obtaining signatures from mentors, department chairs, and subject faculty. This paper trail is frequently delayed, lost, or never reconciled against the daily attendance registers. Consequently, consolidated attendance statistics are only computed at the very end of the semester, leaving at-risk students completely unaware of severe attendance shortages until hall tickets are withheld.

The relational model pioneered by Edgar F. Codd [3] provides the mathematical and architectural foundation necessary to resolve these inefficiencies. By modeling entities such as students, faculty, sections, course offerings, and attendance records as normalized relations linked by primary and foreign keys, an institution can guarantee absolute data integrity, eliminate redundancy, and support concurrent multi-user transactions. Building on this theoretical framework, this project designs and implements **AttendX**, a full-featured, database-centered Student Attendance and Leave Approval Management System.

## 1.2 Motivation and Relevance to Real-World Problem
The practical motivation for this project stems from recurring institutional challenges observed in campus management:
1. **Arithmetic Inaccuracies & Redundant Entry**: Manually tallying hundreds of attendance sheets creates human calculation errors. A single missed mark or mathematical miscount can unfairly disqualify a student from writing their semester exams.
2. **Absence of Real-Time Shortage Visibility**: In manual systems, students receive zero feedback regarding their standing. When attendance percentages are computed dynamically by an active database, automated shortage warnings can be triggered weeks in advance, enabling corrective intervention.
3. **Disjointed Leave Reconciliation**: Physical leave approval slips often remain in departmental drawers, leaving faculty registers marked as "Absent". A synchronized relational database ensures that upon leave approval, attendance records are immediately audited and excused at the database layer.
4. **Disorganized Makeup Lectures**: When university classes are cancelled due to holidays or faculty emergencies, scheduling makeup sessions and tracking student attendance across those compensation classes is poorly documented.
5. **Administrative Transparency & Auditing**: Academic deans and department heads require high-level analytical visibility over course averages, faculty workloads, and student absence trends without asking faculty to manually generate reports.

From an academic perspective, this project serves as a comprehensive capstone applying every core principle taught in a university Database Management Systems curriculum: Entity-Relationship modeling [4], functional dependency analysis, Third Normal Form (3NF) and BCNF normalization [5], composite keys, referential integrity with cascading constraints, complex SQL joins, grouping and aggregate subqueries, analytical database views, stored procedures, and event-driven database triggers [8].

## 1.3 Scope and Organisation of the Report
The developed system encapsulates the end-to-end lifecycle of academic attendance and leave processing:
- Master academic entity configuration (Students, Faculty, Courses, Sections, Term Course Offerings).
- Class session scheduling and daily attendance recording.
- Makeup lecture creation explicitly linked to original cancelled sessions.
- Dynamic percentage calculation via database views.
- Digital multi-tier leave application submission, tracking, and faculty approval.
- Automated threshold-driven shortage alert generation via database triggers.
- Multi-dimensional analytics, reporting, and SQL consoles.

The remainder of this report is organized as follows:
- **Chapter 2** defines the problem, measurable objectives, constraints, assumptions, and functional requirements.
- **Chapter 3** conducts a literature review on data modeling, normalization, transactions, RBAC, and active triggers, concluding with a research gap analysis.
- **Chapter 4** describes the methodology, three-tier architecture, complete Entity-Relationship diagram, process flowcharts, algorithms, and data flow diagrams.
- **Chapter 5** presents the comprehensive logical database design (relational schema, functional dependencies, 3NF/BCNF proof, complete 15-table data dictionary, triggers, stored procedures, analytical views, and Streamlit application implementation).
- **Chapter 6** details results, end-to-end test cases, database constraint verification, and performance chart interpretations.
- **Chapter 7** concludes the report with academic learning outcomes and future enhancements.

---
\pagebreak

# CHAPTER 2: PROBLEM STATEMENT AND OBJECTIVES

## 2.1 Problem Definition
Traditional university attendance and leave management processes rely on disconnected paper registers, disparate spreadsheets, and manual leave request letters. This environment exhibits five fundamental failures:
1. **Data Fragmentation and Redundancy**: Student and course information is duplicated across multiple registers, resulting in data inconsistency and update anomalies.
2. **Computational Latency & Inaccurate Aggregations**: Consolidated attendance percentages are calculated manually at the end of the semester, frequently introducing human computational errors.
3. **Communication Gap in Leave Approvals**: Physical leave slips are rarely updated in faculty daily registers, causing legitimate leaves to remain recorded as unexcused absences.
4. **Absence of Proactive Shortage Alerts**: Students have no visibility into their real-time attendance percentage and receive no systematic warning before falling below statutory minimums (75%).
5. **Lack of Referential Traceability**: Makeup classes scheduled to compensate for cancelled lectures are not formally linked to the original class, making attendance audit trails impossible.

**Formal Problem Statement:**  
*To design and implement a secure, centralized, 3NF-normalized Relational Database Management System (AttendX) that automates the end-to-end lifecycle of student attendance tracking, class session scheduling, digital leave approvals, and threshold-based shortage alerting, while strictly enforcing data integrity, referential constraints, and transactional consistency at the database tier.*

## 2.2 Objectives
The project is executed to fulfill the following measurable objectives:
1. **Centralize Institutional Records in a 3NF Relational Schema**: Architect a unified relational schema comprising 15 normalized tables eliminating partial and transitive dependencies.
2. **Enforce Database-Level Referential and Domain Integrity**: Enforce constraints via Primary Keys, Composite Foreign Keys with cascading actions (`ON DELETE CASCADE`), `UNIQUE` constraints (preventing duplicate attendance per student per session), and `CHECK` constraints (validating date orders and percentages).
3. **Automate Attendance Percentage Computation via Views**: Implement production database views that dynamically compute attended sessions, total sessions, and percentages without storing derived data.
4. **Implement Active Database Triggers for Threshold Shortage Alerting**: Deploy triggers that listen to attendance inserts and automatically generate warning records in `alerts` if a student falls below predefined thresholds (75% minimum, 65% critical).
5. **Automate Absence Reconciliation upon Leave Approval**: Implement database triggers that automatically update past absences to `EXCUSED` status upon faculty leave approval.
6. **Provide Role-Segregated Application Interfaces (RBAC)**: Develop dedicated, secure consoles for Admin, Faculty, and Student users with password hashing.
7. **Support Administrative Decision Making via Data Analytics**: Provide dynamic visualizations for course averages, shortage severity ratios, and monthly trends.

## 2.3 Constraints and Assumptions
**Table 2.1: Scope and Boundary Assumptions**
| Parameter | Classification | Description |
| :--- | :--- | :--- |
| **DBMS Engine** | Constraint | MySQL 8.0 utilizing the InnoDB storage engine for transactional safety. |
| **Normalization** | Constraint | Every table must strictly satisfy 1NF, 2NF, and 3NF/BCNF. |
| **Hardware** | Constraint | Runs locally on a standard workstation using open-source Python and MySQL. |
| **Out of Scope** | Exclusion | Campus fee collection, examination grading, hostel allocation, and biometric/RFID hardware. |
| **User Identity** | Assumption | Every user has a unique username and belongs to a designated role (`ADMIN`, `FACULTY`, `STUDENT`). |
| **Attendance Rule** | Assumption | Exactly one attendance status (`PRESENT`, `ABSENT`, `LATE`, `EXCUSED`) exists per student per session. |
| **Time Standard** | Assumption | All timestamps use server clock time; sessions cannot have `end_time <= start_time`. |

## 2.4 Proposed Solution Strategy & Functional Requirements
**Table 2.2: Proposed Solution Strategy & Modules**
| Module / Actor | Core Functional Responsibilities |
| :--- | :--- |
| **Admin Module** | Master CRUD on Courses, Sections, Faculty, Students, and Ternary Course Offerings; Global analytical reporting; Stored procedure execution. |
| **Faculty Module** | Session creation; Makeup session scheduling; Grid-based attendance marking and updating; Review and decision on pending leave applications. |
| **Student Module** | Live attendance percentage viewing; Session history filtering; Digital leave application submission; Dynamic shortage alert notifications. |

**Table 2.3: Functional Requirements Specification**
| Req. ID | Description | Primary Actor | Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | Secure authentication with role-based session isolation and SHA-256 password hashing. | All Users | High |
| **FR-02** | Master maintenance of academic courses, sections, faculty profiles, and student enrollments. | Admin | High |
| **FR-03** | Configuration of ternary `course_offerings` mapping Course + Section + Faculty. | Admin | High |
| **FR-04** | Creation and lifecycle management of daily class sessions (`SCHEDULED`, `COMPLETED`, `CANCELLED`). | Faculty | High |
| **FR-05** | Batch attendance marking with prevention of duplicate attendance records via composite unique keys. | Faculty | High |
| **FR-06** | Scheduling makeup lectures explicitly mapped to original cancelled sessions. | Faculty | Medium |
| **FR-07** | Submission of leave requests with date range verification and document requirements. | Student | High |
| **FR-08** | Review, approval, or rejection of student leave applications with faculty audit remarks. | Faculty | High |
| **FR-09** | Automatic conversion of unexcused absences to `EXCUSED` upon leave approval via database triggers. | Database Engine | High |
| **FR-10** | Automated evaluation of attendance percentages and insertion of shortage alerts. | Database Engine | High |
| **FR-11** | Interactive graphical dashboards showing course standings, shortage ratios, and monthly trends. | Admin / Faculty | Medium |

---
\pagebreak

# CHAPTER 3: LITERATURE REVIEW

## 3.1 Data Modeling and Relational Algebra
The mathematical foundation of relational databases was established by E. F. Codd in his seminal 1970 paper, *"A Relational Model of Data for Large Shared Data Banks"* [3]. Codd introduced the representation of data as mathematical n-ary relations (tables) composed of tuples (rows) and attributes (columns). The core contribution was the principle of **data independence**, which decouples logical database schemas from underlying physical storage mechanisms. Operations are executed using relational algebra operators—selection ($\sigma$), projection ($\pi$), cartesian product ($\times$), join ($\bowtie$), and set operations. 

In AttendX, the relational model serves as the foundational structure: all academic entities (students, class sessions, leave requests) are formally defined as relations linked by referential keys. However, Codd’s initial theoretical paper addressed structural representations and left application concerns, such as authentication, authorization, and workflow triggers, to implementation systems.

In 1976, Peter P. Chen introduced the **Entity-Relationship (ER) Model** [4] as a semantic modeling technique that bridges human perceptions of real-world enterprise logic and logical database design. Chen defined entities, attributes, and relationship cardinalities (1:1, 1:N, M:N), providing an intuitive graphical notation. In AttendX, the conceptual design was synthesized using Chen's model: entities such as `STUDENTS`, `COURSES`, and `CLASS_SESSIONS` were established before mapping them into physical tables. Crucially, Chen's model highlighted that Many-to-Many (M:N) relationships cannot be physically implemented in relational databases without decomposing them into two One-to-Many (1:N) relationships through associative bridge entities.

## 3.2 Database Normalization and Anomaly Mitigation
Following his introduction of the relational model, Codd addressed data redundancy and operational anomalies in his 1972 work, *"Further Normalization of the Data Base Relational Model"* [5]. He formalized the Second Normal Form (2NF) and Third Normal Form (3NF) based on the concept of **Functional Dependencies (FD)**. Normalization is the formal mathematical decomposition of relations to ensure that all non-key attributes depend strictly on the candidate key, the whole candidate key, and nothing but the candidate key.

As detailed by Elmasri and Navathe [6] and Silberschatz et al. [7], unnormalized database schemas exhibit three catastrophic anomalies:
- **Insertion Anomalies**: The inability to record certain attributes without artificially inserting unrelated data (e.g., being unable to add a new Course until a student enrolls in it).
- **Update Anomalies**: Data inconsistencies caused by duplicating the same fact across thousands of records (e.g., updating a faculty member's email address in 500 session rows).
- **Deletion Anomalies**: The unintended loss of essential master data when deleting transactional records (e.g., deleting a semester's attendance records inadvertently deleting the course definition).

AttendX applies formal functional dependency decomposition across all 15 tables to achieve full compliance with 3NF and Boyce-Codd Normal Form (BCNF), ensuring complete elimination of these anomalies.

## 3.3 Transactions, ACID Properties, and Database-Level Integrity
In multi-user database environments, concurrent operations must maintain structural consistency. Haerder and Reuter (1983) formalized transaction management by defining the **ACID** properties [8]:
- **Atomicity**: Guarantees that a suite of database modifications either executes entirely or rolls back completely.
- **Consistency**: Ensures transitions occur only between valid schema states, preserving all integrity constraints.
- **Isolation**: Prevents concurrent transactions from interfering with one another.
- **Durability**: Ensures committed modifications survive system failures.

In AttendX, ACID transactions are paramount. For instance, when faculty submit an attendance roster for 60 students, the database executes an atomic transaction: 60 rows are inserted, session statuses are updated, and if any single operation violates a constraint, the entire transaction rolls back. MySQL's InnoDB storage engine provides full ACID transaction support, row-level locking, and crash recovery.

## 3.4 Access Control, Authentication, and Security Principles
Role-Based Access Control (RBAC) was formalized by Ferraiolo and Kuhn (1992) [9] and expanded by Sandhu et al. (1996) [10]. Under RBAC, system permissions are assigned to specific roles rather than individual users, and users acquire privileges based on their assigned role. This architecture aligns with university structures, where distinct roles exist:
- **Admin**: System configuration and global audits.
- **Faculty**: Academic execution and approval authority.
- **Student**: Personal record tracking and self-service requests.

Saltzer and Schroeder (1975) formulated fundamental security principles for computing systems [11], including the **Principle of Least Privilege** (each user should operate using the minimum privileges necessary) and **Complete Mediation** (every access attempt must be checked). AttendX implements RBAC by enforcing role checks at the server tier and hashing credentials with SHA-256 to protect against credential disclosure, adhering to OWASP security guidelines [12].

## 3.5 Automated Database Triggers and Active Databases
Traditional relational databases are passive—they store data and execute queries on demand. Modern database research highlights the power of **Active Databases**, which use event-condition-action (ECA) rules implemented as database triggers. A trigger executes automatically when specific DML operations (`INSERT`, `UPDATE`, `DELETE`) occur.

Database triggers provide several advantages over application-level code:
- **Tamper-Evident Business Logic**: Logic executed by a database trigger cannot be bypassed by bugs, unauthorized scripts, or direct SQL execution in administrative clients.
- **Immediate Data Consistency**: Triggers execute within the active transaction context, ensuring that derived updates occur atomically with the triggering statement.

AttendX employs active database triggers to calculate real-time percentages, generate shortage alerts, and reconcile absences upon leave approvals directly within the MySQL database engine.

## 3.6 Comparison of Reviewed Literature and Research Gap
**Table 3.1: Comparison of Reviewed Works and AttendX System**
| Author / Standard | Theoretical Focus | Relevance to AttendX | Research / Practical Gap |
| :--- | :--- | :--- | :--- |
| **Codd (1970) [3]** | Relational Model | Foundation for all tables, primary keys, and foreign keys. | Pure theory; lacks application workflows and security mechanisms. |
| **Chen (1976) [4]** | ER Modeling | Structural design of entities and cardinalities. | Models structure only; does not define behavior, triggers, or workflows. |
| **Codd (1972) [5]** | Normalization (2NF/3NF) | Decomposition eliminating partial and transitive dependencies. | Mathematical method; requires adaptation to domain-specific entities. |
| **Haerder & Reuter (1983) [8]** | ACID Transactions | Guarantees atomic attendance marking and leave updates. | Focuses on engine recovery; does not model institutional business rules. |
| **Sandhu et al. (1996) [10]** | Role-Based Access Control | Segregation of Admin, Faculty, and Student consoles. | Models policies; requires integration with database session management. |
| **Fielding (2000) [13]** | Three-Tier Architecture | Decoupling of presentation, application, and database tiers. | Architectural style; requires concrete technological implementation. |
| **AttendX (This Work)** | **Integrated Academic DBMS** | **Full 15-table 3NF schema, active triggers, views, stored procedures, RBAC.** | **Addresses gap by delivering an active, automated, full-stack university system.** |

---
\pagebreak

# CHAPTER 4: METHODOLOGY AND SYSTEM DESIGN

## 4.1 Overall Three-Tier System Architecture
AttendX is engineered following a clean **Three-Tier Architecture** [13], depicted in Figure 4.1. This decouples presentation, business logic, and database management, ensuring high modularity, maintainability, and security.

```
+-----------------------------------------------------------------------------------+
|                        1. PRESENTATION TIER (Web Browser)                         |
|   +-----------------------+ +-----------------------+ +-----------------------+   |
|   |     ADMIN PORTAL      | |    FACULTY PORTAL     | |    STUDENT PORTAL     |   |
|   | Global Master CRUD    | | Session Scheduling    | | Standing & Progress   |   |
|   | Analytics & Reports   | | Attendance Grid       | | Leave Applications    |   |
|   | Stored Proc Console   | | Leave Approvals       | | Shortage Alerts       |   |
|   +-----------------------+ +-----------------------+ +-----------------------+   |
|              Interactive Visualizations & Charts powered by Plotly                |
+-----------------------------------------------------------------------------------+
                                          |
                                          | HTTPS / UI Events (Session Token Auth)
                                          v
+-----------------------------------------------------------------------------------+
|                   2. APPLICATION TIER (Python / Business Logic)                   |
|   +---------------------------------------------------------------------------+   |
|   | Core Routing & Navigation Engine (`app.py`)                               |   |
|   +---------------------------------------------------------------------------+   |
|   +-------------------+ +-------------------+ +-------------------+ +---------+   |
|   |   Auth Service    | |Attendance Service | |   Leave Service   | | Alert   |   |
|   | Role Verification | | Atomic Recording  | | Multi-Day Workflow| | Service |   |
|   +-------------------+ +-------------------+ +-------------------+ +---------+   |
|   +---------------------------------------------------------------------------+   |
|   | MySQL Database Connection Pool & Transaction Manager (`config/database.py`)|   |
|   | Parameterized Prepared Statements (SQL Injection Mitigation)              |   |
|   +---------------------------------------------------------------------------+   |
+-----------------------------------------------------------------------------------+
                                          |
                                          | Parameterized SQL over Port 3306
                                          v
+-----------------------------------------------------------------------------------+
|                     3. DATA TIER (MySQL 8.0 InnoDB Storage Engine)                |
|   +------------------------------------+ +------------------------------------+   |
|   | Core Relational Schema (15 Tables) | | Production Database Views (5 Views)|   |
|   | - 3NF / BCNF Certified Design      | | - Dynamic Attendance Percentages   |   |
|   | - Primary & Foreign Key Integrity  | | - Real-time Shortage Evaluation    |   |
|   | - CHECK, UNIQUE, DEFAULT Rules     | | - Course Attendance Summaries      |   |
|   +------------------------------------+ +------------------------------------+   |
|   +------------------------------------+ +------------------------------------+   |
|   | Active Database Triggers           | | Stored Procedures                  |   |
|   | - `trg_after_attendance_insert`    | | - `sp_batch_schedule_sessions`     |   |
|   | - `trg_after_leave_approval`       | | - `sp_get_student_summary`         |   |
|   +------------------------------------+ +------------------------------------+   |
+-----------------------------------------------------------------------------------+
```
**Figure 4.1: Three-Tier Architecture of AttendX System**

- **Presentation Tier**: Built using Python and Streamlit, augmented with custom CSS and Plotly. Users interact with dedicated consoles based on their authenticated role.
- **Application Tier**: Contains business logic split into modular services (`auth_service`, `attendance_service`, `leave_service`, `report_service`). Manages database connection pooling, handles transactions, hashes credentials, and sanitizes input.
- **Data Tier**: MySQL 8.0 server using the InnoDB engine. Enforces data integrity, executes triggers, maintains views, and runs stored procedures directly inside the database kernel.

## 4.2 Entity-Relationship (ER) Modeling
Figure 4.2 presents the complete conceptual Entity-Relationship Diagram for AttendX, using standard Crow's Foot notation.

```
       +---------------+                     +---------------+
       |     USERS     |                     |    COURSES    |
       +---------------+                     +---------------+
        |1           |1                       |1
        |            |                        |
        |has         |has                     |offered as
        |            |                        |
        v0..1        v0..1                    v1..*
+---------------+ +---------------+     +-----------------------+     +---------------+
|   STUDENTS    | |    FACULTY    |     |   COURSE_OFFERINGS    |<----+   SECTIONS    |
+---------------+ +---------------+     +-----------------------+1   *+---------------+
 |1            |1  |1           |1       |1                        1|
 |             |   |            |        |conducts                  |
 |enrolled     |   |teaches     |        |                          |contains
 |             |   |            |        v1..*                      |
 v1..*         |   |            |   +-------------------+           |
+-------------+|   |            |   |  CLASS_SESSIONS   |           |
|STUDENT_SECT ||   |            |   +-------------------+           |
+-------------+|   |            |    |1        |1                   |
               |   |            |    |records  |compensated by      |
               |   |            |    |         |                    |
               |   |            |    v1..*     v0..1                |
               |   |            |   +----------++----------+        |
               |   |            |   |ATTENDANCE||MAKEUP_SES|        |
               |   |            |   +----------++----------+        |
               |   |            |               |                   |
               |   |            +---------------+assigned to        |
               |   |                            |                   |
               |   |                            v                   |
               |   |                   +------------------+         |
               |   |                   |    FACULTY       |         |
               |   |                   +------------------+         |
               |   |                                                |
               |   |submits                                         |
               |   v1..*                                            |
               |  +--------------------+1       1+-----------------+|
               |  | LEAVE_APPLICATIONS |<--------|   LEAVE_TYPES   ||
               |  +--------------------+categoriz+-----------------+|
               |   |1                                               |
               |   |receives                                        |
               |   v0..1                                            |
               |  +--------------------+1       1+-----------------+|
               |  |  LEAVE_APPROVALS   |-------->|     FACULTY     ||
               |  +--------------------+processed+-----------------+|
               |                                                    |
               |receives                                            |
               v1..*                                                |
              +------------------------+1       1+-----------------+|
              |         ALERTS         |<--------| COURSE_OFFERINGS||
              +------------------------+triggered+------------------+
```
**Figure 4.2: Complete Entity-Relationship Diagram of AttendX (Crow's Foot Notation)**

## 4.3 Entity and Relationship Cardinality Analysis
**Table 4.1: Entity, Identifier, and Purpose Summary**
| Entity Name | Primary Key | Conceptual Purpose in AttendX |
| :--- | :--- | :--- |
| **USERS** | `user_id` | Core authentication entity containing login credentials and role assignments. |
| **STUDENTS** | `student_id` | Contains student profile information, registration numbers, and departments. |
| **FACULTY** | `faculty_id` | Stores academic faculty profiles, designations, and departments. |
| **COURSES** | `course_id` | Master catalog of university courses, course codes, and credits. |
| **SECTIONS** | `section_id` | Cohort sections categorized by department, semester, and academic year. |
| **STUDENT_SECTION** | `student_section_id` | Associative bridge entity mapping Students to Sections (M:N). |
| **COURSE_OFFERINGS**| `offering_id` | Ternary associative entity connecting Course + Section + Faculty. |
| **CLASS_SESSIONS** | `session_id` | Individual lecture or lab session instances conducted on specific dates. |
| **ATTENDANCE** | `attendance_id` | Associative bridge entity recording student presence per session (M:N). |
| **LEAVE_TYPES** | `leave_type_id` | Master leave categories (Medical, Academic, Personal, Emergency). |
| **LEAVE_APPLICATIONS**| `application_id` | Multi-day leave requests submitted by students. |
| **LEAVE_APPROVALS** | `approval_id` | Official decision and audit log recorded by faculty for leave requests. |
| **MAKEUP_SESSIONS** | `makeup_id` | Links newly scheduled makeup lectures to original cancelled sessions. |
| **ALERTS** | `alert_id` | Dynamic shortage notifications generated for students at risk. |
| **ATTENDANCE_THRESHOLDS**| `threshold_id` | System-wide policy rules defining minimum (75%) and critical (65%) percentages. |

### Resolution of Many-to-Many (M:N) Relationships:
1. **Students and Class Sessions (M:N $\to$ 1:N + 1:N)**:
   - One student attends many class sessions. One class session is attended by many students.
   - **Resolution**: Resolved via the associative entity `ATTENDANCE`. Each row stores foreign keys `session_id` and `student_id`, along with the `attendance_status`.
   - **Constraint**: `UNIQUE(session_id, student_id)` guarantees that no student can have multiple attendance records for the same session.
2. **Students and Sections (M:N $\to$ 1:N + 1:N)**:
   - Over an academic career, a student enrolls in multiple sections, and a section contains multiple students.
   - **Resolution**: Resolved via `STUDENT_SECTION` with foreign keys referencing `student_id` and `section_id`.
3. **Courses, Sections, and Faculty (Ternary Association)**:
   - A course is offered to multiple sections and can be taught by different faculty members.
   - **Resolution**: Resolved via `COURSE_OFFERINGS`, acting as a ternary relationship that creates a distinct offering instance with unique scheduling and session dependencies.

**Table 4.2: Relationship Cardinality and Implementation Mapping**
| Entity 1 | Relationship | Entity 2 | Cardinality | Implementation Mechanism |
| :--- | :---: | :--- | :---: | :--- |
| **USERS** | specializes | **STUDENTS** | 1:1 | `students.user_id` $\to$ `users.user_id` (Unique FK) |
| **USERS** | specializes | **FACULTY** | 1:1 | `faculty.user_id` $\to$ `users.user_id` (Unique FK) |
| **COURSES** | offered as | **COURSE_OFFERINGS** | 1:M | `course_offerings.course_id` $\to$ `courses.course_id` |
| **SECTIONS** | scheduled in | **COURSE_OFFERINGS** | 1:M | `course_offerings.section_id` $\to$ `sections.section_id` |
| **FACULTY** | assigned to | **COURSE_OFFERINGS** | 1:M | `course_offerings.faculty_id` $\to$ `faculty.faculty_id` |
| **STUDENTS** | enrolled via | **STUDENT_SECTION** | 1:M | `student_section.student_id` $\to$ `students.student_id` |
| **SECTIONS** | populated via | **STUDENT_SECTION** | 1:M | `student_section.section_id` $\to$ `sections.section_id` |
| **COURSE_OFFERINGS** | conducts | **CLASS_SESSIONS** | 1:M | `class_sessions.offering_id` $\to$ `course_offerings.offering_id` |
| **CLASS_SESSIONS** | logged in | **ATTENDANCE** | 1:M | `attendance.session_id` $\to$ `class_sessions.session_id` |
| **STUDENTS** | marked in | **ATTENDANCE** | 1:M | `attendance.student_id` $\to$ `students.student_id` |
| **CLASS_SESSIONS** | compensated by | **MAKEUP_SESSIONS** | 1:1 | `makeup_sessions.original_session_id` $\to$ `class_sessions.session_id` |
| **LEAVE_TYPES** | classifies | **LEAVE_APPLICATIONS**| 1:M | `leave_applications.leave_type_id` $\to$ `leave_types.leave_type_id`|
| **STUDENTS** | submits | **LEAVE_APPLICATIONS**| 1:M | `leave_applications.student_id` $\to$ `students.student_id` |
| **LEAVE_APPLICATIONS**| reviewed in | **LEAVE_APPROVALS** | 1:1 | `leave_approvals.application_id` $\to$ `leave_applications.application_id` |
| **FACULTY** | decides | **LEAVE_APPROVALS** | 1:M | `leave_approvals.faculty_id` $\to$ `faculty.faculty_id` |
| **STUDENTS** | receives | **ALERTS** | 1:M | `alerts.student_id` $\to$ `students.student_id` |

## 4.4 Process Flow of Attendance and Leave Governance
```
   [FACULTY ATTENDANCE LIFECYCLE]                      [STUDENT LEAVE APPROVAL LIFECYCLE]
                +                                                    +
                |                                                    |
                v                                                    v
     +--------------------+                               +--------------------+
     | Faculty Selects    |                               | Student Logs in to |
     | Assigned Offering  |                               | Portal             |
     +--------------------+                               +--------------------+
                |                                                    |
                v                                                    v
     +--------------------+                               +--------------------+
     | Creates Class      |                               | Submits Leave App  |
     | Session (Date/Time)|                               | (Type, Dates, Text)|
     +--------------------+                               +--------------------+
                |                                                    |
                v                                                    v
     +--------------------+                               +--------------------+
     | Marks Attendance   |                               | DB Validates Range |
     | (PRESENT/ABSENT)   |                               | CHECK(from <= to)  |
     +--------------------+                               +--------------------+
                |                                                    | Status: PENDING
                v                                                    v
     +--------------------+                               +--------------------+
     | Atomic Transaction |                               | Faculty Reviews in |
     | Commits to DB      |                               | Approval Console   |
     +--------------------+                               +--------------------+
                |                                                    |
                v                                        +-----------+-----------+
     +--------------------+                              |                       |
     | Database Trigger   |                              v                       v
     | Fires Automatically|                        [REJECTED]               [APPROVED]
     +--------------------+                              |                       |
                |                                        v                       v
        +-------+-------+                         +--------------+      +----------------+
        |               |                         | App Status   |      | App Status     |
        v               v                         | Set REJECTED |      | Set APPROVED   |
   [>= 75%]        [< 75%]                        +--------------+      +----------------+
        |               |                                                        |
        v               v                                                        v
   No Action      Trigger Inserts                                       +----------------+
                  Shortage Alert                                        | DB Trigger     |
                        |                                               | Fires: Absences|
                        v                                               | Converted to   |
                  +-------------+                                       | EXCUSED        |
                  | Student     |                                       +----------------+
                  | Alert Banner|
                  +-------------+
```
**Figure 4.3: Process Flowchart of Attendance Marking and Leave Workflows**

## 4.5 Algorithmic Logic and Stored Routine Design

### Algorithm 1: User Authentication & Role-Based Authorization
```text
INPUT: username, plain_password
OUTPUT: user_record OR authentication_failure

1. query <- "SELECT user_id, username, password_hash, role, is_active FROM users WHERE username = :username"
2. user <- execute_query(query, [username], fetch_one=TRUE)
3. IF user IS NULL OR user.is_active != TRUE THEN
4.    RETURN Error("Invalid username or account inactive")
5. END IF
6. computed_hash <- SHA256(plain_password)
7. IF computed_hash != user.password_hash THEN
8.    RETURN Error("Invalid credentials")
9. END IF
10. session.set("authenticated", TRUE)
11. session.set("user_id", user.user_id)
12. session.set("role", user.role)
13. IF user.role == 'STUDENT' THEN
14.    student_info <- execute_query("SELECT student_id, first_name FROM students WHERE user_id = :id", [user.user_id])
15.    session.set("student_id", student_info.student_id)
16. ELSE IF user.role == 'FACULTY' THEN
17.    faculty_info <- execute_query("SELECT faculty_id, first_name FROM faculty WHERE user_id = :id", [user.user_id])
18.    session.set("faculty_id", faculty_info.faculty_id)
19. END IF
20. REDIRECT to corresponding Role Dashboard
```

### Algorithm 2: Atomic Batch Attendance Submission
```text
INPUT: session_id, student_attendance_list [(student_id, status, remarks)]
OUTPUT: transaction_status

1. BEGIN TRANSACTION
2. TRY:
3.    FOR EACH (student_id, status, remarks) IN student_attendance_list DO:
4.       query <- "INSERT INTO attendance (session_id, student_id, attendance_status, remarks) 
                   VALUES (:sess_id, :stu_id, :status, :remarks)
                   ON DUPLICATE KEY UPDATE attendance_status = :status, remarks = :remarks"
5.       execute_query(query, [session_id, student_id, status, remarks])
6.    END FOR
7.    UPDATE class_sessions SET session_status = 'COMPLETED' WHERE session_id = :session_id
8.    COMMIT TRANSACTION
9.    RETURN Success("Attendance marked atomically. Triggers fired.")
10. CATCH Exception AS err:
11.   ROLLBACK TRANSACTION
12.   RETURN Error("Attendance commit failed. Rolled back: " + err.message)
```

### Algorithm 3: Real-Time Shortage Evaluation Trigger (`trg_after_attendance_insert`)
```text
EVENT: AFTER INSERT ON attendance
FOR EACH ROW:
1. offering_id <- (SELECT offering_id FROM class_sessions WHERE session_id = NEW.session_id)
2. min_threshold, crit_threshold <- (SELECT minimum_percentage, critical_percentage 
                                     FROM attendance_thresholds ORDER BY applicable_from DESC LIMIT 1)
3. total_completed <- (SELECT COUNT(*) FROM class_sessions 
                       WHERE offering_id = offering_id AND session_status = 'COMPLETED')
4. attended <- (SELECT COUNT(*) FROM attendance a 
                JOIN class_sessions cs ON a.session_id = cs.session_id
                WHERE cs.offering_id = offering_id AND a.student_id = NEW.student_id 
                  AND cs.session_status = 'COMPLETED' 
                  AND a.attendance_status IN ('PRESENT', 'EXCUSED', 'LATE'))
5. IF total_completed > 0 THEN:
6.    pct <- (attended / total_completed) * 100.0
7.    IF pct < crit_threshold THEN:
8.       IF NOT EXISTS (SELECT 1 FROM alerts WHERE student_id = NEW.student_id 
                        AND offering_id = offering_id AND alert_type = 'CRITICAL_SHORTAGE' AND is_resolved = FALSE):
9.          INSERT INTO alerts (student_id, offering_id, alert_type, attendance_percentage, message)
            VALUES (NEW.student_id, offering_id, 'CRITICAL_SHORTAGE', pct, 
                    CONCAT('Critical shortage: ', ROUND(pct, 1), '% (Threshold: ', crit_threshold, '%)'))
10.      END IF
11.   ELSE IF pct < min_threshold THEN:
12.      IF NOT EXISTS (SELECT 1 FROM alerts WHERE student_id = NEW.student_id 
                        AND offering_id = offering_id AND alert_type = 'SHORTAGE' AND is_resolved = FALSE):
13.         INSERT INTO alerts (student_id, offering_id, alert_type, attendance_percentage, message)
            VALUES (NEW.student_id, offering_id, 'SHORTAGE', pct, 
                    CONCAT('Attendance warning: ', ROUND(pct, 1), '% (Minimum: ', min_threshold, '%)'))
14.      END IF
15.   END IF
16. END IF
```

## 4.6 Tools and Technologies
**Table 4.3: Tools, Libraries, and Technology Stack**
| Layer / Category | Technology | Version | Justification / Role |
| :--- | :--- | :--- | :--- |
| **Relational DBMS** | MySQL Server | 8.0.36+ | Industrial-strength RDBMS providing ACID transactions, foreign keys, triggers, and views. |
| **Storage Engine** | InnoDB | MySQL 8.0 | Default engine supporting row-level locking, foreign key integrity, and MVCC concurrency. |
| **Development IDE** | Antigravity IDE | Latest | Full-stack programming environment, Git version control, and shell execution. |
| **Programming Language**| Python | 3.12+ | Core application logic, database connection pooling, and web routing. |
| **Web Interface** | Streamlit | 1.36+ | Framework delivering reactive multi-page dashboards. |
| **Data Analytics** | Pandas | 2.2+ | Tabular manipulation, schema matrix handling, and aggregation. |
| **Data Visualization** | Plotly Express | 5.22+ | Interactive charts (bar, pie, line) with tooltips. |
| **Database Connector** | `mysql-connector-python`| 8.4+ | Database driver supporting parameterized queries. |
| **Security Module** | Python `hashlib` | Built-in | Cryptographic SHA-256 password hashing. |

## 4.7 Use-Case and Data Flow Design
```
                                 +--------------------------------+
                                 |          AttendX SYSTEM        |
                                 +--------------------------------+
           ADMIN                 |                                |
             +------------------>|  (Manage Courses & Sections)   |
             |                   |                                |
             +------------------>|  (Manage Students & Faculty)   |
             |                   |                                |
             +------------------>|  (Configure Course Offerings)  |
             |                   |                                |
             +------------------>|  (Execute Stored Procedures)   |
                                 |                                |
          FACULTY                |                                |
             +------------------>|  (Schedule Class Sessions)     |
             |                   |                                |
             +------------------>|  (Batch Mark/Edit Attendance)  |
             |                   |                                |
             +------------------>|  (Schedule Makeup Sessions)    |
             |                   |                                |
             +------------------>|  (Approve/Reject Leave Apps)   |
                                 |                                |
          STUDENT                |                                |
             +------------------>|  (View Dynamic Percentage)     |
             |                   |                                |
             +------------------>|  (Filter Session History)      |
             |                   |                                |
             +------------------>|  (Submit Leave Applications)   |
             |                   |                                |
             +------------------>|  (Receive Shortage Alerts)     |
                                 +--------------------------------+
```
**Figure 4.4: Use-Case Diagram for AttendX System**

```
 [STUDENT / FACULTY / ADMIN]
              |
              | 1. Credentials
              v
     +-------------------+       Read/Write      +-------------------+
     | 1.0 AUTHENTICATE  |<=====================>| D1: USERS         |
     +-------------------+                       +-------------------+
              | Validated Session
              |
      +-------+---------------------------------------+
      |                                               |
      v                                               v
+-------------------+                           +-------------------+
| 2.0 MANAGE MASTER |                           | 3.0 SCHEDULE &    |
| DATA & OFFERINGS  |                           | RECORD ATTENDANCE |
+-------------------+                           +-------------------+
      |                                               |
      | Writes                                        | Inserts Attendance
      v                                               v
+-----------------------------+                 +-----------------------------+
| D2: COURSES, SECTIONS,      |                 | D3: CLASS_SESSIONS,         |
| COURSE_OFFERINGS, STUDENTS  |                 | ATTENDANCE                  |
+-----------------------------+                 +-----------------------------+
                                                      |
                                                      | After Insert Event
                                                      v
                                                +-----------------------------+
                                                | 4.0 TRIGGER SHORTAGE ALERTS |
                                                +-----------------------------+
                                                      |
                                                      | Generates
                                                      v
                                                +-----------------------------+
                                                | D4: ALERTS                  |
                                                +-----------------------------+
                                                      ^
                                                      | Reads Standing
                                                      |
                                                +-----------------------------+
                                                | 5.0 LEAVE GOVERNANCE &      |
                                                | ABSENCE RECONCILIATION      |
                                                +-----------------------------+
                                                 Writes | Reads
                                                        v
                                                +-----------------------------+
                                                | D5: LEAVE_APPLICATIONS,     |
                                                | LEAVE_APPROVALS, LEAVE_TYPES|
                                                +-----------------------------+
```
**Figure 4.5: Level-1 Data Flow Diagram (DFD) of AttendX**

---
\pagebreak

# CHAPTER 5: LOGICAL DATABASE DESIGN & IMPLEMENTATION

## 5.1 Relational Schema
The logical relational schema derived from the ER design consists of **15 core relations**, detailed below.  
*Notation: Primary keys are indicated by **PK**, foreign keys by **FK**, and unique attributes by **(U)**.*

**Table 5.1: Relational Schema of AttendX (15 Relations)**
1. **`users`** (**user_id [PK]**, username [U], password_hash, role, is_active, created_at)
2. **`students`** (**student_id [PK]**, *user_id [FK $\to$ users]*, registration_number [U], first_name, last_name, email [U], phone, department, semester, created_at)
3. **`faculty`** (**faculty_id [PK]**, *user_id [FK $\to$ users]*, faculty_code [U], first_name, last_name, email [U], department, designation)
4. **`courses`** (**course_id [PK]**, course_code [U], course_name, credits, department)
5. **`sections`** (**section_id [PK]**, section_name, semester, academic_year, department, *(section_name, semester, academic_year, department) [U]*)
6. **`student_section`** (**student_section_id [PK]**, *student_id [FK $\to$ students]*, *section_id [FK $\to$ sections]*, academic_year, *(student_id, section_id, academic_year) [U]*)
7. **`course_offerings`** (**offering_id [PK]**, *course_id [FK $\to$ courses]*, *section_id [FK $\to$ sections]*, *faculty_id [FK $\to$ faculty]*, academic_year, semester, *(course_id, section_id, academic_year, semester) [U]*)
8. **`class_sessions`** (**session_id [PK]**, *offering_id [FK $\to$ course_offerings]*, session_date, start_time, end_time, topic_covered, session_status, created_at, *(offering_id, session_date, start_time) [U]*)
9. **`attendance`** (**attendance_id [PK]**, *session_id [FK $\to$ class_sessions]*, *student_id [FK $\to$ students]*, attendance_status, marked_at, remarks, *(session_id, student_id) [U]*)
10. **`leave_types`** (**leave_type_id [PK]**, leave_type_name [U], description, max_days, requires_document)
11. **`leave_applications`** (**application_id [PK]**, *student_id [FK $\to$ students]*, *leave_type_id [FK $\to$ leave_types]*, from_date, to_date, reason, application_status, submitted_at)
12. **`leave_approvals`** (**approval_id [PK]**, *application_id [FK $\to$ leave_applications]*, *faculty_id [FK $\to$ faculty]*, approval_status, remarks, approved_at)
13. **`makeup_sessions`** (**makeup_id [PK]**, *original_session_id [FK $\to$ class_sessions]*, *makeup_session_id [FK $\to$ class_sessions]*, reason, *created_by [FK $\to$ faculty]*, created_at)
14. **`alerts`** (**alert_id [PK]**, *student_id [FK $\to$ students]*, *offering_id [FK $\to$ course_offerings]*, alert_type, attendance_percentage, message, is_resolved, generated_at)
15. **`attendance_thresholds`** (**threshold_id [PK]**, minimum_percentage, critical_percentage, applicable_from)

## 5.2 Functional Dependencies (FD)
To prove that our schema is normalized up to 3NF and BCNF, we identify the non-trivial functional dependencies for each core table:

1. **`users`**:
   - $\text{user\_id} \to \text{username}, \text{password\_hash}, \text{role}, \text{is\_active}, \text{created\_at}$
   - $\text{username} \to \text{user\_id}, \text{password\_hash}, \text{role}, \text{is\_active}, \text{created\_at}$
2. **`students`**:
   - $\text{student\_id} \to \text{user\_id}, \text{registration\_number}, \text{first\_name}, \text{last\_name}, \text{email}, \text{phone}, \text{department}, \text{semester}, \text{created\_at}$
   - $\text{registration\_number} \to \text{student\_id}, \dots$
   - $\text{email} \to \text{student\_id}, \dots$
3. **`faculty`**:
   - $\text{faculty\_id} \to \text{user\_id}, \text{faculty\_code}, \text{first\_name}, \text{last\_name}, \text{email}, \text{department}, \text{designation}$
   - $\text{faculty\_code} \to \text{faculty\_id}, \dots$
   - $\text{email} \to \text{faculty\_id}, \dots$
4. **`courses`**:
   - $\text{course\_id} \to \text{course\_code}, \text{course\_name}, \text{credits}, \text{department}$
   - $\text{course\_code} \to \text{course\_id}, \text{course\_name}, \text{credits}, \text{department}$
5. **`sections`**:
   - $\text{section\_id} \to \text{section\_name}, \text{semester}, \text{academic\_year}, \text{department}$
   - $\{\text{section\_name}, \text{semester}, \text{academic\_year}, \text{department}\} \to \text{section\_id}$
6. **`student_section`**:
   - $\text{student\_section\_id} \to \text{student\_id}, \text{section\_id}, \text{academic\_year}$
   - $\{\text{student\_id}, \text{section\_id}, \text{academic\_year}\} \to \text{student\_section\_id}$
7. **`course_offerings`**:
   - $\text{offering\_id} \to \text{course\_id}, \text{section\_id}, \text{faculty\_id}, \text{academic\_year}, \text{semester}$
   - $\{\text{course\_id}, \text{section\_id}, \text{academic\_year}, \text{semester}\} \to \text{offering\_id}, \text{faculty\_id}$
8. **`class_sessions`**:
   - $\text{session\_id} \to \text{offering\_id}, \text{session\_date}, \text{start\_time}, \text{end\_time}, \text{topic\_covered}, \text{session\_status}, \text{created\_at}$
   - $\{\text{offering\_id}, \text{session\_date}, \text{start\_time}\} \to \text{session\_id}, \dots$
9. **`attendance`**:
   - $\text{attendance\_id} \to \text{session\_id}, \text{student\_id}, \text{attendance\_status}, \text{marked\_at}, \text{remarks}$
   - $\{\text{session\_id}, \text{student\_id}\} \to \text{attendance\_id}, \text{attendance\_status}, \text{marked\_at}, \text{remarks}$
10. **`leave_types`**:
    - $\text{leave\_type\_id} \to \text{leave\_type\_name}, \text{description}, \text{max\_days}, \text{requires\_document}$
    - $\text{leave\_type\_name} \to \text{leave\_type\_id}, \dots$
11. **`leave_applications`**:
    - $\text{application\_id} \to \text{student\_id}, \text{leave\_type\_id}, \text{from\_date}, \text{to\_date}, \text{reason}, \text{application\_status}, \text{submitted\_at}$
12. **`leave_approvals`**:
    - $\text{approval\_id} \to \text{application\_id}, \text{faculty\_id}, \text{approval\_status}, \text{remarks}, \text{approved\_at}$
13. **`makeup_sessions`**:
    - $\text{makeup\_id} \to \text{original\_session\_id}, \text{makeup\_session\_id}, \text{reason}, \text{created\_by}, \text{created\_at}$
14. **`alerts`**:
    - $\text{alert\_id} \to \text{student\_id}, \text{offering\_id}, \text{alert\_type}, \text{attendance_percentage}, \text{message}, \text{is\_resolved}, \text{generated\_at}$
15. **`attendance_thresholds`**:
    - $\text{threshold\_id} \to \text{minimum\_percentage}, \text{critical\_percentage}, \text{applicable\_from}$

## 5.3 Normalization Analysis up to 3NF and BCNF

### 1. Verification of First Normal Form (1NF)
A table is in 1NF if all attribute values are atomic and there are no repeating groups.
- In AttendX, attributes such as student names are decomposed into atomic columns (`first_name`, `last_name`).
- Date and time ranges are split into discrete columns (`start_time`, `end_time`, `from_date`, `to_date`).
- Multi-valued attributes (e.g., student course enrollments) are placed in separate relations (`student_section`, `attendance`).
- Therefore, every table satisfies 1NF.

### 2. Verification of Second Normal Form (2NF)
A table is in 2NF if it is in 1NF and contains no **partial functional dependencies**—that is, no non-prime attribute depends on a proper subset of a composite candidate key.
- Tables with single-column surrogate primary keys (`users`, `students`, `courses`, `class_sessions`, etc.) are automatically free from partial dependencies because their primary keys contain no subsets.
- In associative tables with candidate composite keys (`attendance`, `course_offerings`, `student_section`):
  - In `attendance`, the candidate key is $\{\text{session\_id}, \text{student\_id}\}$. The attribute $\text{attendance\_status}$ depends on the *combination* of the session and the student; it cannot be determined by the student alone or the session alone.
  - In `course_offerings`, the assignment of a faculty member depends on the complete combination of Course, Section, Semester, and Year.
- Therefore, every table satisfies 2NF.

### 3. Verification of Third Normal Form (3NF)
A table is in 3NF if it is in 2NF and contains no **transitive dependencies** ($X \to Y$ and $Y \to Z$, where non-key attribute $Z$ depends on non-key attribute $Y$).
- In `students`, department details are stored as a simple string attribute, while student credentials are decomposed into the `users` table via foreign key `user_id`. Non-key attributes depend directly on `student_id`.
- In `course_offerings`, course details (`credits`, `course_name`) are not duplicated; they reside in `courses` and are referenced by `course_id`.
- In `leave_applications`, approval details are not stored within the application row, avoiding `NULL` values prior to evaluation and preventing transitive dependencies on faculty approvers. Approvals are isolated in `leave_approvals`.
- Therefore, every table satisfies 3NF.

### 4. Verification of Boyce-Codd Normal Form (BCNF)
A table is in BCNF if for every non-trivial functional dependency $X \to Y$, the determinant $X$ is a **superkey**.
- In every relation in AttendX, the left-hand side determinant of every functional dependency is either the Primary Key or a declared Candidate Key with a `UNIQUE` constraint.
- Therefore, the AttendX schema satisfies Boyce-Codd Normal Form (BCNF).

**Table 5.2: Summary of Normalization Status (1NF to 3NF/BCNF)**
| Relation Name | 1NF | 2NF | 3NF | BCNF | Normalization Rationale |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `users` | ✓ | ✓ | ✓ | ✓ | Atomic credentials; determinant `user_id` and `username` are superkeys. |
| `students` | ✓ | ✓ | ✓ | ✓ | Registration and email are unique candidate keys; no transitive FDs. |
| `faculty` | ✓ | ✓ | ✓ | ✓ | Single-attribute PK; faculty code and email are unique candidate keys. |
| `courses` | ✓ | ✓ | ✓ | ✓ | Course code is unique; credit attributes depend strictly on course key. |
| `sections` | ✓ | ✓ | ✓ | ✓ | Composite uniqueness prevents duplicate cohorts; no partial dependencies. |
| `student_section` | ✓ | ✓ | ✓ | ✓ | M:N associative entity; enrollment attributes depend on the full composite key. |
| `course_offerings`| ✓ | ✓ | ✓ | ✓ | Ternary associative table; foreign keys isolate course, section, and faculty facts. |
| `class_sessions` | ✓ | ✓ | ✓ | ✓ | Timing constraints validated; session facts depend strictly on `session_id`. |
| `attendance` | ✓ | ✓ | ✓ | ✓ | Composite unique key $\{\text{session}, \text{student}\}$; status depends on both keys. |
| `leave_types` | ✓ | ✓ | ✓ | ✓ | Master policy category; no multi-valued or dependent attributes. |
| `leave_applications`|✓| ✓ | ✓ | ✓ | Separates request details from approval actions, eliminating transitive nulls. |
| `leave_approvals` | ✓ | ✓ | ✓ | ✓ | Dedicated audit relation preserving historical decisions per application. |
| `makeup_sessions` | ✓ | ✓ | ✓ | ✓ | Dual foreign keys to sessions ensure referential integrity for compensations. |
| `alerts` | ✓ | ✓ | ✓ | ✓ | Generated event log; foreign keys link student and offering context. |
| `attendance_thresholds`|✓|✓| ✓ | ✓ | System policy relation; independent scalar thresholds. |

## 5.4 Data Dictionary (All 15 Core Relations)

### Table 5.3: Data Dictionary for `users`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `user_id` | INT | PK, AUTO_INCREMENT | Unique identifier for authentication accounts. |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE | User login handle (e.g., admin, student1). |
| `password_hash` | VARCHAR(255) | NOT NULL | SHA-256 cryptographic password hash. |
| `role` | ENUM | NOT NULL | Access role (`ADMIN`, `FACULTY`, `STUDENT`). |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account state flag. |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp when account was provisioned. |

### Table 5.4: Data Dictionary for `students`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `student_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for students. |
| `user_id` | INT | NOT NULL, FK $\to$ users | Associated login account ID (`ON DELETE CASCADE`). |
| `registration_number`| VARCHAR(20) | NOT NULL, UNIQUE | Institutional roll number (e.g., REG2023001). |
| `first_name` | VARCHAR(50) | NOT NULL | Student given name. |
| `last_name` | VARCHAR(50) | NOT NULL | Student surname. |
| `email` | VARCHAR(100) | NOT NULL, UNIQUE | Official university email address. |
| `phone` | VARCHAR(15) | NULL | Contact phone number. |
| `department` | VARCHAR(50) | NOT NULL | Academic branch (e.g., Computer Science). |
| `semester` | INT | CHECK (1 TO 8) | Current semester of study. |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Profile creation timestamp. |

### Table 5.5: Data Dictionary for `faculty`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `faculty_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for faculty. |
| `user_id` | INT | NOT NULL, FK $\to$ users | Associated login account ID (`ON DELETE CASCADE`). |
| `faculty_code` | VARCHAR(20) | NOT NULL, UNIQUE | Institutional faculty employee code (e.g., FAC001). |
| `first_name` | VARCHAR(50) | NOT NULL | Faculty first name. |
| `last_name` | VARCHAR(50) | NOT NULL | Faculty last name. |
| `email` | VARCHAR(100) | NOT NULL, UNIQUE | Institutional faculty email address. |
| `department` | VARCHAR(50) | NOT NULL | Faculty department. |
| `designation` | VARCHAR(50) | NULL | Academic rank (Professor, Associate Professor). |

### Table 5.6: Data Dictionary for `courses`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `course_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for courses. |
| `course_code` | VARCHAR(20) | NOT NULL, UNIQUE | University course catalog code (e.g., CS301). |
| `course_name` | VARCHAR(100) | NOT NULL | Full descriptive course title. |
| `credits` | INT | CHECK (credits > 0) | Academic credit weight. |
| `department` | VARCHAR(50) | NOT NULL | Department offering the course. |

### Table 5.7: Data Dictionary for `sections`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `section_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for sections. |
| `section_name` | VARCHAR(20) | NOT NULL | Cohort identifier (e.g., CS-A). |
| `semester` | INT | NOT NULL | Academic semester. |
| `academic_year` | VARCHAR(9) | NOT NULL | Academic year period (e.g., 2023-2024). |
| `department` | VARCHAR(50) | NOT NULL | Department owning the section. |
| *Composite* | UNIQUE | *(name, sem, year, dept)* | Prevents duplicate section cohort definitions. |

### Table 5.8: Data Dictionary for `student_section`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `student_section_id`| INT | PK, AUTO_INCREMENT | Surrogate identifier for student enrollment. |
| `student_id` | INT | NOT NULL, FK $\to$ students | Enrolled student reference (`ON DELETE CASCADE`). |
| `section_id` | INT | NOT NULL, FK $\to$ sections | Assigned section reference (`ON DELETE CASCADE`). |
| `academic_year` | VARCHAR(9) | NOT NULL | Applicable academic enrollment year. |
| *Composite* | UNIQUE | *(student, section, year)* | Prevents duplicate enrollments in the same term. |

### Table 5.9: Data Dictionary for `course_offerings`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `offering_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for course offerings. |
| `course_id` | INT | NOT NULL, FK $\to$ courses | Course reference (`ON DELETE CASCADE`). |
| `section_id` | INT | NOT NULL, FK $\to$ sections | Section reference (`ON DELETE CASCADE`). |
| `faculty_id` | INT | NOT NULL, FK $\to$ faculty | Assigned instructor (`ON DELETE CASCADE`). |
| `academic_year` | VARCHAR(9) | NOT NULL | Academic year of offering. |
| `semester` | INT | NOT NULL | Semester of offering. |
| *Composite* | UNIQUE | *(course, sec, year, sem)* | Ensures one faculty assignment per course-section term. |

### Table 5.10: Data Dictionary for `class_sessions`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `session_id` | INT | PK, AUTO_INCREMENT | Surrogate identifier for a class lecture. |
| `offering_id` | INT | NOT NULL, FK $\to$ offerings| Associated offering (`ON DELETE CASCADE`). |
| `session_date` | DATE | NOT NULL | Date the lecture took place. |
| `start_time` | TIME | NOT NULL | Scheduled start time. |
| `end_time` | TIME | NOT NULL, CHECK (end > start)| Scheduled conclusion time. |
| `topic_covered` | VARCHAR(255) | NULL | Academic syllabus topic addressed. |
| `session_status`| ENUM | DEFAULT 'SCHEDULED' | Status: `SCHEDULED`, `COMPLETED`, `CANCELLED`, `MAKEUP`. |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Session record creation timestamp. |
| *Composite* | UNIQUE | *(offering, date, start_time)*| Prevents double-scheduling of a class session. |

### Table 5.11: Data Dictionary for `attendance`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `attendance_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for attendance mark. |
| `session_id` | INT | NOT NULL, FK $\to$ sessions | Class session reference (`ON DELETE CASCADE`). |
| `student_id` | INT | NOT NULL, FK $\to$ students | Student reference (`ON DELETE CASCADE`). |
| `attendance_status`| ENUM | NOT NULL | Status: `PRESENT`, `ABSENT`, `LATE`, `EXCUSED`. |
| `marked_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp when attendance was logged. |
| `remarks` | VARCHAR(255) | NULL | Instructor observations or excuse notes. |
| *Composite* | UNIQUE | *(session_id, student_id)* | Enforces exactly one attendance mark per student per session. |

### Table 5.12: Data Dictionary for `leave_types`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `leave_type_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for leave categories. |
| `leave_type_name` | VARCHAR(50) | NOT NULL, UNIQUE | Leave title (Medical, Academic, Personal). |
| `description` | VARCHAR(255) | NULL | Policy description of leave type. |
| `max_days` | INT | CHECK (max_days > 0) | Maximum consecutive days allowed. |
| `requires_document`| BOOLEAN | DEFAULT FALSE | Flag indicating if medical/event proof is required. |

### Table 5.13: Data Dictionary for `leave_applications`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `application_id` | INT | PK, AUTO_INCREMENT | Surrogate identifier for leave requests. |
| `student_id` | INT | NOT NULL, FK $\to$ students | Applying student (`ON DELETE CASCADE`). |
| `leave_type_id` | INT | NOT NULL, FK $\to$ types | Category reference (`ON DELETE CASCADE`). |
| `from_date` | DATE | NOT NULL | Start date of requested leave. |
| `to_date` | DATE | NOT NULL, CHECK (from <= to) | End date of requested leave. |
| `reason` | TEXT | NOT NULL | Justification provided by applicant. |
| `application_status`| ENUM | DEFAULT 'PENDING' | Status: `PENDING`, `APPROVED`, `REJECTED`, `CANCELLED`. |
| `submitted_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Application submission timestamp. |

### Table 5.14: Data Dictionary for `leave_approvals`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `approval_id` | INT | PK, AUTO_INCREMENT | Surrogate identifier for approval decisions. |
| `application_id` | INT | NOT NULL, FK $\to$ apps | Evaluated request (`ON DELETE CASCADE`). |
| `faculty_id` | INT | NOT NULL, FK $\to$ faculty | Evaluating instructor (`ON DELETE CASCADE`). |
| `approval_status`| ENUM | NOT NULL | Decision: `APPROVED` or `REJECTED`. |
| `remarks` | VARCHAR(255) | NULL | Comments or justifications from instructor. |
| `approved_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Decision timestamp. |

### Table 5.15: Data Dictionary for `makeup_sessions`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `makeup_id` | INT | PK, AUTO_INCREMENT | Surrogate identifier for makeup mappings. |
| `original_session_id`| INT | NOT NULL, FK $\to$ sessions| Cancelled class reference (`ON DELETE CASCADE`). |
| `makeup_session_id` | INT | NOT NULL, FK $\to$ sessions| Compensatory class reference (`ON DELETE CASCADE`). |
| `reason` | VARCHAR(255) | NULL | Explanation for makeup requirement. |
| `created_by` | INT | NOT NULL, FK $\to$ faculty | Instructor scheduling the makeup. |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp. |
| *Constraint* | CHECK | *(original != makeup)* | Prevents circular mapping of a session to itself. |

### Table 5.16: Data Dictionary for `alerts`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `alert_id` | INT | PK, AUTO_INCREMENT | Surrogate identifier for shortage alerts. |
| `student_id` | INT | NOT NULL, FK $\to$ students | Target student reference (`ON DELETE CASCADE`). |
| `offering_id` | INT | NOT NULL, FK $\to$ offerings| Relevant course offering (`ON DELETE CASCADE`). |
| `alert_type` | ENUM | NOT NULL | Category: `SHORTAGE`, `CRITICAL_SHORTAGE`. |
| `attendance_percentage`| DECIMAL(5,2)| CHECK (pct BETWEEN 0 AND 100)| Percentage at time of alert generation. |
| `message` | VARCHAR(255) | NOT NULL | Explanatory warning text. |
| `is_resolved` | BOOLEAN | DEFAULT FALSE | Flag indicating if acknowledged/rectified. |
| `generated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Generation timestamp. |

### Table 5.17: Data Dictionary for `attendance_thresholds`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `threshold_id` | INT | PK, AUTO_INCREMENT | Surrogate identifier for institutional policy. |
| `minimum_percentage` | DECIMAL(5,2)| NOT NULL | Standard passing percentage (75.00%). |
| `critical_percentage`| DECIMAL(5,2)| NOT NULL | Critical danger threshold (65.00%). |
| `applicable_from` | DATE | NOT NULL | Policy effective date. |
| *Constraint* | CHECK | *(minimum > critical)* | Prevents invalid policy definitions. |

## 5.5 Database Triggers and Stored Procedures Implementation
AttendX utilizes active database programming via triggers and stored procedures implemented in MySQL 8.0:

**Table 5.18: Active Database Triggers and Stored Procedures**
| Routine Name | Type | Event / Purpose |
| :--- | :--- | :--- |
| **`trg_after_attendance_insert`** | `TRIGGER` | Fires after an attendance insert. Dynamically calculates student course percentage; if below 75% or 65%, inserts a warning row into `alerts`. |
| **`trg_after_leave_approval`** | `TRIGGER` | Fires after a leave approval insert. Updates `leave_applications` status and automatically flips corresponding `ABSENT` records to `EXCUSED`. |
| **`sp_batch_schedule_sessions`** | `PROCEDURE`| Batch schedules sessions for an offering over a date range for a specific day of the week with syllabus topic prefixes. |
| **`sp_get_student_summary`** | `PROCEDURE`| Computes aggregated student standing metrics using nested subqueries and joins with `vw_student_attendance_percentage`. |

### Listing 5.1: Absence Reconciliation Trigger
```sql
DELIMITER $$
CREATE TRIGGER trg_after_leave_approval
AFTER INSERT ON leave_approvals
FOR EACH ROW
BEGIN
    DECLARE v_student_id INT;
    DECLARE v_from_date DATE;
    DECLARE v_to_date DATE;

    IF NEW.approval_status = 'APPROVED' THEN
        SELECT student_id, from_date, to_date 
        INTO v_student_id, v_from_date, v_to_date
        FROM leave_applications
        WHERE application_id = NEW.application_id;

        UPDATE leave_applications 
        SET application_status = 'APPROVED'
        WHERE application_id = NEW.application_id;

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
DELIMITER ;
```

## 5.6 Analytical Views Implementation
To prevent redundant storage of derived data (violating 3NF), dynamic attendance percentages are computed on-the-fly using 5 production database views:

**Table 5.19: Production Database Analytical Views**
| View Name | Primary Function | Core Aggregation Logic |
| :--- | :--- | :--- |
| **`vw_student_attendance_percentage`** | Dynamic attendance percentage per student per course. | `SUM(CASE WHEN status IN ('PRESENT','EXCUSED','LATE') THEN 1 ELSE 0 END) / COUNT(sessions) * 100` |
| **`vw_attendance_shortage`** | Flags students as `GOOD`, `SHORTAGE`, or `CRITICAL_SHORTAGE`. | Cross-joins `vw_student_attendance_percentage` with latest thresholds in `attendance_thresholds`. |
| **`vw_leave_history`** | Full audit trail of leave applications and approver decisions. | Joins `leave_applications`, `students`, `leave_types`, `leave_approvals`, and `faculty`. |
| **`vw_course_attendance_summary`** | Course-level average attendance across sections. | Aggregates completed session counts and computes average percentage per offering. |
| **`vw_monthly_attendance_trends`** | Month-over-month attendance tracking for seasonal analysis. | Groups completed sessions by `DATE_FORMAT(session_date, '%Y-%m')`. |

### Listing 5.2: Percentage Computation View Definition
```sql
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
```

## 5.7 Representative SQL Queries (Joins, Aggregates, Subqueries)
The schema was validated using complex SQL statements spanning various relational operations:

### 1. Complex Inner Join: Attendance Roster with Offering Context
```sql
SELECT s.registration_number, CONCAT(s.first_name, ' ', s.last_name) AS student_name,
       c.course_name, sec.section_name, cs.session_date, a.attendance_status
FROM attendance a
INNER JOIN students s ON a.student_id = s.student_id
INNER JOIN class_sessions cs ON a.session_id = cs.session_id
INNER JOIN course_offerings co ON cs.offering_id = co.offering_id
INNER JOIN courses c ON co.course_id = c.course_id
INNER JOIN sections sec ON co.section_id = sec.section_id
WHERE cs.session_id = 1;
```

### 2. Aggregate Query with Having: Total Absences Exceeding Tolerance
```sql
SELECT s.registration_number, CONCAT(s.first_name, ' ', s.last_name) AS student_name,
       COUNT(a.attendance_id) AS total_absences
FROM attendance a
JOIN students s ON a.student_id = s.student_id
WHERE a.attendance_status = 'ABSENT'
GROUP BY s.student_id
HAVING total_absences >= 3;
```

### 3. Nested Correlated Subquery: Identifying Students Below Course Average
```sql
SELECT v1.student_name, v1.course_code, v1.attendance_percentage
FROM vw_student_attendance_percentage v1
WHERE v1.attendance_percentage < (
    SELECT AVG(v2.attendance_percentage)
    FROM vw_student_attendance_percentage v2
    WHERE v2.course_code = v1.course_code
);
```

## 5.8 Application Development & Module-to-Database Mapping
**Table 5.20: Application Module to Database Mapping**
| Module / Page | Primary Target Relations | Operations Executed |
| :--- | :--- | :--- |
| **Authentication (`app.py`, `auth_service.py`)** | `users`, `students`, `faculty` | Verification, Session Token Provisioning (`SELECT`). |
| **Admin Master Management (`pages/admin/`)** | `students`, `faculty`, `courses`, `sections`, `offerings` | Full CRUD operations. |
| **Admin Analytics Console (`pages/admin/reports.py`)**| `vw_*` Views, `sp_get_student_summary` | Analytical extraction, visualization, raw query sandbox. |
| **Faculty Session Management (`pages/faculty/`)** | `class_sessions`, `makeup_sessions` | Creation, makeup linking (`INSERT`, `UPDATE`). |
| **Faculty Attendance Grid (`pages/faculty/attendance.py`)**| `attendance`, `class_sessions` | Atomic batch marking (`INSERT ... ON DUPLICATE KEY`). |
| **Faculty Leave Review (`pages/faculty/leave_approval.py`)**| `leave_applications`, `leave_approvals`| Decision recording; triggers absence reconciliation. |
| **Student Dashboard & History (`pages/student/`)** | `vw_student_attendance_percentage`, `attendance` | Filtering and personal progress reporting. |
| **Student Leave Submission (`pages/student/leave_app.py`)**| `leave_applications`, `leave_types` | Request submission with date validation. |
| **Student Alerts Center (`pages/student/alerts.py`)** | `alerts`, `vw_attendance_shortage` | Active alert inspection. |

## 5.9 CRUD Operations and Business Rule Verification
**Table 5.21: CRUD Operations Evidence Matrix**
| Operation | Feature / Screen | Target Relation(s) | Operational Evidence |
| :--- | :--- | :--- | :--- |
| **Create** | Add Student Profile | `users`, `students` | User and profile records inserted atomically with hashed credentials. |
| **Create** | Schedule Session | `class_sessions` | Session record created with `SCHEDULED` status. |
| **Read** | View Course Standing | `vw_student_attendance_percentage` | Dynamic percentage computed without storing derived values. |
| **Update** | Re-mark Attendance | `attendance` | Updates existing status; activates shortage trigger. |
| **Update** | Leave Review Decision | `leave_approvals` | Inserts approval; trigger updates application status and absences. |
| **Delete** | Student De-registration | `students` | Cascading deletion removes enrollments, attendances, and leaves. |

**Table 5.22: Business Rules, Validation, and Constraint Mapping**
| Business Rule | Implementation Level | Enforcement Mechanism | Operational Evidence |
| :--- | :--- | :--- | :--- |
| **Unique Student Attendance** | Database Tier | `UNIQUE (session_id, student_id)` | Duplicate attendance rejected with error code 1062. |
| **Valid Session Duration** | Database Tier | `CHECK (end_time > start_time)` | Zero or negative duration rejected by schema. |
| **Logical Leave Window** | Database Tier | `CHECK (from_date <= to_date)` | Inverted leave windows rejected. |
| **Non-Circular Makeup Class** | Database Tier | `CHECK (original != makeup)` | Self-referencing makeup mapping blocked. |
| **Bounded Percentage Values** | Database Tier | `CHECK (percentage BETWEEN 0 AND 100)` | Invalid percentages rejected. |
| **Valid Academic Semesters** | Database Tier | `CHECK (semester BETWEEN 1 AND 8)` | Semesters outside 1–8 rejected. |
| **Cascading Cleanup** | Database Tier | `ON DELETE CASCADE` on Foreign Keys | Deleting a student removes all dependent attendance rows. |
| **Credential Protection** | Application Tier | SHA-256 Hashing | Plaintext passwords are never stored in the database. |

## 5.10 Dataset Description & Seed Population
The database is seeded with realistic institutional test data across all relations:

**Table 5.23: Seed Dataset Breakdown across Core Entities**
| Entity / Table | Record Count | Seed Description / Test Profile |
| :--- | :---: | :--- |
| **`users`** | 14 | Accounts for Admin, 3 Faculty, and 10 Students with SHA-256 hashes. |
| **`faculty`** | 3 | Faculty across Computer Science, Information Technology, and Electronics. |
| **`students`** | 10 | Students across CS, IT, and EC cohorts. |
| **`courses`** | 5 | Core curriculum: CS301 (DBMS), CS302 (OS), IT301 (Web Tech), IT302 (CN), EC301 (DSP). |
| **`sections`** | 3 | Cohorts: CS-A, IT-A, EC-A. |
| **`course_offerings`** | 5 | Ternary mappings connecting Course + Section + Faculty. |
| **`class_sessions`** | 65 | Complete lecture history over 6 weeks, including completed and cancelled classes. |
| **`attendance`** | 216 | Realistic attendance records (`PRESENT`, `ABSENT`, `LATE`, `EXCUSED`). |
| **`leave_types`** | 4 | Policies for Medical (10 days), Personal (5 days), Academic (7 days), Emergency (3 days). |
| **`leave_applications`** | 6 | Multi-day leave requests: 3 Approved, 1 Rejected, 2 Pending. |
| **`leave_approvals`** | 4 | Faculty approval decisions with audit remarks. |
| **`makeup_sessions`** | 5 | Mappings linking cancelled lectures to makeup sessions. |
| **`attendance_thresholds`**| 1 | University policy: 75% minimum, 65% critical. |
| **`alerts`** | 38 | Trigger-generated warning records for students at risk. |

## 5.11 Application Screens & Output Verification
The application provides distinct interfaces for each role:
- **Admin Dashboard & Reports**: Displays institutional metrics, course averages, shortage severity breakdowns, and an SQL query console.
- **Faculty Console**: Facilitates session creation, grid-based attendance marking, makeup scheduling, and leave approvals.
- **Student Portal**: Shows live attendance percentages with color-coded threshold bars, session history filters, and leave submission forms.

---
\pagebreak

# CHAPTER 6: RESULTS AND DISCUSSION

## 6.1 Functional Verification & End-to-End Test Cases
The AttendX prototype was tested against a live MySQL 8.0 instance to verify functional workflows and database integrity:

**Table 6.1: End-to-End Lifecycle Test Execution Results**
| Test ID | Operational Test Scenario | Target Entity | Expected Result | Actual Database Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | User Authentication with Valid Role | `users` | Session token created; redirected to role console. | Successfully authenticated and redirected. | **PASS** |
| **TC-02** | Schedule Class Session | `class_sessions` | Session row created with `SCHEDULED` status. | Verified row created for offering. | **PASS** |
| **TC-03** | Batch Mark Attendance (Atomic) | `attendance` | Roster inserted; status updated to `COMPLETED`. | All attendance rows committed atomically. | **PASS** |
| **TC-04** | Shortage Alert Generation | `alerts` | Trigger creates warning row if percentage < 75%. | Shortage alert generated via trigger. | **PASS** |
| **TC-05** | Makeup Session Scheduling | `makeup_sessions` | Makeup class mapped to original cancelled session. | Verified makeup linkage created. | **PASS** |
| **TC-06** | Student Leave Submission | `leave_applications` | Leave request inserted with `PENDING` status. | Validated row created with submission time. | **PASS** |
| **TC-07** | Faculty Leave Approval | `leave_approvals` | Approval logged; absence converted to `EXCUSED`. | Trigger converted past absences to `EXCUSED`. | **PASS** |
| **TC-08** | Dynamic Percentage Computation | `vw_student_attendance_percentage` | Dynamic computation without stored derived data. | Accurately returns attended / total * 100. | **PASS** |

## 6.2 Database Integrity & Constraint Verification
Negative test cases were conducted to confirm that constraints are enforced by the database engine:

**Table 6.2: Negative Constraint and Integrity Test Cases**
| Test ID | Constraint Under Test | Applied Negative Input | Database Response | Status |
| :--- | :--- | :--- | :--- | :---: |
| **NC-01** | `UNIQUE (session_id, student_id)` | Insert duplicate attendance for same student and session. | **Rejected**: Error 1062 (Duplicate entry). | **PASS** |
| **NC-02** | `CHECK (end_time > start_time)` | Session with `start_time = 11:00:00` and `end_time = 10:00:00`. | **Rejected**: Error 3819 (Check constraint violated). | **PASS** |
| **NC-03** | `CHECK (from_date <= to_date)` | Leave request with `from = 2023-10-10` and `to = 2023-10-05`. | **Rejected**: Error 3819 (Check constraint violated). | **PASS** |
| **NC-04** | `CHECK (original != makeup)` | Makeup session mapped to its own `session_id`. | **Rejected**: Error 3819 (Check constraint violated). | **PASS** |
| **NC-05** | `ON DELETE CASCADE` | Delete student with existing attendance and leave rows. | **Success**: Student deleted; all child rows cascaded. | **PASS** |
| **NC-06** | Foreign Key Referential Action | Insert attendance referencing non-existent `student_id = 999`. | **Rejected**: Error 1452 (Cannot add child row). | **PASS** |

## 6.3 Analytical Performance Graphs & Interpretations
The analytical views and dashboard charts provide actionable administrative insights:

```
Course Average Attendance Standing (%)
CS301 (DBMS)     [###############################     ] 79.2%
CS302 (OS)       [##############################      ] 75.0%
IT301 (Web Tech) [################################### ] 87.5%
IT302 (Networks) [####################################] 93.8%
EC301 (DSP)      [#################################   ] 83.3%
-------------------------------------------------------------
                 0%        25%       50%       75%    100%
```
**Figure 6.1: Course Attendance Distribution (Average % Across Courses)**  
- **Interpretation**: IT302 (Computer Networks) recorded the highest engagement (93.8%), while CS302 (Operating Systems) sits at the 75.0% threshold boundary, indicating a need for academic review.

```
Attendance Shortage Severity Ratio
+------------------------------------------+
|  GOOD (>= 75%)                 | 73.7%   |
|  SHORTAGE (65% - 75%)          | 15.8%   |
|  CRITICAL SHORTAGE (< 65%)     | 10.5%   |
+------------------------------------------+
```
**Figure 6.2: Attendance Shortage Severity Ratio**  
- **Interpretation**: 73.7% of enrolled students meet attendance requirements. However, 10.5% of students are in critical shortage (<65%), allowing administrators to intervene before exams.

```
Leave Applications by Type and Status
Medical Leave    [##### APPROVED ][# PENDING]
Academic Leave   [### APPROVED  ]
Personal Leave   [## APPROVED   ]
Emergency Leave  [## REJECTED   ]
```
**Figure 6.3: Leave Application Distribution Categorized by Type**  
- **Interpretation**: Medical leaves represent the largest category. Emergency leaves without supporting documentation were rejected, proving that business policies are enforced.

## 6.4 Comparison with Project Objectives
**Table 6.3: Achievement of Project Objectives Evaluation**
| Stated Project Objective | Implementation Measure | Achieved Result | Evaluation |
| :--- | :--- | :--- | :--- |
| **1. 3NF Relational Architecture** | 15 tables decomposed to remove partial and transitive FDs. | Zero insertion, update, or deletion anomalies. | **Fully Achieved** |
| **2. Database-Level Constraints** | Primary keys, foreign keys, `CHECK`, and `UNIQUE` constraints. | Rejects invalid data at the database layer. | **Fully Achieved** |
| **3. Automated Percentage Views** | Dynamic views calculating attendance percentages on-the-fly. | Eliminates stored derived data; calculates in real time. | **Fully Achieved** |
| **4. Trigger Shortage Alerts** | `trg_after_attendance_insert` monitors thresholds. | Automatically inserts alert rows when percentage < 75%. | **Fully Achieved** |
| **5. Trigger Absence Reconciliation**| `trg_after_leave_approval` reconciles past absences. | Automatically converts unexcused absences to `EXCUSED`. | **Fully Achieved** |
| **6. Role-Based Access Control** | Dedicated Admin, Faculty, and Student consoles with SHA-256. | Complete session isolation and unauthorized access prevention. | **Fully Achieved** |
| **7. Multi-Tier Reporting** | Interactive dashboards showing course standings and shortage ratios.| Real-time visual metrics for institutional decision-making. | **Fully Achieved** |

---
\pagebreak

# CHAPTER 7: CONCLUSION AND FUTURE SCOPE

## 7.1 Summary
This Project-Based Learning project successfully designed and implemented **AttendX**, a relational database management system for student attendance and leave governance. By transitioning from manual registers to a centralized **MySQL 8.0** schema composed of **15 tables normalized up to 3NF/BCNF**, the system eliminates data redundancy, duplicate records, and arithmetic errors. 

The implementation demonstrates that a database can serve as an active processing engine: **database views** dynamically calculate percentages without storing derived data; **database triggers** automate shortage alerting and absence reconciliation; and **stored procedures** support batch scheduling and complex analytics. The multi-console web application built with **Python, Streamlit, and Plotly** provides secure, role-segregated access for Admins, Faculty, and Students. End-to-end testing verified that data integrity rules are enforced directly by the database engine.

## 7.2 Key Academic Learning Outcomes
1. **Conceptual-to-Relational Translation**: Applied Chen's ER modeling to identify real-world entities, map cardinalities, and resolve Many-to-Many relationships using associative bridge tables (`attendance`, `student_section`, `course_offerings`).
2. **Mathematical Normalization**: Conducted functional dependency analysis proving that all relations satisfy 1NF, 2NF, 3NF, and BCNF, eliminating insertion, update, and deletion anomalies.
3. **Database Integrity Enforcement**: Implemented primary keys, composite foreign keys with cascading actions (`ON DELETE CASCADE`), domain constraints (`ENUM`, `CHECK`), and candidate keys (`UNIQUE`).
4. **Active Database Programming**: Developed MySQL triggers (`AFTER INSERT`) and stored procedures to enforce institutional business rules at the database tier.
5. **Full-Stack Application Development**: Engineered a database-connected application using Python, connection pooling, parameterized queries, and interactive Plotly visualizations.

## 7.3 Limitations and Future Enhancements
- **Limitations**: The prototype operates in a local environment with simulated SHA-256 session authentication and does not interface with hardware biometric scanners or campus SMS gateways.
- **Future Enhancements**:
  1. **Biometric and RFID Integration**: Interface with biometric or RFID readers to log session attendance directly to `attendance`.
  2. **Automated Notification Gateway**: Integrate Twilio or SendGrid APIs to dispatch automated email and SMS alerts to parents when critical shortages are detected.
  3. **Predictive Attendance Analytics**: Use machine learning models on attendance trends (`vw_monthly_attendance_trends`) to forecast at-risk students earlier in the semester.
  4. **Mobile Application Development**: Build cross-platform mobile apps for iOS and Android to allow students and faculty to access portals on personal devices.

---
\pagebreak

# REFERENCES

[1] B. Atkin and A. Brooks, *Total Facility Management*, 4th ed. Chichester, U.K.: Wiley-Blackwell, 2015.

[2] I. Lopes et al., "Requirements specification of a computerized maintenance management system—A case study," *Procedia CIRP*, vol. 52, pp. 268–273, 2016.

[3] E. F. Codd, "A relational model of data for large shared data banks," *Communications of the ACM*, vol. 13, no. 6, pp. 377–387, Jun. 1970.

[4] P. P. Chen, "The entity-relationship model—Toward a unified view of data," *ACM Transactions on Database Systems*, vol. 1, no. 1, pp. 9–36, Mar. 1976.

[5] E. F. Codd, "Further normalization of the data base relational model," in *Data Base Systems*, R. Rustin, Ed. Englewood Cliffs, NJ, USA: Prentice-Hall, 1972, pp. 33–64.

[6] R. Elmasri and S. B. Navathe, *Fundamentals of Database Systems*, 7th ed. Hoboken, NJ, USA: Pearson, 2016.

[7] A. Silberschatz, H. F. Korth, and S. Sudarshan, *Database System Concepts*, 7th ed. New York, NY, USA: McGraw-Hill, 2019.

[8] T. Haerder and A. Reuter, "Principles of transaction-oriented database recovery," *ACM Computing Surveys*, vol. 15, no. 4, pp. 287–317, Dec. 1983.

[9] D. F. Ferraiolo and D. R. Kuhn, "Role-based access controls," in *Proc. 15th NIST-NCSC National Computer Security Conf.*, Baltimore, MD, USA, Oct. 1992, pp. 554–563.

[10] R. S. Sandhu, E. J. Coyne, H. L. Feinstein, and C. E. Youman, "Role-based access control models," *IEEE Computer*, vol. 29, no. 2, pp. 38–47, Feb. 1996.

[11] J. H. Saltzer and M. D. Schroeder, "The protection of information in computer systems," *Proceedings of the IEEE*, vol. 63, no. 9, pp. 1278–1308, Sep. 1975.

[12] OWASP Foundation, "OWASP Top 10:2021 - The Ten Most Critical Web Application Security Risks," [Online]. Available: https://owasp.org/Top10/. Accessed: Oct. 2026.

[13] R. T. Fielding, "Architectural styles and the design of network-based software architectures," Ph.D. dissertation, Dept. Inf. Comput. Sci., Univ. California, Irvine, CA, USA, 2000.

[14] Oracle Corporation, "MySQL 8.0 Reference Manual: InnoDB Storage Engine, Triggers, and Stored Programs," [Online]. Available: https://dev.mysql.com/doc/refman/8.0/en/. Accessed: Oct. 2026.

[15] Python Software Foundation, "Python Database API Specification v2.0 (PEP 249)," [Online]. Available: https://peps.python.org/pep-0249/. Accessed: Oct. 2026.

---
\pagebreak

# APPENDICES

### APPENDIX A - COMPLETE DATABASE DDL SCRIPT (`database.sql`)
```sql
CREATE DATABASE IF NOT EXISTS attendx_db;
USE attendx_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('ADMIN', 'FACULTY', 'STUDENT') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    credits INT CHECK (credits > 0),
    department VARCHAR(50) NOT NULL
);

CREATE TABLE sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    section_name VARCHAR(20) NOT NULL,
    semester INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    department VARCHAR(50) NOT NULL,
    UNIQUE (section_name, semester, academic_year, department)
);

CREATE TABLE student_section (
    student_section_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    section_id INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
    UNIQUE (student_id, section_id, academic_year)
);

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

CREATE TABLE leave_types (
    leave_type_id INT AUTO_INCREMENT PRIMARY KEY,
    leave_type_name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    max_days INT CHECK (max_days > 0),
    requires_document BOOLEAN DEFAULT FALSE
);

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

CREATE TABLE attendance_thresholds (
    threshold_id INT AUTO_INCREMENT PRIMARY KEY,
    minimum_percentage DECIMAL(5, 2) NOT NULL,
    critical_percentage DECIMAL(5, 2) NOT NULL,
    applicable_from DATE NOT NULL,
    CHECK (minimum_percentage > critical_percentage)
);
```

### APPENDIX B - PROCEDURES, TRIGGERS, AND ANALYTICAL VIEWS
*(See Section 5.5 and 5.6 for detailed listings of `trg_after_attendance_insert`, `trg_after_leave_approval`, `sp_batch_schedule_sessions`, `sp_get_student_summary`, and all five database views).*

### APPENDIX C - REPRESENTATIVE ANALYTICAL QUERIES (`queries.sql`)
*(See Section 5.7 and project file `database/queries.sql` for complete catalog of 15+ complex queries categorized under Joins, Aggregate Functions, and Correlated Subqueries).*
