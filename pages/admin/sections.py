import streamlit as st
from config.database import execute_query
from utils.helpers import require_role
import pandas as pd

def show():
    require_role('ADMIN')
    st.header("🏫 Section & Enrollment Management")
    
    tab1, tab2 = st.tabs(["Sections List", "Student-Section Enrollments"])
    
    with tab1:
        st.subheader("Academic Sections")
        sections = execute_query("SELECT * FROM sections", fetch_all=True)
        if sections:
            st.dataframe(pd.DataFrame(sections)[['section_name', 'semester', 'academic_year', 'department']], use_container_width=True)
            
        with st.expander("➕ Create New Section"):
            with st.form("new_sec_form"):
                s_name = st.text_input("Section Name (e.g. CS-B)")
                sem = st.number_input("Semester", min_value=1, max_value=8, value=5)
                acad_year = st.text_input("Academic Year", value="2023-2024")
                dept = st.selectbox("Department", ["Computer Science", "Information Technology", "Electronics", "Mechanical"])
                if st.form_submit_button("Create Section"):
                    if s_name:
                        try:
                            execute_query(
                                "INSERT INTO sections (section_name, semester, academic_year, department) VALUES (%s, %s, %s, %s)",
                                (s_name.strip(), sem, acad_year.strip(), dept),
                                commit=True
                            )
                            st.success("Section created successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error creating section: {e}")
                            
    with tab2:
        st.subheader("Student Enrollment Mapping (`student_section`)")
        st.caption("Demonstrating M:N associative entity mapping Students to Sections.")
        enrollments = execute_query("""
            SELECT 
                ss.student_section_id,
                s.registration_number,
                CONCAT(s.first_name, ' ', s.last_name) AS student_name,
                sec.section_name,
                sec.department,
                ss.academic_year
            FROM student_section ss
            JOIN students s ON ss.student_id = s.student_id
            JOIN sections sec ON ss.section_id = sec.section_id
            ORDER BY sec.section_name, s.registration_number
        """, fetch_all=True)
        if enrollments:
            st.dataframe(pd.DataFrame(enrollments), use_container_width=True)
