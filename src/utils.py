"""
src/utils.py
------------
Utility helpers for input validation and formatting.
"""

def sanitize_input(text):
    """Sanitizes user input string."""
    if not text:
        return ""
    return str(text).strip()

def format_score(score):
    """Formats numeric score to 2 decimal string representation."""
    try:
        return f"{float(score):.2f}"
    except (ValueError, TypeError):
        return "0.00"
