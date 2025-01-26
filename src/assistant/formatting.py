def format_quiz(questions: list) -> str:
    """Convert validated questions to quiz format"""
    return "\n".join(
        f"{i+1}. {q['question']}\n   Options: {q['options']}"
        for i, q in enumerate(questions)
    ) 