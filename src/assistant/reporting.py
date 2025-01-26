from .state import SummaryState

def final_report(state: SummaryState) -> dict:
    """Generate end-of-session report"""
    return {
        "completed_topics": state.learning_path,
        "quiz_scores": state.quiz_scores,
        "knowledge_level": state.knowledge_level
    } 