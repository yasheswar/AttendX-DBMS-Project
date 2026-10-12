-- Sample Data for AttendX
USE attendx_db;

-- Passwords are hashed using SHA-256
-- Admin@123 -> e86f78a8a3caf0b60d8e74e5942aa6d86dc150cd3c03338aef25b7d2d7e3acc7
-- Faculty@123 -> 9859bcef2187144a16f11447b17129443780817a119496650b96bf354a65739e
-- Student@123 -> b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54

-- Insert Users
INSERT INTO users (username, password_hash, role) VALUES
('admin', 'e86f78a8a3caf0b60d8e74e5942aa6d86dc150cd3c03338aef25b7d2d7e3acc7', 'ADMIN'),
('faculty1', '9859bcef2187144a16f11447b17129443780817a119496650b96bf354a65739e', 'FACULTY'),
('faculty2', '9859bcef2187144a16f11447b17129443780817a119496650b96bf354a65739e', 'FACULTY'),
('faculty3', '9859bcef2187144a16f11447b17129443780817a119496650b96bf354a65739e', 'FACULTY'),
('student1', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54', 'STUDENT'),
('student2', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54', 'STUDENT'),
('student3', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54', 'STUDENT'),
('student4', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54', 'STUDENT'),
('student5', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54', 'STUDENT'),
('student6', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54', 'STUDENT'),
('student7', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54', 'STUDENT'),
('student8', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54', 'STUDENT'),
('student9', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54', 'STUDENT'),
('student10', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54', 'STUDENT');

-- Insert Faculty
INSERT INTO faculty (user_id, faculty_code, first_name, last_name, email, department, designation) VALUES
(2, 'FAC001', 'Arvind', 'Kumar', 'arvind.kumar@university.edu', 'Computer Science', 'Professor'),
(3, 'FAC002', 'Sunita', 'Sharma', 'sunita.sharma@university.edu', 'Information Technology', 'Associate Professor'),
(4, 'FAC003', 'Rajesh', 'Singh', 'rajesh.singh@university.edu', 'Electronics', 'Assistant Professor');

-- Insert Students
INSERT INTO students (user_id, registration_number, first_name, last_name, email, phone, department, semester) VALUES
(5, 'REG2023001', 'Rahul', 'Verma', 'rahul.v@university.edu', '9876543210', 'Computer Science', 5),
(6, 'REG2023002', 'Priya', 'Patel', 'priya.p@university.edu', '9876543211', 'Computer Science', 5),
(7, 'REG2023003', 'Amit', 'Shah', 'amit.s@university.edu', '9876543212', 'Information Technology', 5),
(8, 'REG2023004', 'Neha', 'Gupta', 'neha.g@university.edu', '9876543213', 'Information Technology', 5),
(9, 'REG2023005', 'Vikram', 'Singh', 'vikram.s@university.edu', '9876543214', 'Electronics', 5),
(10, 'REG2023006', 'Sneha', 'Reddy', 'sneha.r@university.edu', '9876543215', 'Computer Science', 5),
(11, 'REG2023007', 'Karan', 'Malhotra', 'karan.m@university.edu', '9876543216', 'Information Technology', 5),
(12, 'REG2023008', 'Pooja', 'Iyer', 'pooja.i@university.edu', '9876543217', 'Electronics', 5),
(13, 'REG2023009', 'Rohan', 'Desai', 'rohan.d@university.edu', '9876543218', 'Computer Science', 5),
(14, 'REG2023010', 'Anjali', 'Nair', 'anjali.n@university.edu', '9876543219', 'Information Technology', 5);

-- Insert Courses
INSERT INTO courses (course_code, course_name, credits, department) VALUES
('CS301', 'Database Management Systems', 4, 'Computer Science'),
('CS302', 'Operating Systems', 4, 'Computer Science'),
('IT301', 'Web Technologies', 3, 'Information Technology'),
('IT302', 'Computer Networks', 4, 'Information Technology'),
('EC301', 'Digital Signal Processing', 4, 'Electronics');

-- Insert Sections
INSERT INTO sections (section_name, semester, academic_year, department) VALUES
('CS-A', 5, '2023-2024', 'Computer Science'),
('IT-A', 5, '2023-2024', 'Information Technology'),
('EC-A', 5, '2023-2024', 'Electronics');

-- Insert Student Sections
INSERT INTO student_section (student_id, section_id, academic_year) VALUES
(1, 1, '2023-2024'), (2, 1, '2023-2024'), (6, 1, '2023-2024'), (9, 1, '2023-2024'),
(3, 2, '2023-2024'), (4, 2, '2023-2024'), (7, 2, '2023-2024'), (10, 2, '2023-2024'),
(5, 3, '2023-2024'), (8, 3, '2023-2024');

-- Insert Course Offerings
INSERT INTO course_offerings (course_id, section_id, faculty_id, academic_year, semester) VALUES
(1, 1, 1, '2023-2024', 5), -- DBMS for CS-A by Arvind
(2, 1, 2, '2023-2024', 5), -- OS for CS-A by Sunita
(3, 2, 2, '2023-2024', 5), -- Web Tech for IT-A by Sunita
(4, 2, 1, '2023-2024', 5), -- CN for IT-A by Arvind
(5, 3, 3, '2023-2024', 5); -- DSP for EC-A by Rajesh

-- Insert Leave Types
INSERT INTO leave_types (leave_type_name, description, max_days, requires_document) VALUES
('Medical Leave', 'Leave due to illness or medical emergencies', 10, TRUE),
('Personal Leave', 'Leave for personal reasons or family events', 5, FALSE),
('Academic Leave', 'Leave for attending conferences, workshops, or academic events', 7, TRUE),
('Emergency Leave', 'Unplanned emergency situations', 3, FALSE);

-- Insert Attendance Thresholds
INSERT INTO attendance_thresholds (minimum_percentage, critical_percentage, applicable_from) VALUES
(75.00, 65.00, '2023-01-01');

-- Additional data like class sessions and attendance can be created through the UI for testing
