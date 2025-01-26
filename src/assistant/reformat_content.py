from .state import SummaryState

def reformat_content(content: list, state: SummaryState) -> str:
    """Format validated content for output"""
    formatted = []
    
    for item in content:
        if item['kg_valid'] or item['web_valid']:
            formatted.append(f"✅ {item['claim']}")
        else:
            formatted.append(f"⚠️ {item['claim']} (needs verification)")
    
    return "\n".join(formatted) 