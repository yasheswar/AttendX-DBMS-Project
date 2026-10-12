import streamlit as st
from services.student_service import get_student_attendance_summary, get_student_alerts
from utils.helpers import require_role, format_percentage
from config.database import execute_query
import pandas as pd
import plotly.express as px

def show():
    require_role('STUDENT')
    st.header(f"🎓 Welcome, {st.session_state.user['name']}")
    student_id = st.session_state.user['student_id']
    
    summary = get_student_attendance_summary(student_id)
    alerts = get_student_alerts(student_id)
    
    # Check pending leave count
    leave_query = "SELECT COUNT(*) as cnt FROM leave_applications WHERE student_id = %s AND application_status = 'PENDING'"
    pending_leaves = execute_query(leave_query, (student_id,), fetch_one=True)
    pending_cnt = pending_leaves['cnt'] if pending_leaves else 0

    col1, col2, col3 = st.columns(3)
    overall_pct = sum([float(s['attendance_percentage']) for s in summary]) / len(summary) if summary else 0.0
    
    delta_text = "Safe" if overall_pct >= 75 else "Action Needed (<75%)"
    delta_color = "normal" if overall_pct >= 75 else "inverse"
    col1.metric("Cumulative Attendance", format_percentage(overall_pct), delta=delta_text, delta_color=delta_color)
    col2.metric("Active Shortage Alerts", len(alerts) if alerts else 0, delta="Attention" if alerts else "None", delta_color="inverse" if alerts else "normal")
    col3.metric("Pending Leaves", pending_cnt)
    
    if alerts:
        st.error(f"⚠️ You have {len(alerts)} active shortage alert(s). Review your course attendance immediately!")
        with st.expander("🔔 View Urgent Alerts", expanded=True):
            for a in alerts:
                st.warning(f"**{a['course_name']}**: {a['message']}")
    
    st.markdown("---")
    
    st.subheader("📚 Enrolled Courses & Standing")
    if summary:
        df_sum = pd.DataFrame(summary)
        
        # Modern Card layout
        cols = st.columns(len(summary))
        for i, s in enumerate(summary):
            pct = float(s['attendance_percentage'])
            border_color = '#10B981' if pct >= 75 else ('#F59E0B' if pct >= 65 else '#EF4444')
            with cols[i % len(cols)]:
                st.markdown(f"""
                <div style='padding: 16px; border-radius: 10px; border-left: 6px solid {border_color}; background-color: #1e293b; color: white; margin-bottom: 15px;'>
                    <span style='font-size: 0.85em; background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 4px;'>{s['course_code']}</span>
                    <h4 style='margin: 8px 0 4px 0; color: #f8fafc;'>{s['course_name']}</h4>
                    <h2 style='margin: 0; color: {border_color};'>{format_percentage(pct)}</h2>
                    <p style='margin: 4px 0 0 0; font-size: 0.85em; color: #94a3b8;'>{s['attended_sessions']} of {s['total_completed_sessions']} classes attended</p>
                </div>
                """, unsafe_allow_html=True)
                
        # Radar/Bar Chart for quick visual check
        fig = px.bar(
            df_sum, 
            x="course_code", 
            y="attendance_percentage", 
            color="attendance_percentage",
            title="My Attendance Profile",
            color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
            range_y=[0, 100],
            text_auto='.1f'
        )
        fig.add_hline(y=75, line_dash="dash", line_color="#EF4444", annotation_text="Mandatory 75% Cut-off")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No course enrollment found.")
