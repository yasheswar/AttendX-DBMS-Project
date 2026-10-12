import streamlit as st
from services.faculty_service import get_faculty_courses
from services.attendance_service import get_sessions_by_offering, create_makeup_session
from utils.helpers import require_role

def show():
    require_role('FACULTY')
    st.header("Makeup Sessions")
    fac_id = st.session_state.user['faculty_id']
    
    courses = get_faculty_courses(fac_id)
    if not courses:
        st.warning("No courses assigned.")
        return
        
    course_opts = {f"{c['course_code']} ({c['section_name']})": c['offering_id'] for c in courses}
    offering_id = course_opts[st.selectbox("Select Course", list(course_opts.keys()))]
    
    sessions = get_sessions_by_offering(offering_id)
    if not sessions:
        st.info("No original sessions found to create makeup for.")
        return
        
    session_opts = {f"[{s['session_status']}] {s['session_date']} {s['start_time']}": s['session_id'] for s in sessions if s['session_status'] in ('CANCELLED', 'COMPLETED')}
    
    if not session_opts:
        st.info("No eligible sessions for makeup.")
        return
        
    orig_session_id = session_opts[st.selectbox("Select Original Session", list(session_opts.keys()))]
    
    with st.form("makeup_form"):
        st.write("### New Makeup Session Details")
        date = st.date_input("Makeup Date")
        col1, col2 = st.columns(2)
        start = col1.time_input("Start Time")
        end = col2.time_input("End Time")
        reason = st.text_input("Reason for Makeup")
        
        if st.form_submit_button("Create Makeup Session"):
            if start < end:
                try:
                    create_makeup_session(orig_session_id, date, start, end, reason, fac_id)
                    st.success("Makeup session created successfully! Go to Mark Attendance to take attendance.")
                except Exception as e:
                    st.error(f"Failed to create makeup session: {e}")
            else:
                st.error("Start time must be before end time.")
