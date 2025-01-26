# AI Learning Companion

**AI Learning Companion** is an adaptive educational platform that helps students master any topic through personalized learning paths, interactive explanations, and continuous assessment. Built with local LLMs via Ollama, it provides:

- **Personalized Learning Paths** - Break down complex topics into manageable steps
- **Multimodal Explanations** - Text, visual diagrams, and audio explanations
- **Adaptive Assessments** - Automatic quiz generation and progress tracking
- **Knowledge Validation** - Fact-checking against trusted sources
- **Spaced Repetition** - Optimized review scheduling for long-term retention


## Key Features

- **Diagnostic Testing** - Assess starting knowledge level
- **Interactive Tutoring** - Ask questions, get step-by-step explanations
- **Gamified Learning** - Earn badges and track progress
- **Remediation System** - Alternative explanations for struggling students
- **Cross-Device Sync** - Continue learning on any device

## 🚀 Quick Start

1. **Install Requirements**
```bash
ollama pull llama3.2
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
export LOCAL_LLM=llama3.2
export DIFFICULTY_LEVEL=high_school
```

3. **Launch Learning Companion**
```bash
python -m src.main
```

4. **Start Learning**
```python
What would you like to learn today? quantum physics
Student ID: student123
```

## How It Works

1. **Topic Analysis**  
   The system breaks down your topic into core concepts using knowledge graphs

2. **Adaptive Content Generation**  
   Generates explanations matched to your learning level (elementary to college)

3. **Interactive Assessment**  
   Regular quizzes identify knowledge gaps

4. **Personalized Remediation**  
   Provides alternative explanations and practice problems

5. **Progress Tracking**  
   Visual dashboard shows mastery over time

## Development Setup

```bash
git clone https://github.com/yourrepo/ai-learning-companion.git
cd ai-learning-companion
uv pip install -r requirements.txt
```

## Contributing

We welcome contributions! Please see our [Contribution Guidelines](CONTRIBUTING.md) for details.


