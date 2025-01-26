import sqlite3
import json

class ProgressTracker:
    def __init__(self):
        self.conn = sqlite3.connect('progress.db')
        self._create_tables()
    
    def _create_tables(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            progress_data TEXT
        )''')
    
    def save_progress(self, student_id: str, state: SummaryState):
        data = json.dumps({
            "completed_topics": state.completed_topics,
            "quiz_scores": state.quiz_scores
        })
        self.conn.execute('''
            INSERT OR REPLACE INTO students VALUES (?, ?)
        ''', (student_id, data))
        self.conn.commit()

    def get_progress_report(self, student_id: str) -> dict:
        """Generate comprehensive progress report"""
        state = self.load_student_state(student_id)
        
        return {
            "completed_topics": state.completed_topics,
            "quiz_scores": state.quiz_scores,
            "knowledge_gaps": state.knowledge_gaps,
            "learning_path_progress": {
                "total": len(state.learning_path),
                "completed": len(state.completed_topics)
            },
            "recommended_next_steps": state.recommendations
        }

    def generate_learning_report(self, state: SummaryState) -> str:
        """Create human-readable progress report"""
        report = f"""
        Learning Report for {state.learning_topic}
        =========================================
        
        Progress: {len(state.completed_topics)}/{len(state.learning_path)} topics
        Average Quiz Score: {sum(state.quiz_scores.values())/len(state.quiz_scores):.1%}
        
        Current Focus: {state.current_subtopic}
        Knowledge Gaps: {', '.join(state.knowledge_gaps) or 'None identified'}
        
        Recommendations:
        {state.recommendations}
        """
        return report 