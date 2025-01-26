from .state import SummaryState

def load_student_state(student_id: str) -> SummaryState:
    """Load or initialize student progress"""
    return SummaryState(
        learning_topic="new_student",
        knowledge_level="beginner"
    ) 