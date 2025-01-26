import operator
from dataclasses import dataclass, field
from typing_extensions import TypedDict, Annotated

@dataclass(kw_only=True)
class SummaryState:
    research_topic: str = field(default=None) # Report topic     
    search_query: str = field(default=None) # Search query
    web_research_results: Annotated[list, operator.add] = field(default_factory=list) 
    sources_gathered: Annotated[list, operator.add] = field(default_factory=list) 
    research_loop_count: int = field(default=0) # Research loop count
    running_summary: str = field(default=None) # Final report
    learning_topic: str = field(default=None)
    current_subtopic: str = field(default=None)
    learning_path: list = field(default_factory=list)
    completed_topics: Annotated[list, operator.add] = field(default_factory=list)
    quiz_scores: dict = field(default_factory=dict)
    explanation_history: Annotated[list, operator.add] = field(default_factory=list)
    preferred_format: str = "text"
    knowledge_gaps: list = field(default_factory=list)
    misconceptions: dict = field(default_factory=dict)
    learning_objectives: list = field(default_factory=list)
    difficulty_level: str = "high_school"
    preferred_modality: str = "text"
    review_schedule: dict = field(default_factory=dict)

    def update(self, new_data: dict):
        for key, value in new_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

@dataclass(kw_only=True)
class SummaryStateInput(TypedDict):
    research_topic: str = field(default=None) # Report topic     

@dataclass(kw_only=True)
class SummaryStateOutput(TypedDict):
    running_summary: str = field(default=None) # Final report