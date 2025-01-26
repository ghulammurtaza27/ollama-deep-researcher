import json
from langchain_ollama import ChatOllama
from .configuration import Configuration
from json import JSONDecodeError

def generate_learning_path(topic: str, config: Configuration) -> dict:
    """Generate adaptive learning path with error handling"""
    llm = ChatOllama(model=config.local_llm)
    
    prompt = f"""Create a learning path for {topic} with 5 subtopics.
    Format as JSON list of strings."""
    
    try:
        response = llm.invoke(prompt)
        return json.loads(response.content)
    except JSONDecodeError:
        print("⚠️ Failed to parse LLM response as JSON")
        return {"error": "Invalid response format", "path": []}
    except Exception as e:
        print(f"Learning path generation error: {e}")
        return {"error": str(e), "path": []} 