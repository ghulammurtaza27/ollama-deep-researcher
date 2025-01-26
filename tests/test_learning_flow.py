import pytest
from assistant.engine import LearningEngine
from assistant.configuration import Configuration

@pytest.fixture
def test_engine():
    config = Configuration(local_llm="llama3.2")
    return LearningEngine(config=config)

def test_basic_learning_flow(test_engine):
    result = test_engine.start_learning_session("photosynthesis", "test_student")
    assert "summary" in result
    assert len(result["quiz"]) > 0 