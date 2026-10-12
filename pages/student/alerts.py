import streamlit as st
from services.student_service import get_student_alerts
from utils.helpers import require_role
from services.alert_service import resolve_alert

def show():
    require_role('STUDENT')
    st.header("My Alerts")
    student_id = st.session_state.user['student_id']
    
    alerts = get_student_alerts(student_id)
    
    if not alerts:
        st.success("You have no active alerts. Great job!")
        return
        
    for a in alerts:
        color = "error" if a['alert_type'] == 'CRITICAL_SHORTAGE' else "warning"
        st.markdown(f"**{a['course_name']}**")
        if color == "error":
            st.error(f"{a['message']} (Generated: {a['generated_at']})")
        else:
            st.warning(f"{a['message']} (Generated: {a['generated_at']})")
