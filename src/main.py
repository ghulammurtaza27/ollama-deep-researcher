from src.assistant.engine import LearningEngine
from src.assistant.configuration import Configuration
from src.assistant.progress_tracker import ProgressTracker
import os

def main():
    # Initialize configuration properly
    config = Configuration(
        local_llm="llama3",  # Explicitly set model
        tavily_api_key=os.getenv("TAVILY_API_KEY", "")
    )
    
    tracker = ProgressTracker()
    engine = LearningEngine(config)
    
    while True:
        topic = input("What would you like to learn today? ")
        student_id = input("Student ID: ")
        
        # Start learning session
        result = engine.start_learning_session(topic, student_id)
        
        print(f"\nLearning Summary:")
        print(f"- Completed Topics: {len(result.completed_topics)}")
        print(f"- Current Score: {result.quiz_scores.get('latest', 0):.0%}")
        
        if input("\nContinue learning? (y/n) ").lower() != 'y':
            break

if __name__ == "__main__":
    main() 