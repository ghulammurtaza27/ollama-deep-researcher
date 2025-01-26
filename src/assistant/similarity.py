import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def similar(text1: str, text2: str, threshold=0.7) -> bool:
    """Check semantic similarity between two texts"""
    emb1 = model.encode(text1)
    emb2 = model.encode(text2)
    similarity = np.dot(emb1, emb2)
    return similarity > threshold 