import streamlit as st
from services.leave_service import get_pending_leaves_for_faculty, process_leave_application
from utils.helpers import require_role
import pandas as pd

def show():
    require_role('FACULTY')
    st.header("Leave Approvals")
    fac_id = st.session_state.user['faculty_id']
    
    pending = get_pending_leaves_for_faculty(fac_id)
    
    if not pending:
        st.info("No pending leave applications.")
        return
        
    for app in pending:
        with st.expander(f"{app['registration_number']} - {app['first_name']} {app['last_name']} ({app['leave_type_name']})"):
            st.write(f"**Dates:** {app['from_date']} to {app['to_date']}")
            st.write(f"**Reason:** {app['reason']}")
            
            with st.form(f"leave_form_{app['application_id']}"):
                remarks = st.text_input("Remarks")
                col1, col2 = st.columns(2)
                approve = col1.form_submit_button("Approve")
                reject = col2.form_submit_button("Reject")
                
                if approve:
                    process_leave_application(app['application_id'], fac_id, 'APPROVED', remarks)
                    st.success("Leave Approved")
                    st.rerun()
                elif reject:
                    process_leave_application(app['application_id'], fac_id, 'REJECTED', remarks)
                    st.warning("Leave Rejected")
                    st.rerun()
