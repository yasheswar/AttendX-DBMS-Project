# Comprehensive Database Normalization Analysis (Up to 3NF & BCNF)
## AttendX: Smart Student Attendance & Leave Management System

This document provides a formal, mathematically rigorous explanation of database normalization for AttendX, proving that every relation satisfies the **Third Normal Form (3NF)** and **Boyce-Codd Normal Form (BCNF)** to eliminate Insertion, Update, and Deletion anomalies.

---

## 1. Unnormalized Form (UNF) & Anomalies

In a naive flat-file or spreadsheet design, a university attendance tracking record combines everything into a single relation:

$$\text{ATTENDANCE\_FLAT}(\underline{\text{RegNo}}, \text{StudentName}, \text{CourseCode}, \text{CourseName}, \text{Credits}, \text{FacultyCode}, \text{FacultyName}, \text{Section}, \text{SessionDate}, \text{Time}, \text{Status}, \text{LeaveReason})$$

### Anomalies in UNF:
1. **Redundancy**: Course name, credits, and faculty details are duplicated for every student in every single class session.
2. **Insertion Anomaly**: We cannot create a new Course or Faculty until at least one student attends a session.
3. **Update Anomaly**: If a Course title changes, thousands of rows across all past class sessions must be updated. A failure to update all causes data inconsistency.
4. **Deletion Anomaly**: If we delete the attendance records for a semester, all information about the Course, Section, and Faculty assignment could be lost.

---

## 2. First Normal Form (1NF)

### Formal Definition:
A relation $R$ is in **1NF** if and only if all domain values are atomic (indivisible) and there are no repeating groups or composite multivalued attributes.

### Transformation in AttendX:
- Multi-valued attributes (e.g., student phone numbers or multiple sessions attended) are eliminated.
- Single atomic columns are defined for all attributes (`first_name`, `last_name`, `start_time`, `end_time`).
- Unique row identification is guaranteed by candidate keys and primary keys.

$$\text{All } 15 \text{ tables in AttendX satisfy 1NF.}$$

---

## 3. Second Normal Form (2NF)

### Formal Definition:
A relation $R$ is in **2NF** if and only if it is in 1NF and every non-prime attribute is **fully functionally dependent** on the primary key (i.e., no non-prime attribute has a partial dependency on any proper subset of a candidate key).

### Identification and Elimination of Partial Dependencies:
Consider student section enrollment and course offerings:
- In a composite table $\text{ENROLLMENT}(\underline{\text{student\_id}, \text{course\_id}}, \text{student\_name}, \text{course\_name})$, we have:
  - $\text{student\_id} \to \text{student\_name}$ (Partial dependency)
  - $\text{course\_id} \to \text{course\_name}$ (Partial dependency)

### Resolution in AttendX:
We decompose composite relationships into dedicated entities with surrogate or proper primary keys:
1. **`students`**: $\text{student\_id} \to \text{first\_name}, \text{last\_name}, \text{email}, \text{department}$
2. **`courses`**: $\text{course\_id} \to \text{course\_code}, \text{course\_name}, \text{credits}$
3. **`course_offerings`**: Uses $\text{offering\_id}$ as PK, mapping $(\text{course\_id}, \text{section\_id}, \text{faculty\_id})$.
4. **`attendance`**: Primary key is $\text{attendance\_id}$. The composite candidate key $(\text{session\_id}, \text{student\_id})$ is enforced via a `UNIQUE` constraint, and the non-key attribute $\text{attendance\_status}$ depends on the *entire* session-student pair.

$$\text{Therefore, all relations in AttendX are in 2NF.}$$

---

## 4. Third Normal Form (3NF)

### Formal Definition:
A relation $R$ is in **3NF** if and only if it is in 2NF and for every non-trivial functional dependency $X \to Y$, either:
1. $X$ is a superkey of $R$, or
2. $Y$ is a prime attribute (part of a candidate key).

In plain words: **No transitive dependencies ($X \to Y$ and $Y \to Z$ where $Z$ is non-prime).**

### Analysis of Key Tables in AttendX:

#### Case 1: `students` Table
- **Functional Dependencies:**
  - $\text{student\_id} \to \text{user\_id}, \text{registration\_number}, \text{first\_name}, \text{last\_name}, \text{email}, \text{department}, \text{semester}$
  - $\text{registration\_number} \to \text{student\_id}, \dots$
  - $\text{email} \to \text{student\_id}, \dots$
- **Verification:** Both $\text{student\_id}$, $\text{registration\_number}$, and $\text{email}$ are candidate keys. There are no non-key to non-key dependencies. $\implies$ **Satisfies 3NF**.

#### Case 2: `course_offerings` Table
- **Decomposition:** Instead of embedding faculty department details or course credit details inside the offering, we maintain foreign keys $\text{course\_id}$, $\text{section\_id}$, and $\text{faculty\_id}$.
- **Dependency:** $\text{offering\_id} \to \text{course\_id}, \text{section\_id}, \text{faculty\_id}, \text{academic\_year}, \text{semester}$.
- **Verification:** The determinant is the candidate key. $\implies$ **Satisfies 3NF**.

#### Case 3: `leave_applications` & `leave_approvals` (Workflow Normalization)
- If approval details were inside `leave_applications`:
  - $\text{application\_id} \to \text{faculty\_id}, \text{approval\_status}, \text{approved\_at}$
  - When an application is created, $\text{faculty\_id}$ and $\text{approval\_status}$ would be `NULL`, violating normalization best practices and introducing insertion/update anomalies during re-reviews.
- **Resolution:** Separated into:
  - `leave_applications(application_id, student_id, leave_type_id, from_date, to_date, reason, application_status)`
  - `leave_approvals(approval_id, application_id, faculty_id, approval_status, remarks, approved_at)`
  $\implies$ **Zero NULL anomalies, strict 3NF maintained**.

---

## 5. Boyce-Codd Normal Form (BCNF) Evaluation

A relation $R$ is in **BCNF** if and only if for every non-trivial functional dependency $X \to Y$, **$X$ is a superkey**.

In AttendX:
- In `attendance`, $(\text{session\_id}, \text{student\_id})$ is a unique key, and $\text{attendance\_id}$ is a surrogate primary key. Every determinant is a superkey.
- In `student_section`, $(\text{student\_id}, \text{section\_id}, \text{academic\_year})$ is unique. Every determinant is a superkey.
- In `sections`, $(\text{section\_name}, \text{semester}, \text{academic\_year}, \text{department})$ is unique. Every determinant is a superkey.

$$\text{AttendX achieves 3NF and Boyce-Codd Normal Form (BCNF) across its entire schema.}$$
