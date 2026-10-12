import streamlit as st
from services.faculty_service import get_faculty_courses
from services.attendance_service import get_sessions_by_offering, get_students_in_offering, get_attendance_for_session, mark_attendance
from utils.helpers import require_role

def show():
    require_role('FACULTY')
    st.header("Mark Attendance")
    fac_id = st.session_state.user['faculty_id']
    
    courses = get_faculty_courses(fac_id)
    if not courses:
        st.warning("No courses assigned.")
        return
        
    course_opts = {f"{c['course_code']} ({c['section_name']})": c['offering_id'] for c in courses}
    offering_id = course_opts[st.selectbox("Select Course", list(course_opts.keys()))]
    
    sessions = get_sessions_by_offering(offering_id)
    if not sessions:
        st.info("No sessions available. Create one first.")
        return
        
    session_opts = {f"{s['session_date']} {s['start_time']} - {s['topic_covered']} [{s['session_status']}]": s['session_id'] for s in sessions}
    session_id = session_opts[st.selectbox("Select Session", list(session_opts.keys()))]
    
    students = get_students_in_offering(offering_id)
    existing_attendance = get_attendance_for_session(session_id)
    
    if students:
        with st.form("attendance_form"):
            attendance_data = []
            st.write("### Student List")
            for idx, stu in enumerate(students):
                sid = stu['student_id']
                col1, col2, col3 = st.columns([2, 2, 2])
                col1.write(f"**{stu['registration_number']}** - {stu['first_name']} {stu['last_name']}")
                
                prev_status = existing_attendance.get(sid, {}).get('attendance_status', 'PRESENT')
                prev_remarks = existing_attendance.get(sid, {}).get('remarks', '')
                
                status_idx = ['PRESENT', 'ABSENT', 'LATE', 'EXCUSED'].index(prev_status)
                status = col2.selectbox("Status", ['PRESENT', 'ABSENT', 'LATE', 'EXCUSED'], index=status_idx, key=f"status_{sid}")
                remarks = col3.text_input("Remarks", value=prev_remarks, key=f"rem_{sid}")
                
                attendance_data.append({'student_id': sid, 'status': status, 'remarks': remarks})
                
            submit = st.form_submit_button("Save Attendance")
            if submit:
                try:
                    mark_attendance(session_id, attendance_data)
                    st.success("Attendance saved successfully!")
                except Exception as e:
                    st.error(f"Failed to save attendance: {e}")
    else:
        st.info("No students enrolled in this section.")
