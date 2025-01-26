from progress_tracker import ProgressTracker

def upgrade():
    tracker = ProgressTracker()
    tracker.conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            progress_data TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''') 