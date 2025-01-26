import os
from dataclasses import dataclass, field, fields
from typing import Any, Optional, Literal

from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated
from dataclasses import dataclass
from pydantic import validate_call

@dataclass(kw_only=True)
class Configuration:
    """Educational configuration fields"""
    max_topics: int = field(default=5)
    difficulty_level: Literal['elementary', 'high_school', 'college'] = 'high_school'
    output_format: Literal['text', 'visual', 'audio'] = 'text'
    enable_quizzes: bool = True
    local_llm: str = "llama3.2"
    validation_enabled: bool = True
    required_corroboration: int = 2  # Minimum matching sources

    @validate_call
    def __post_init__(self):
        if self.max_topics < 1 or self.max_topics > 10:
            raise ValueError("max_topics must be between 1-10")

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})