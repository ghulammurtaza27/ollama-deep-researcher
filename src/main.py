from assistant.engine import LearningEngine
from assistant.configuration import Configuration
from assistant.progress_tracker import ProgressTracker

def main():
    config = Configuration()
    tracker = ProgressTracker()
    engine = LearningEngine(config=config, tracker=tracker)
    
    while True:
        topic = input("What would you like to learn today? ")
        student_id = input("Student ID: ")
        
        engine.start_learning_session(topic, student_id)
        
        if input("Continue learning? (y/n) ").lower() != 'y':
            break

if __name__ == "__main__":
    main() 