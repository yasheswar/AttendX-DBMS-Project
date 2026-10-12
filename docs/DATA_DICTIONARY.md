# Data Dictionary

## Table: `users`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | INT | PK, AUTO_INC | Unique user ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Login username |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| role | ENUM | NOT NULL | 'ADMIN', 'FACULTY', 'STUDENT' |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |

## Table: `students`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| student_id | INT | PK, AUTO_INC | Unique student ID |
| user_id | INT | FK (users) | Link to auth |
| registration_number | VARCHAR | UNIQUE, NOT NULL | University Roll No |
| first_name | VARCHAR | NOT NULL | - |
| semester | INT | CHECK (1-8) | Current semester |

*(Complete schema details can be inferred directly from `database.sql`)*
