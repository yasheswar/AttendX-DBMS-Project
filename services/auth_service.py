import hashlib
from config.database import execute_query

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 (Simplified for academic demonstration)."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(plain_password) == hashed_password

def authenticate_user(username, password):
    """
    Authenticate a user.
    Returns user dict if successful, None otherwise.
    """
    query = "SELECT user_id, username, password_hash, role, is_active FROM users WHERE username = %s"
    user = execute_query(query, (username,), fetch_one=True)
    
    if user and user['is_active']:
        if verify_password(password, user['password_hash']):
            # Fetch specific profile based on role
            profile_info = {}
            if user['role'] == 'ADMIN':
                profile_info = {'name': 'Administrator'}
            elif user['role'] == 'FACULTY':
                q = "SELECT faculty_id, first_name, last_name, department FROM faculty WHERE user_id = %s"
                fac = execute_query(q, (user['user_id'],), fetch_one=True)
                if fac:
                    profile_info = {
                        'faculty_id': fac['faculty_id'],
                        'name': f"{fac['first_name']} {fac['last_name']}",
                        'department': fac['department']
                    }
            elif user['role'] == 'STUDENT':
                q = "SELECT student_id, registration_number, first_name, last_name FROM students WHERE user_id = %s"
                stu = execute_query(q, (user['user_id'],), fetch_one=True)
                if stu:
                    profile_info = {
                        'student_id': stu['student_id'],
                        'registration_number': stu['registration_number'],
                        'name': f"{stu['first_name']} {stu['last_name']}"
                    }
            
            user.update(profile_info)
            del user['password_hash'] # Do not return hash
            return user
    return None

def create_user(username, password, role):
    """Create a new user."""
    hashed = hash_password(password)
    query = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"
    execute_query(query, (username, hashed, role), commit=True)
    
    # Get created user id
    q_id = "SELECT user_id FROM users WHERE username = %s"
    user = execute_query(q_id, (username,), fetch_one=True)
    return user['user_id'] if user else None
