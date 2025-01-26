from .state import SummaryState
from datetime import datetime

def flag_for_review(claim: str, state: SummaryState) -> None:
    """Flag unverified claims for human review"""
    state.flagged_claims.append({
        "claim": claim,
        "timestamp": datetime.now().isoformat()
    }) 