def generate_diagnostic_quiz(state: dict) -> dict:
    return {
        "quiz": {
            "questions": [
                {
                    "text": "What is the basic unit of life?",
                    "options": ["Cell", "Atom", "Molecule", "Organ"],
                    "answer": "Cell"
                }
            ]
        }
    }

def grade_diagnostic(state: dict) -> dict:
    return {"score": 0.85} 