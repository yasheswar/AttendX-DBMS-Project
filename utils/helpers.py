import streamlit as st

def check_authentication():
    """Check if user is authenticated. Redirects to login if not."""
    if 'user' not in st.session_state or st.session_state.user is None:
        st.warning("Please log in to access this page.")
        st.stop()
        return False
    return True

def require_role(role):
    """Check if authenticated user has the required role."""
    if check_authentication():
        if st.session_state.user.get('role') != role:
            st.error(f"Access Denied. You must be an {role} to view this page.")
            st.stop()
            return False
        return True
    return False

def format_percentage(value):
    """Format a decimal value to percentage string."""
    if value is None:
        return "0.00%"
    return f"{float(value):.2f}%"

def get_shortage_color(shortage_level):
    """Return color hex based on shortage level."""
    if shortage_level == 'GOOD':
        return '#28a745' # Green
    elif shortage_level == 'SHORTAGE':
        return '#ffc107' # Yellow
    elif shortage_level == 'CRITICAL_SHORTAGE':
        return '#dc3545' # Red
    return '#6c757d'
