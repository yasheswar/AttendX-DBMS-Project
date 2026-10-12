import streamlit as st
from services.auth_service import authenticate_user

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AttendX - Attendance Management",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'user' not in st.session_state:
    st.session_state.user = None

def logout():
    st.session_state.user = None
    st.success("You have been logged out.")
    st.rerun()

# --- ROUTING LOGIC ---
if st.session_state.user is None:
    # Login Page
    st.title("🎓 AttendX")
    st.subheader("Smart Student Attendance & Leave Management")
    
    with st.container():
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.write("### Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", type="primary", use_container_width=True):
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success(f"Welcome {user.get('name', username)}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            
            st.markdown("---")
            st.info("""
            **Demo Credentials:**
            * Admin: `admin` / `Admin@123`
            * Faculty: `faculty1` / `Faculty@123`
            * Student: `student1` / `Student@123`
            """)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Authenticated Layout
    role = st.session_state.user['role']
    name = st.session_state.user.get('name', st.session_state.user['username'])
    
    with st.sidebar:
        st.write(f"### 👤 {name}")
        st.caption(f"Role: **{role}**")
        st.button("Logout", on_click=logout, use_container_width=True)
        st.divider()
        st.write("### Navigation")
        
        if role == 'ADMIN':
            page = st.radio("Go to", ["Dashboard", "Students", "Faculty", "Courses", "Sections", "Reports"])
        elif role == 'FACULTY':
            page = st.radio("Go to", ["Dashboard", "My Sessions", "Mark Attendance", "Leave Approvals", "Makeup Sessions"])
        elif role == 'STUDENT':
            page = st.radio("Go to", ["Dashboard", "My Attendance", "Apply Leave", "Alerts"])

    # Load appropriate page based on selection
    if role == 'ADMIN':
        if page == "Dashboard":
            import pages.admin.dashboard as p
            p.show()
        elif page == "Students":
            import pages.admin.students as p
            p.show()
        elif page == "Faculty":
            import pages.admin.faculty as p
            p.show()
        elif page == "Courses":
            import pages.admin.courses as p
            p.show()
        elif page == "Sections":
            import pages.admin.sections as p
            p.show()
        elif page == "Reports":
            import pages.admin.reports as p
            p.show()
            
    elif role == 'FACULTY':
        if page == "Dashboard":
            import pages.faculty.dashboard as p
            p.show()
        elif page == "My Sessions":
            import pages.faculty.sessions as p
            p.show()
        elif page == "Mark Attendance":
            import pages.faculty.attendance as p
            p.show()
        elif page == "Leave Approvals":
            import pages.faculty.leave_approval as p
            p.show()
        elif page == "Makeup Sessions":
            import pages.faculty.makeup_sessions as p
            p.show()
            
    elif role == 'STUDENT':
        if page == "Dashboard":
            import pages.student.dashboard as p
            p.show()
        elif page == "My Attendance":
            import pages.student.attendance as p
            p.show()
        elif page == "Apply Leave":
            import pages.student.leave_application as p
            p.show()
        elif page == "Alerts":
            import pages.student.alerts as p
            p.show()
