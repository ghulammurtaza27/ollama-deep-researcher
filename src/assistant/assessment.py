import json
from typing import Dict

def parse_quiz_response(response: str) -> Dict:
    """Parse LLM quiz response into structured format"""
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"questions": [], "answers": {}}

def calculate_metrics(answers: Dict, correct: Dict) -> Dict:
    """Calculate learning metrics from quiz results"""
    total = len(correct)
    correct_count = sum(1 for q,a in answers.items() if a == correct.get(q))
    
    return {
        "score": correct_count / total,
        "weak_areas": [q for q,a in answers.items() if a != correct.get(q)],
        "mastered": correct_count == total
    }

def grade_quiz(response: dict, correct_answers: dict) -> float:
    """Calculate quiz score and provide feedback"""
    score = 0
    for question, answer in response.items():
        if answer == correct_answers.get(question):
            score += 1
    return score / len(correct_answers)

def generate_feedback(score: float, misconceptions: list) -> str:
    """Generate personalized feedback based on performance"""
    if score >= 0.8:
        return "Great job! You've mastered this concept."
    else:
        return f"Let's review these areas: {', '.join(misconceptions)}" 