from langchain_ollama import ChatOllama
from .configuration import Configuration
from .state import SummaryState

class RemediationEngine:
    def __init__(self, config: Configuration):
        self.llm = ChatOllama(model=config.local_llm)
        self.max_attempts = 3
        
    def generate_alternative_explanation(self, original_content: str, misconceptions: list) -> str:
        """Create simplified explanation addressing specific gaps"""
        prompt = f"""Create an alternative explanation that addresses these misunderstandings:
        {misconceptions}
        
        Original content:
        {original_content}
        
        Use:
        - Simpler language
        - More examples
        - Step-by-step breakdown
        """
        return self.llm.invoke(prompt).content
    
    def create_practice_exercises(self, topic: str, difficulty: str) -> list:
        """Generate targeted practice problems"""
        prompt = f"""Create 3 {difficulty}-level practice exercises about {topic}.
        Include solutions."""
        return self.llm.invoke(prompt).content

def handle_remediation(state: SummaryState) -> dict:
    """Generate alternative learning materials"""
    llm = ChatOllama(model=state.config.local_llm)
    
    # Generate simplified explanation
    prompt = f"""Create a simplified version of this content for a student struggling with:
    {state.misconceptions}
    
    Original content:
    {state.explanation}"""
    
    simplified = llm.invoke(prompt).content
    
    # Create practice exercises
    practice_prompt = f"""Generate 2-3 practice exercises addressing:
    {state.knowledge_gaps}
    """
    exercises = llm.invoke(practice_prompt).content
    
    return {
        "simplified_explanation": simplified,
        "practice_exercises": exercises,
        "remediation_quiz": generate_remediation_quiz(state)
    }

def generate_remediation_quiz(state: SummaryState) -> str:
    """Create targeted quiz for knowledge gaps"""
    prompt = f"""Generate quiz questions focusing on:
    {state.knowledge_gaps}
    
    Use simple language and concrete examples."""
    
    llm = ChatOllama(model=state.config.local_llm)
    return llm.invoke(prompt).content 