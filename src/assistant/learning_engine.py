from .progress_tracker import ProgressTracker
from .spaced_repetition import Scheduler, handle_reviews
from .graph import graph
from .learning_path import generate_learning_path
from .validation import validate_content_flow

def learning_flow(topic: str, student_id: str, config: Configuration):
    # Initialize components
    tracker = ProgressTracker()
    scheduler = Scheduler()
    
    # Load existing progress
    state = load_student_state(tracker, student_id)
    
    # Generate or continue learning path
    if not state.learning_path:
        state.learning_path = generate_learning_path(topic, config)
    
    # Main learning loop
    while state.current_subtopic in state.learning_path:
        # Generate content
        result = graph.invoke({
            "learning_topic": topic,
            "current_subtopic": state.current_subtopic,
            **state.__dict__
        }, config)
        
        # Add validation step
        validated_state = validate_content_flow(
            state.update(result)
        )
        
        # Update with validated content
        state = validated_state
        
        # Store progress
        tracker.save_progress(student_id, state)
        
        # Schedule reviews
        if state.current_subtopic in state.quiz_scores:
            scheduler.add_review(
                state.current_subtopic,
                state.quiz_scores[state.current_subtopic]
            )
        
        # Check for due reviews
        handle_reviews(scheduler, state, tracker)

def load_student_state(tracker: ProgressTracker, student_id: str) -> SummaryState:
    """Load or initialize student state"""
    raw = tracker.conn.execute(
        'SELECT progress_data FROM students WHERE id = ?',
        (student_id,)
    ).fetchone()
    
    if raw:
        return SummaryState(**json.loads(raw[0]))
    return SummaryState() 