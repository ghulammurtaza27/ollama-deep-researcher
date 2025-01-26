class LearningEngineError(Exception):
    """Base error class"""
    
class ValidationError(LearningEngineError):
    """Content validation failed"""
    
class RemediationNeeded(LearningEngineError):
    """Student requires remediation"""
    
class KnowledgeGapError(LearningEngineError):
    """Critical knowledge gap detected""" 