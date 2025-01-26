from datetime import datetime, timedelta
from .state import SummaryState

class Scheduler:
    def __init__(self):
        self.review_intervals = [1, 3, 7, 14]  # Days between reviews
    
    def update_schedule(self, state: SummaryState) -> None:
        """Update learning schedule based on spaced repetition"""
        if not state.last_reviewed:
            state.next_review = datetime.now() + timedelta(days=1)
            return
        
        current_level = min(
            len(self.review_intervals) - 1,
            state.review_level or 0
        )
        
        interval = self.review_intervals[current_level]
        state.next_review = datetime.now() + timedelta(days=interval)
        state.review_level = current_level + 1
    
    def get_due_topics(self, state: SummaryState) -> list:
        """Return topics due for review"""
        return [
            topic for topic, due_date in state.schedule.items()
            if due_date <= datetime.now()
        ] 