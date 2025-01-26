import json
from chat_ollama import ChatOllama
from config import Configuration

def generate_learning_path(topic: str, config: Configuration) -> list:
    """Generate structured learning path for a topic"""
    llm = ChatOllama(model=config.local_llm)
    prompt = f"""Break down '{topic}' into 5-7 core subtopics ordered by learning priority.
    Format as JSON: {{"subtopics": ["subtopic1", "subtopic2"]}}"""
    
    response = llm.invoke(prompt)
    subtopics = json.loads(response.content)["subtopics"]
    return subtopics 