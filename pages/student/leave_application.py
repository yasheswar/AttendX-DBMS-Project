import streamlit as st
from services.leave_service import get_leave_types, apply_for_leave, get_student_leaves
from utils.helpers import require_role
from utils.validators import is_valid_date_range
import pandas as pd

def show():
    require_role('STUDENT')
    st.header("Leave Applications")
    student_id = st.session_state.user['student_id']
    
    tab1, tab2 = st.tabs(["Apply for Leave", "Leave History"])
    
    with tab1:
        types = get_leave_types()
        if not types:
            st.warning("Leave types not configured.")
        else:
            with st.form("leave_apply_form"):
                type_opts = {t['leave_type_name']: t['leave_type_id'] for t in types}
                selected_type = st.selectbox("Leave Type", list(type_opts.keys()))
                
                col1, col2 = st.columns(2)
                start = col1.date_input("From Date")
                end = col2.date_input("To Date")
                
                reason = st.text_area("Reason")
                
                if st.form_submit_button("Submit Application"):
                    if is_valid_date_range(start, end) and reason:
                        try:
                            apply_for_leave(student_id, type_opts[selected_type], start, end, reason)
                            st.success("Leave application submitted successfully!")
                        except Exception as e:
                            st.error(f"Error submitting leave: {e}")
                    else:
                        st.error("Invalid dates or missing reason.")
                        
    with tab2:
        leaves = get_student_leaves(student_id)
        if leaves:
            st.dataframe(pd.DataFrame(leaves)[['leave_type_name', 'from_date', 'to_date', 'reason', 'application_status', 'submitted_at']], use_container_width=True)
        else:
            st.info("No leave history.")
