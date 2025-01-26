import json

def parse_quiz(quiz_str: str) -> list:
    """Convert quiz string to structured format"""
    try:
        return json.loads(quiz_str)
    except json.JSONDecodeError:
        return [] 