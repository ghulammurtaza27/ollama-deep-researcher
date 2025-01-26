from .learning_path import generate_learning_path
from .content_generation import generate_adaptive_content
from .assessment import create_quiz, assess_understanding
from .progress_tracker import ProgressTracker
from .validation import ContentValidator
from .scheduler import Scheduler
from .graph import build_learning_graph
from .services import OllamaService
from .knowledge_graph import WolframAlphaKnowledgeGraph
from .state import SummaryState
from .configuration import Configuration
from .reformat_content import reformat_content
from .diagnostics import run_diagnostic
from .delivery import deliver_to_student
from .reporting import final_report

def initialize_engine():
    # Create all components
    graph = build_learning_graph()
    tracker = ProgressTracker()
    validator = ContentValidator()
    scheduler = Scheduler()
    
    # Configure services
    llm_service = OllamaService()
    knowledge_graph = WolframAlphaKnowledgeGraph()
    
    return LearningEngine(
        graph=graph,
        tracker=tracker,
        validator=validator,
        scheduler=scheduler,
        llm=llm_service,
        knowledge_graph=knowledge_graph
    )

class LearningEngine:
    def __init__(self, config: Configuration):
        self.config = config
        self.tracker = ProgressTracker()
        self.validator = ContentValidator(config)
        
    def start_learning_session(self, topic: str, student_id: str) -> dict:
        """Start new learning session with required fields"""
        state = self.tracker.load_progress(student_id) or SummaryState(
            learning_topic=topic,
            knowledge_level="beginner"  # Default starting level
        )
        
        if not state.learning_path:
            state.learning_path = generate_learning_path(topic, self.config)
        
        content = generate_adaptive_content(state, self.config)
        return reformat_content(content, state)
    
    def _deliver_content(self, content):
        """Display learning materials"""
        print(f"\n# {content['title']}\n")
        print(content['explanation'])
        
    def _administer_quiz(self, quiz):
        """Handle quiz interaction"""
        print("\nQuiz Time!")
        for q in quiz['questions']:
            print(f"\n{q['question']}")
            print("Options: " + ", ".join(q['options']))
            
        return 1.0  # Temporary perfect score

    def learn(self, topic: str, student_id: str):
        # Full learning sequence
        state = self.tracker.load_state(student_id)
        
        if not state.diagnostic_complete:
            state = run_diagnostic(student_id)
            
        while not state.learning_complete:
            # Generate content
            content = generate_adaptive_content(state)
            
            # Validate accuracy
            validation = self.validator.check(content)
            
            # Deliver content
            deliver_to_student(content, state.preferred_modality)
            
            # Assess understanding
            if state.enable_quizzes:
                assess_understanding(state)
                
            # Update progress
            self.tracker.save_progress(student_id, state)
            
            # Schedule reviews
            self.scheduler.update_schedule(state)
            
        return final_report(state) 