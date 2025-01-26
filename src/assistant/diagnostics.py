def run_diagnostic(student_id: str, config: Configuration):
    """Assess student's starting level"""
    state = load_student_state(student_id)
    
    diagnostic_quiz = graph.invoke({
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