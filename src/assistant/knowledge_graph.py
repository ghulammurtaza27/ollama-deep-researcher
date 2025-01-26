import json
from sentence_transformers import SentenceTransformer
import numpy as np
from .configuration import Configuration

class KnowledgeGraph:
    def __init__(self, config: Configuration):
        self.config = config
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = self._load_base_knowledge()
        self.embeddings = self.model.encode(self.knowledge_base)
        
    def _load_base_knowledge(self) -> list:
        """Load educational facts from file"""
        with open('data/base_knowledge.json') as f:
            return json.load(f)
    
    def verify(self, claim: str, threshold=0.7) -> bool:
        """Check claim against knowledge base using semantic similarity"""
        claim_embed = self.model.encode(claim)
        similarities = np.dot(self.embeddings, claim_embed)
        return np.max(similarities) > threshold
    
    def add_fact(self, fact: str):
        """Dynamically expand knowledge base"""
        self.knowledge_base.append(fact)
        self.embeddings = np.vstack([self.embeddings, self.model.encode(fact)])

class WolframAlphaKnowledgeGraph:
    def __init__(self):
        self.base_knowledge = [...]  # Add base facts 