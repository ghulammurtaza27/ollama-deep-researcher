def generate_adaptive_content(state: SummaryState, config: Configuration) -> dict:
    """Generate content tailored to student's needs"""
    base_content = graph.invoke({
        "current_subtopic": state.current_subtopic,
        "difficulty_level": state.difficulty_level
    }, config)
    
    if state.needs_remediation:
        return generate_remediation_content(base_content, state)
    
    if state.preferred_modality != "text":
        return convert_to_modality(base_content, state.preferred_modality)
    
    return base_content

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