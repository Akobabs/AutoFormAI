import re
from typing import Optional

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_name(name: str) -> bool:
    """Validate name format"""
    if not name or len(name) < 1 or len(name) > 100:
        return False
    
    # Allow letters, spaces, hyphens, apostrophes
    pattern = r"^[a-zA-Z\s\-']+$"
    return bool(re.match(pattern, name))

def validate_suggestion(text: str) -> bool:
    """Validate suggestion text"""
    if not text or not isinstance(text, str):
        return False
    
    text = text.strip()
    if len(text) < 1 or len(text) > 255:
        return False
    
    # Check if it's email or name
    return validate_email(text) or validate_name(text)

def validate_prefix(prefix: str) -> bool:
    """Validate search prefix"""
    if not isinstance(prefix, str):
        return False
    
    prefix = prefix.strip()
    if len(prefix) > 50:  # Reasonable limit
        return False
    
    # Allow empty prefix for popular suggestions
    return True

def sanitize_input(text: str) -> Optional[str]:
    """Sanitize user input"""
    if not isinstance(text, str):
        return None
    
    # Remove potentially harmful characters
    text = re.sub(r'[<>"\']', '', text)
    text = text.strip()
    
    return text if text else None