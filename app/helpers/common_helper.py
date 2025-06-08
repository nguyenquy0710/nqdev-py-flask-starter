from datetime import datetime


def format_datetime_for_api(dt_value):
    """Convert datetime to string format for API response"""
    if isinstance(dt_value, str):
        return dt_value
    elif isinstance(dt_value, datetime):
        return dt_value.isoformat()
    else:
        return str(dt_value)
