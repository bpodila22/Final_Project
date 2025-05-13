# utils.py

import re
import uuid
from datetime import datetime

def is_valid_date(date_string):
    """Validate date format as YYYY-MM-DD"""
    try:
        if not isinstance(date_string, str):
            return False
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_string):
            return False
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def generate_visit_id(existing_ids):
    """Generate a unique visit ID"""
    attempts = 100
    existing = set(str(i) for i in existing_ids)
    for _ in range(attempts):
        candidate = uuid.uuid4().hex[:8].upper()
        if candidate not in existing:
            return candidate
    raise RuntimeError("Unable to generate a unique Visit ID")
