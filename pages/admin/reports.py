import streamlit as st
from config.database import execute_query
from utils.helpers import require_role
import pandas as pd
import plotly.express as px

def show():
    require_role('ADMIN')
    st.header("📊 Analytical Reports & Insights")
    st.caption("Real-time aggregation driven by database views, stored procedures, and triggers")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Course Attendance", 
        "⚠️ Shortage Analysis", 
        "📝 Leave Audit Trail", 
        "📅 Monthly Trends", 
        "⚡ DB Console & Queries"
    ])
    
    with tab1:
        st.subheader("Course Attendance Summary")
        data = execute_query("SELECT * FROM vw_course_attendance_summary", fetch_all=True)
        if data:
            df = pd.DataFrame(data)
            
            # Interactive Chart
            fig = px.bar(
                df, 
                x="course_name", 
                y="average_attendance", 
                color="average_attendance",
                color_continuous_scale="Viridis",
                title="Average Attendance by Course (%)",
                labels={"average_attendance": "Avg Attendance (%)", "course_name": "Course"},
                text_auto='.1f'
            )
            fig.update_layout(xaxis_tickangle=-25)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No course summary data found.")
            
    with tab2:
        st.subheader("Attendance Shortage & Critical Risk Report")
        data = execute_query("SELECT * FROM vw_attendance_shortage WHERE shortage_level != 'GOOD'", fetch_all=True)
        if data:
            df = pd.DataFrame(data)
            
            col1, col2 = st.columns(2)
            critical_count = len(df[df['shortage_level'] == 'CRITICAL_SHORTAGE'])
            shortage_count = len(df[df['shortage_level'] == 'SHORTAGE'])
            
            col1.error(f"🚨 Critical Shortage (<65%): {critical_count} Students")
            col2.warning(f"⚠️ Warning Shortage (65%-75%): {shortage_count} Students")
            
            fig = px.pie(
                df, 
                names="shortage_level", 
                title="Shortage Severity Distribution",
                color="shortage_level",
                color_discrete_map={"CRITICAL_SHORTAGE": "#EF4444", "SHORTAGE": "#F59E0B"}
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.success("🎉 All enrolled students meet or exceed minimum attendance thresholds!")
            
    with tab3:
        st.subheader("Leave Applications & Approval Audit Trail")
        data = execute_query("SELECT * FROM vw_leave_history ORDER BY application_id DESC", fetch_all=True)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            # Breakdown by leave type
            fig = px.histogram(
                df, 
                x="leave_type_name", 
                color="application_status",
                barmode="group",
                title="Leave Applications by Type & Resolution",
                color_discrete_map={"APPROVED": "#10B981", "REJECTED": "#EF4444", "PENDING": "#F59E0B"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No leave history records logged yet.")

    with tab4:
        st.subheader("Monthly Attendance Trends")
        data = execute_query("SELECT * FROM vw_monthly_attendance_trends", fetch_all=True)
        if data:
            df = pd.DataFrame(data)
            fig = px.line(
                df,
                x="month",
                y="attendance_percentage",
                color="course_name",
                markers=True,
                title="Month-over-Month Attendance Fluctuation (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Monthly trends will become active as session history accumulates.")

    with tab5:
        st.subheader("DBMS Viva Query Evaluator & Stored Procedure Runner")
        st.caption("Demonstrate live SQL execution, Views, and Stored Procedures directly to your professor!")
        
        proc_choice = st.selectbox(
            "Select an Academic Stored Procedure to Execute:",
            ["None", "sp_get_student_summary (Procedure with Subqueries)", "Custom SQL Sandbox"]
        )
        
        if proc_choice == "sp_get_student_summary (Procedure with Subqueries)":
            st_id = st.number_input("Enter Student ID to inspect:", min_value=1, value=1, step=1)
            if st.button("Execute Stored Procedure `CALL sp_get_student_summary(?)`", type="primary"):
                res = execute_query("CALL sp_get_student_summary(%s)", (st_id,), fetch_all=True)
                if res:
                    st.success("Stored Procedure executed successfully via MySQL Server!")
                    st.json(res)
                else:
                    st.warning("No record returned for this Student ID.")
                    
        elif proc_choice == "Custom SQL Sandbox":
            sql_query = st.text_area(
                "Enter SELECT Query for Viva evaluation:",
                value="SELECT * FROM vw_attendance_shortage LIMIT 10;"
            )
            if st.button("Run SQL Query", type="primary"):
                try:
                    res = execute_query(sql_query, fetch_all=True)
                    if res:
                        st.dataframe(pd.DataFrame(res), use_container_width=True)
                    else:
                        st.info("Query returned 0 rows.")
                except Exception as err:
                    st.error(f"SQL Error: {err}")
