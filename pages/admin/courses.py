import streamlit as st
from config.database import execute_query
from utils.helpers import require_role
import pandas as pd

def show():
    require_role('ADMIN')
    st.header("📚 Course & Offering Management")
    
    tab1, tab2 = st.tabs(["Courses Master", "Course Offerings (Ternary Relationship)"])
    
    with tab1:
        st.subheader("All University Courses")
        courses = execute_query("SELECT * FROM courses", fetch_all=True)
        if courses:
            st.dataframe(pd.DataFrame(courses)[['course_code', 'course_name', 'credits', 'department']], use_container_width=True)
            
        with st.expander("➕ Add New Course"):
            with st.form("new_course_form"):
                c_code = st.text_input("Course Code (e.g. CS401)")
                c_name = st.text_input("Course Name")
                credits = st.number_input("Credits", min_value=1, max_value=6, value=4)
                dept = st.selectbox("Department", ["Computer Science", "Information Technology", "Electronics", "Mechanical"])
                if st.form_submit_button("Add Course"):
                    if c_code and c_name:
                        try:
                            execute_query(
                                "INSERT INTO courses (course_code, course_name, credits, department) VALUES (%s, %s, %s, %s)",
                                (c_code.upper().strip(), c_name.strip(), credits, dept),
                                commit=True
                            )
                            st.success("Course added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error adding course: {e}")
                    else:
                        st.warning("Please fill in all fields.")

    with tab2:
        st.subheader("Active Course Offerings")
        st.caption("Demonstrating M:N associative entity mapping Courses, Sections, and Faculty.")
        offerings_query = """
            SELECT 
                co.offering_id,
                c.course_code,
                c.course_name,
                sec.section_name,
                CONCAT(f.first_name, ' ', f.last_name) AS faculty_name,
                co.academic_year,
                co.semester
            FROM course_offerings co
            JOIN courses c ON co.course_id = c.course_id
            JOIN sections sec ON co.section_id = sec.section_id
            JOIN faculty f ON co.faculty_id = f.faculty_id
        """
        offerings = execute_query(offerings_query, fetch_all=True)
        if offerings:
            st.dataframe(pd.DataFrame(offerings), use_container_width=True)
