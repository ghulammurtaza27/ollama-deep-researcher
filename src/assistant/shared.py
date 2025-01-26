def convert_to_modality(content: dict, modality: str) -> dict:
    """Convert text content to specified modality"""
    return {
        "text": content,
        "visual": {"diagram": content['explanation']},
        "audio": {"text": content['explanation']}
    }[modality] 