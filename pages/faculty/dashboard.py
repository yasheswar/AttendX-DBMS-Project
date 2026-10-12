import streamlit as st
from services.faculty_service import get_faculty_courses
from utils.helpers import require_role
from config.database import execute_query
import pandas as pd
import plotly.express as px

def show():
    require_role('FACULTY')
    st.header("👨‍🏫 Faculty Control Center")
    fac_id = st.session_state.user['faculty_id']
    
    courses = get_faculty_courses(fac_id)
    
    # 1. Real-time Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Assigned Offerings", len(courses) if courses else 0)
    
    # Total sessions conducted
    sess_query = """
        SELECT COUNT(cs.session_id) as total_sessions
        FROM class_sessions cs
        JOIN course_offerings co ON cs.offering_id = co.offering_id
        WHERE co.faculty_id = %s AND cs.session_status = 'COMPLETED'
    """
    total_sess = execute_query(sess_query, (fac_id,), fetch_one=True)
    col2.metric("Completed Classes", total_sess['total_sessions'] if total_sess else 0)
    
    # Pending Leaves for enrolled students
    leaves_query = """
        SELECT COUNT(DISTINCT la.application_id) as pending_cnt 
        FROM leave_applications la 
        JOIN students s ON la.student_id = s.student_id 
        JOIN student_section ss ON s.student_id = ss.student_id 
        JOIN course_offerings co ON ss.section_id = co.section_id 
        WHERE co.faculty_id = %s AND la.application_status = 'PENDING'
    """
    leaves = execute_query(leaves_query, (fac_id,), fetch_one=True)
    pending_count = leaves['pending_cnt'] if leaves else 0
    col3.metric("Pending Leaves", pending_count, delta="Action Required" if pending_count > 0 else "All cleared", delta_color="inverse" if pending_count > 0 else "normal")
    
    # Shortage students in faculty's classes
    shortage_query = """
        SELECT COUNT(DISTINCT v.student_id) as shortage_cnt
        FROM vw_attendance_shortage v
        JOIN course_offerings co ON v.course_code = co.course_id OR v.offering_id = co.offering_id
        WHERE co.faculty_id = %s AND v.shortage_level != 'GOOD'
    """
    shortage_res = execute_query(shortage_query, (fac_id,), fetch_one=True)
    shortage_cnt = shortage_res['shortage_cnt'] if shortage_res else 0
    col4.metric("At-Risk Students", shortage_cnt, delta="Warning" if shortage_cnt > 0 else "Optimal", delta_color="inverse" if shortage_cnt > 0 else "normal")
    
    st.markdown("---")
    
    # 2. Offerings Overview & Attendance Health
    st.subheader("📚 My Assigned Course Offerings")
    if courses:
        df_courses = pd.DataFrame(courses)
        st.dataframe(df_courses[['course_code', 'course_name', 'section_name', 'semester']], use_container_width=True)
        
        # Course Health Chart
        health_query = """
            SELECT 
                c.course_code,
                sec.section_name,
                ROUND(AVG(v.attendance_percentage), 1) as avg_attendance
            FROM course_offerings co
            JOIN courses c ON co.course_id = c.course_id
            JOIN sections sec ON co.section_id = sec.section_id
            LEFT JOIN vw_student_attendance_percentage v ON co.offering_id = v.offering_id
            WHERE co.faculty_id = %s
            GROUP BY co.offering_id
        """
        health_data = execute_query(health_query, (fac_id,), fetch_all=True)
        if health_data and any(d['avg_attendance'] is not None for d in health_data):
            df_health = pd.DataFrame(health_data)
            fig = px.bar(
                df_health, 
                x="course_code", 
                y="avg_attendance", 
                color="avg_attendance",
                title="Class Attendance Standing Across Your Courses (%)",
                color_continuous_scale="RdYlGn",
                range_y=[0, 100],
                text_auto=True
            )
            fig.add_hline(y=75, line_dash="dash", line_color="red", annotation_text="University 75% Min")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No courses assigned yet.")
