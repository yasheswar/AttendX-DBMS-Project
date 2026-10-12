import streamlit as st
from services.report_service import get_dashboard_metrics
from services.alert_service import check_and_generate_alerts
from utils.helpers import require_role, format_percentage

def show():
    require_role('ADMIN')
    st.header("Admin Dashboard")
    
    # Run alert generator in background
    try:
        check_and_generate_alerts()
    except Exception as e:
        st.error(f"Error checking alerts: {e}")

    metrics = get_dashboard_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", metrics['total_students'])
    col2.metric("Total Faculty", metrics['total_faculty'])
    col3.metric("Total Courses", metrics['total_courses'])
    col4.metric("Total Sessions", metrics['total_sessions'])
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Attendance", format_percentage(metrics['avg_attendance']))
    col2.metric("Shortage Students", metrics['shortage_students'])
    col3.metric("Pending Leaves", metrics['pending_leaves'])
    
    st.write("### Quick Actions")
    cols = st.columns(4)
    if cols[0].button("Manage Students", use_container_width=True):
        st.info("Navigate using the sidebar")
    if cols[1].button("Manage Faculty", use_container_width=True):
        st.info("Navigate using the sidebar")
    if cols[2].button("View Reports", use_container_width=True):
        st.info("Navigate using the sidebar")
