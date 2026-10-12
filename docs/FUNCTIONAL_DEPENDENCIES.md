# Functional Dependencies

In relational database theory, a functional dependency is a relationship between two attributes, typically between the primary key and other non-key attributes within a table.

## 1. `users` Table
- `user_id` &rarr; `username, password_hash, role, is_active, created_at`
- `username` &rarr; `user_id, password_hash, role` (Candidate Key)

## 2. `students` Table
- `student_id` &rarr; `user_id, registration_number, first_name, last_name, email, phone, department, semester`
- `registration_number` &rarr; `student_id, user_id, first_name...` (Candidate Key)
- `email` &rarr; `student_id...` (Candidate Key)

## 3. `courses` Table
- `course_id` &rarr; `course_code, course_name, credits, department`
- `course_code` &rarr; `course_id, course_name, credits, department`

## 4. `course_offerings` Table
- `offering_id` &rarr; `course_id, section_id, faculty_id, academic_year, semester`
- Composite Key: `{course_id, section_id, academic_year, semester}` &rarr; `offering_id, faculty_id`

## 5. `class_sessions` Table
- `session_id` &rarr; `offering_id, session_date, start_time, end_time, topic_covered, session_status`
- Composite Key: `{offering_id, session_date, start_time}` &rarr; `session_id, end_time, topic_covered`

## 6. `attendance` Table
- `attendance_id` &rarr; `session_id, student_id, attendance_status, remarks, marked_at`
- Composite Key: `{session_id, student_id}` &rarr; `attendance_id, attendance_status, remarks`

## 7. `leave_applications` Table
- `application_id` &rarr; `student_id, leave_type_id, from_date, to_date, reason, application_status`

## 8. `alerts` Table
- `alert_id` &rarr; `student_id, offering_id, alert_type, attendance_percentage, message, is_resolved`
