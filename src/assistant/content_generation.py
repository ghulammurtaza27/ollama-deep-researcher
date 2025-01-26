from .state import SummaryState
from .configuration import Configuration
from .shared import convert_to_modality
from .graph import build_learning_graph

def generate_adaptive_content(state: SummaryState, config: Configuration) -> dict:
    """Generate content based on learning path"""
    graph = build_learning_graph()
    return graph.invoke({
        "topic": state.learning_topic,
        "knowledge_level": state.knowledge_level,
        "config": config
    })

def generate_remediation_content(base: dict, state: SummaryState) -> dict:
    """Create alternative explanations for struggling students"""
    llm = ChatOllama(model=state.config.local_llm)
    prompt = f"""Create a simplified explanation of: {base['explanation']}
    Address these specific misunderstandings: {state.misconceptions}
    Use analogies and interactive examples."""
    
    return {
        "explanation": llm.invoke(prompt).content,
        "remediation": True,
        "original_content": base
    } 