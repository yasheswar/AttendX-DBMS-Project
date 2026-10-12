import re
from datetime import datetime

def is_valid_email(email):
    """Validate email format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    """Validate phone number (basic validation)."""
    return phone.isdigit() and 10 <= len(phone) <= 15

def is_valid_date_range(start_date, end_date):
    """Ensure start date is before or equal to end date."""
    if not start_date or not end_date:
        return False
    return start_date <= end_date

def is_valid_time_range(start_time, end_time):
    """Ensure start time is before end time."""
    if not start_time or not end_time:
        return False
    return start_time < end_time

def validate_required_fields(fields_dict):
    """Check if any required fields are empty."""
    empty_fields = [k for k, v in fields_dict.items() if not v or (isinstance(v, str) and not v.strip())]
    return len(empty_fields) == 0, empty_fields
