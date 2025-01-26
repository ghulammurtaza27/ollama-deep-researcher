from .validation import ContentValidator, validate_with_retry
from langchain_ollama import ChatOllama
from .state import LearningState
from .configuration import Configuration
import json
from pydantic import BaseModel
import re

def generate_content(state: LearningState) -> dict:
    """Generate learning content"""
    config = state.config  # Direct access
    llm = ChatOllama(
        model=config.local_llm,
        temperature=0.3  # More deterministic output
    )
    prompt = f"""Generate learning content about {state.topic} for {state.knowledge_level} level.
    Use EXACTLY this JSON format:
    {{
        "title": "string",
        "body": "string",
        "key_points": ["string1", "string2", "string3"]
    }}
    No markdown, only plain JSON."""
    
    @validate_with_retry(ContentSchema)
    def _generate(prompt: str) -> dict:
        response = llm.invoke(prompt)
        return parse_response(response.content)
        
    return _generate(prompt)

def validate_content(state: LearningState, config: Configuration) -> dict:
    """Validate generated content"""
    validator = ContentValidator(config)
    return {"validation_status": validator.validate(state.generated_content)}

def parse_response(content: str) -> dict:
    # Extract JSON from possible markdown
    json_str = re.search(r'\{.*\}', content, re.DOTALL).group()
    return json.loads(json_str)

class ContentSchema(BaseModel):
    title: str
    body: str
    key_points: list[str] 