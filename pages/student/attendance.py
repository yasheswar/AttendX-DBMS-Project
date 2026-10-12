import streamlit as st
from config.database import execute_query
from utils.helpers import require_role
import pandas as pd
import plotly.express as px

def show():
    require_role('STUDENT')
    st.header("📋 My Attendance Analytics & Detailed History")
    student_id = st.session_state.user['student_id']
    
    # 1. Course summary with visual progress bars
    st.subheader("Current Attendance Standing by Course")
    summary_query = """
        SELECT course_code, course_name, total_completed_sessions, attended_sessions, attendance_percentage
        FROM vw_student_attendance_percentage
        WHERE student_id = %s
    """
    summaries = execute_query(summary_query, (student_id,), fetch_all=True)
    
    if summaries:
        df_sum = pd.DataFrame(summaries)
        
        # Display responsive cards/metrics
        cols = st.columns(len(df_sum))
        for i, row in df_sum.iterrows():
            with cols[i % len(cols)]:
                pct = float(row['attendance_percentage'])
                status_color = "normal" if pct >= 75 else "inverse"
                st.metric(
                    label=f"{row['course_code']}",
                    value=f"{pct:.1f}%",
                    delta=f"{row['attended_sessions']}/{row['total_completed_sessions']} classes",
                    delta_color=status_color
                )
                st.progress(min(max(pct / 100.0, 0.0), 1.0))
                
        # Interactive comparison chart
        fig = px.bar(
            df_sum, 
            x="course_code", 
            y="attendance_percentage",
            title="Course-wise Attendance (%)",
            labels={"attendance_percentage": "Attendance %", "course_code": "Course"},
            color="attendance_percentage",
            color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
            range_y=[0, 100],
            text_auto='.1f'
        )
        # Add target line at 75%
        fig.add_hline(y=75, line_dash="dash", line_color="#EF4444", annotation_text="Minimum Threshold (75%)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No course enrollment records found.")

    st.markdown("---")
    
    # 2. Detailed Session Logs with filtering
    st.subheader("Session-by-Session Breakdown")
    query = """
        SELECT 
            c.course_code, 
            c.course_name, 
            cs.session_date, 
            cs.topic_covered, 
            a.attendance_status, 
            IFNULL(a.remarks, '-') AS remarks,
            a.marked_at
        FROM attendance a
        JOIN class_sessions cs ON a.session_id = cs.session_id
        JOIN course_offerings co ON cs.offering_id = co.offering_id
        JOIN courses c ON co.course_id = c.course_id
        WHERE a.student_id = %s
        ORDER BY cs.session_date DESC, cs.start_time DESC
    """
    records = execute_query(query, (student_id,), fetch_all=True)
    
    if records:
        df_records = pd.DataFrame(records)
        
        col_filter1, col_filter2 = st.columns(2)
        course_filter = col_filter1.multiselect("Filter by Course", options=df_records['course_code'].unique())
        status_filter = col_filter2.multiselect("Filter by Status", options=df_records['attendance_status'].unique())
        
        filtered_df = df_records
        if course_filter:
            filtered_df = filtered_df[filtered_df['course_code'].isin(course_filter)]
        if status_filter:
            filtered_df = filtered_df[filtered_df['attendance_status'].isin(status_filter)]
            
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No recorded attendance sessions yet.")
