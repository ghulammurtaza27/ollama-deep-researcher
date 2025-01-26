from datetime import datetime, timedelta

class Scheduler:
    def __init__(self):
        self.schedule = {}
    
    def add_review(self, topic: str, score: float):
        if score < 0.7:
            interval = 1  # Review next day
        elif score < 0.9:
            interval = 3  # Review in 3 days
        else:
            interval = 7  # Review in a week
            
        self.schedule[topic] = datetime.now() + timedelta(days=interval)
    
    def get_due_reviews(self):
        return [topic for topic, date in self.schedule.items() if date <= datetime.now()] 