import streamlit as st
from services.faculty_service import get_all_faculty, search_faculty
from utils.helpers import require_role
import pandas as pd

def show():
    require_role('ADMIN')
    st.header("Faculty Management")
    
    search = st.text_input("Search Faculty")
    if search:
        faculty = search_faculty(search)
    else:
        faculty = get_all_faculty()
        
    if faculty:
        df = pd.DataFrame(faculty)
        st.dataframe(df[['faculty_code', 'first_name', 'last_name', 'department', 'designation', 'email']], use_container_width=True)
    else:
        st.info("No faculty found.")
