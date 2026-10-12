import streamlit as st
from services.student_service import get_all_students, search_students
from utils.helpers import require_role
import pandas as pd

def show():
    require_role('ADMIN')
    st.header("Student Management")
    
    tab1, tab2 = st.tabs(["View Students", "Add Student"])
    
    with tab1:
        search = st.text_input("Search Students (Name, Reg No, Email)")
        if search:
            students = search_students(search)
        else:
            students = get_all_students()
            
        if students:
            df = pd.DataFrame(students)
            st.dataframe(df[['registration_number', 'first_name', 'last_name', 'department', 'semester', 'email']], use_container_width=True)
        else:
            st.info("No students found.")
            
    with tab2:
        st.write("### Add New Student")
        with st.form("add_student_form"):
            reg_no = st.text_input("Registration Number")
            fname = st.text_input("First Name")
            lname = st.text_input("Last Name")
            email = st.text_input("Email")
            dept = st.selectbox("Department", ["Computer Science", "Information Technology", "Electronics"])
            sem = st.number_input("Semester", 1, 8, 1)
            
            submit = st.form_submit_button("Add Student")
            if submit:
                st.warning("For full implementation, we need to create a User account first and map user_id. Add backend logic here.")
                # This requires user creation logic first
