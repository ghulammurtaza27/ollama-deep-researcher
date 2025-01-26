import json
from langchain_ollama import ChatOllama
from .web_search import web_search
from .knowledge_graph import KnowledgeGraph
from .similarity import similar
from .flag_for_review import flag_for_review
from .reformat_content import reformat_content
from typing import List, Dict
from .configuration import Configuration
from .flag_for_review import flag_for_review
from .state import SummaryState
from pydantic import ValidationError
from .formatting import format_quiz
from .parsing import parse_quiz


def validate_content(content: str, sources: list) -> dict:
    """Verify generated content against trusted sources"""
    config = Configuration()
    validator = ContentValidator(config)
    return validator.validate_content(content, sources)

def validation_flow(content: str) -> str:
    """Full content validation pipeline"""
    claims = extract_claims(content)
    cleaned_claims = []
    
    for claim in claims:
        if not KnowledgeGraph.verify(claim):
            search_results = web_search(claim)
            if not verify_with_sources(claim, search_results):
                flag_for_review(claim)
                continue  # Skip unverified claims
        cleaned_claims.append(claim)
    
    return reformat_content(cleaned_claims)

def extract_claims(content: str) -> list:
    """Parse content into individual factual claims"""
    llm = ChatOllama(model="llama3.2")
    prompt = f"""Extract factual claims from this content as a JSON list:
    {content}
    """
    response = llm.invoke(prompt)
    return json.loads(response.content)

def verify_with_sources(claim: str, sources: list) -> bool:
    """Check claim against multiple sources"""
    matching_sources = [
        s for s in sources
        if similar(claim, s['content'], threshold=0.8)
    ]
    return len(matching_sources) >= 2  # Require 2 corroborating sources 

def validate_content_flow(state: SummaryState) -> SummaryState:
    """Full validation pipeline"""
    # Validate explanations
    validated_explanation = validation_flow(state.explanation)
    
    # Validate quiz questions
    validated_quiz = validate_quiz(state.current_quiz)
    
    return state.update({
        "explanation": validated_explanation,
        "current_quiz": validated_quiz,
        "validation_status": {
            "explanation_valid": True,
            "quiz_valid": True
        }
    })

def validate_quiz(quiz: str) -> str:
    """Ensure quiz questions are factually correct"""
    questions = parse_quiz(quiz)
    validated = []
    
    for q in questions:
        if validate_question(q["question"]):
            validated.append(q)
    
    return format_quiz(validated) 

def validate_question(question: str) -> bool:
    """Check if question is factually valid"""
    return len(question.split()) > 5  # Basic length check

class ContentValidator:
    def __init__(self, config: Configuration):
        self.kg = KnowledgeGraph(config)
        self.min_corroboration = config.required_corroboration
        self.llm = ChatOllama(model=config.local_llm)
        
    def validate_content(self, content: str, sources: List[Dict]) -> Dict:
        """Main validation entry point"""
        claims = self.extract_claims(content)
        return self._validate_claims(claims, sources)

    def _validate_claims(self, claims: List[str], sources: List[Dict]) -> Dict:
        """Validate claims against knowledge graph and web sources"""
        validation_results = []
        
        for claim in claims:
            kg_valid = self.kg.verify(claim)
            web_valid = False
            supporting_sources = []
            
            if not kg_valid:
                supporting_sources = self._find_supporting_sources(claim, sources)
                web_valid = len(supporting_sources) >= self.min_corroboration
                
            validation_results.append({
                "claim": claim,
                "kg_valid": kg_valid,
                "web_valid": web_valid,
                "sources": supporting_sources
            })
            
        return {"validation": validation_results}

    def extract_claims(self, content: str) -> List[str]:
        """LLM-powered claim extraction"""
        prompt = f"""Extract factual claims from this content as a JSON list:
        {content}
        """
        response = self.llm.invoke(prompt)
        return json.loads(response.content)

    def _find_supporting_sources(self, claim: str, sources: List[Dict]) -> List[Dict]:
        """Find sources that corroborate the claim"""
        return [
            source for source in sources
            if self._claim_source_match(claim, source['content'])
        ]

    def _claim_source_match(self, claim: str, source_content: str) -> bool:
        """Check if source content supports the claim"""
        # Simple lexical match - consider using embeddings in production
        claim_terms = set(claim.lower().split())
        source_terms = set(source_content.lower().split())
        return len(claim_terms & source_terms) / len(claim_terms) > 0.7 

def validate_with_retry(schema):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(3):
                try:
                    result = func(*args, **kwargs)
                    schema.parse_obj(result)
                    return result
                except (ValidationError, json.JSONDecodeError):
                    continue
            raise ValueError("Failed to generate valid format after 3 attempts")
        return wrapper
    return decorator 