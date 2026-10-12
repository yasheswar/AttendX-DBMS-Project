import streamlit as st
from services.faculty_service import get_faculty_courses
from services.attendance_service import create_session, get_sessions_by_offering
from utils.helpers import require_role
from utils.validators import is_valid_time_range
import pandas as pd

def show():
    require_role('FACULTY')
    st.header("Manage Class Sessions")
    fac_id = st.session_state.user['faculty_id']
    courses = get_faculty_courses(fac_id)
    
    if not courses:
        st.warning("You don't have any assigned courses.")
        return
        
    course_options = {f"{c['course_code']} - {c['section_name']}": c['offering_id'] for c in courses}
    selected_course = st.selectbox("Select Course", options=list(course_options.keys()))
    offering_id = course_options[selected_course]
    
    tab1, tab2 = st.tabs(["Create Session", "View Sessions"])
    
    with tab1:
        with st.form("create_session"):
            date = st.date_input("Session Date")
            col1, col2 = st.columns(2)
            start = col1.time_input("Start Time")
            end = col2.time_input("End Time")
            topic = st.text_input("Topic Covered")
            
            submit = st.form_submit_button("Create Session")
            if submit:
                if is_valid_time_range(start, end):
                    try:
                        create_session(offering_id, date, start, end, topic)
                        st.success("Session created successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Start time must be before end time.")
                    
    with tab2:
        sessions = get_sessions_by_offering(offering_id)
        if sessions:
            st.dataframe(pd.DataFrame(sessions)[['session_date', 'start_time', 'end_time', 'topic_covered', 'session_status']], use_container_width=True)
        else:
            st.info("No sessions recorded for this course.")
