from .configuration import Configuration
from .storage import load_student_state
from .assessment import grade_quiz
from .diagnostic_graph import build_diagnostic_graph

def run_diagnostic(student_id: str) -> dict:
    """Run full diagnostic flow"""
    graph = build_diagnostic_graph()
    return graph.invoke({"student_id": student_id})

def run_diagnostic_with_config(student_id: str, config: Configuration):
    """Assess student's starting level"""
    state = load_student_state(student_id)
    
    diagnostic_quiz = build_diagnostic_graph().invoke({
        "learning_topic": "diagnostic",
        "current_subtopic": "diagnostic",
        "quiz_type": "pretest"
    }, config)
    
    score = grade_quiz(
        diagnostic_quiz['answers'],
        diagnostic_quiz['correct_answers']
    )
    
    # Set initial difficulty level
    if score < 0.4:
        state.difficulty_level = "elementary"
    elif score < 0.7:
        state.difficulty_level = "high_school"
    else:
        state.difficulty_level = "college"
    
    return state 