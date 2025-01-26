import operator
from dataclasses import dataclass, field
from typing import List, Dict, Optional, TypedDict, Annotated
from datetime import datetime
from .configuration import Configuration

@dataclass
class SummaryState:
    """Main application state"""
    # Required fields first
    learning_topic: str
    knowledge_level: str
    
    # Fields with defaults follow
    research_topic: str = field(default=None) # Report topic     
    search_query: str = field(default=None) # Search query
    web_research_results: Annotated[list, operator.add] = field(default_factory=list) 
    sources_gathered: Annotated[list, operator.add] = field(default_factory=list) 
    research_loop_count: int = field(default=0) # Research loop count
    running_summary: str = field(default=None) # Final report
    current_subtopic: str = field(default=None)
    learning_path: List[str] = field(default_factory=list)
    completed_topics: List[str] = field(default_factory=list)
    quiz_scores: Dict[str, float] = field(default_factory=dict)
    explanation_history: List[str] = field(default_factory=list)
    preferred_format: str = "text"
    misconceptions: dict = field(default_factory=dict)
    learning_objectives: list = field(default_factory=list)
    difficulty_level: str = "high_school"
    preferred_modality: str = "text"
    review_schedule: dict = field(default_factory=dict)
    knowledge_gaps: List[str] = field(default_factory=list)
    flagged_claims: List[dict] = field(default_factory=list)
    schedule: Dict[str, datetime] = field(default_factory=dict)
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None
    review_level: int = 0

    def update(self, new_data: dict):
        for key, value in new_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

class SummaryStateInput(TypedDict):
    learning_topic: Optional[str]
    current_subtopic: Optional[str]
    learning_path: List[str]
    completed_topics: List[str]
    quiz_scores: Dict[str, float]
    explanation_history: List[str]
    preferred_format: str

class SummaryStateOutput(TypedDict):
    running_summary: str

@dataclass
class LearningState:
    """Tracks state of learning session"""
    topic: str
    config: Configuration  # Add config to state
    knowledge_level: str = "beginner"
    generated_content: str = ""
    validation_status: str = "pending"
    learning_path: List[str] = field(default_factory=list)
    quiz_scores: Dict[str, float] = field(default_factory=dict)
    current_step: int = 0