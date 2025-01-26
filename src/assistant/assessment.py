import json
from typing import Dict
from langchain_ollama import ChatOllama
from .configuration import Configuration

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

def grade_quiz(answers: list, correct: list) -> float:
    """Calculate quiz score percentage"""
    correct_count = sum(1 for a, c in zip(answers, correct) if a == c)
    return correct_count / len(correct)

def generate_feedback(score: float, misconceptions: list) -> str:
    """Generate personalized feedback based on performance"""
    if score >= 0.8:
        return "Great job! You've mastered this concept."
    else:
        return f"Let's review these areas: {', '.join(misconceptions)}"

def create_quiz(topic: str, config: Configuration) -> dict:
    """Generate quiz questions using LLM"""
    llm = ChatOllama(model=config.local_llm)
    
    prompt = f"""Create 3 multiple-choice questions about {topic}.
    Format as JSON with 'questions' list containing:
    - question: str
    - options: list[str]
    - correct_answer: str"""
    
    response = llm.invoke(prompt)
    return json.loads(response.content)

def assess_understanding(state):
    """Administer quiz and update state"""
    # Placeholder quiz logic
    state.quiz_scores["latest"] = 0.85
    print("\n✅ Quiz completed - Score: 85%") 