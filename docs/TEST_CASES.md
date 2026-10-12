# Test Cases

| Test ID | Module | Test Scenario | Input | Expected Result | Status |
|---|---|---|---|---|---|
| TC_01 | Auth | Valid login | admin / Admin@123 | Login successful, Admin dashboard loads | Pending |
| TC_02 | Auth | Invalid login | admin / wrongpass | "Invalid username or password" | Pending |
| TC_03 | Student | Unique Registration | Insert duplicate Reg No | Database constraint violation error | Pending |
| TC_04 | Session | Time validation | Start: 10:00, End: 09:00 | "Start time must be before end time" | Pending |
| TC_05 | Attendance | Mark attendance | Select 'PRESENT' for student | Record saved, status='COMPLETED' | Pending |
| TC_06 | Attendance | Duplicate attendance | Re-mark attendance | Replaces existing record (transaction safe) | Pending |
| TC_07 | Leave | Invalid dates | From: 10-Oct, To: 05-Oct | "Invalid dates" validation error | Pending |
| TC_08 | Leave | Faculty approval | Faculty clicks "Approve" | Application status changes to APPROVED | Pending |
| TC_09 | Alerts | Shortage threshold | Attendance < 75% | Shortage alert generated for student | Pending |
| TC_10 | Reports | Course Summary | View Report tab | Shows accurate aggregate data via views | Pending |
| TC_11 | DB | Constraint | Delete Course | Fails if linked to offerings (or cascades) | Pending |
| TC_12 | Makeup | Create Makeup | Link to original session | Makeup session created successfully | Pending |
| TC_13 | Security | Role Isolation | Student tries to access `/pages/admin` | Redirected / Access Denied | Pending |
| TC_14 | DB | View Data | Select from vw_student_attendance | Returns accurately calculated % | Pending |
| TC_15 | Attendance | Percentage Calc | Mark 1 absent, 3 present | Percentage dynamically updates to 75% | Pending |
