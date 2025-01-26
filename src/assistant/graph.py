import json

from typing_extensions import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph

from assistant.configuration import Configuration
from assistant.utils import deduplicate_and_format_sources, tavily_search, format_sources
from assistant.state import SummaryState, SummaryStateInput, SummaryStateOutput
from assistant.prompts import query_writer_instructions, summarizer_instructions, reflection_instructions, quiz_generator_instructions, recommendation_instructions

# Nodes   
def generate_query(state: SummaryState, config: RunnableConfig):
    """Generate search query for research phase
    
    Args:
        state: Current learning state containing research topic
        config: Runtime configuration
        
    Returns:
        dict: Contains generated search query
    """
    
    # Format the prompt
    query_writer_instructions_formatted = query_writer_instructions.format(research_topic=state.research_topic)

    # Generate a query
    configurable = Configuration.from_runnable_config(config)
    llm_json_mode = ChatOllama(model=configurable.local_llm, temperature=0, format="json")
    result = llm_json_mode.invoke(
        [SystemMessage(content=query_writer_instructions_formatted),
        HumanMessage(content=f"Generate a query for web search:")]
    )   
    query = json.loads(result.content)
    
    return {"search_query": query['query']}

def web_research(state: SummaryState):
    """ Gather information from the web """
    
    # Search the web
    search_results = tavily_search(state.search_query, include_raw_content=True, max_results=1)
    
    # Format the sources
    search_str = deduplicate_and_format_sources(search_results, max_tokens_per_source=1000)
    return {"sources_gathered": [format_sources(search_results)], "research_loop_count": state.research_loop_count + 1, "web_research_results": [search_str]}

def summarize_sources(state: SummaryState, config: RunnableConfig):
    """ Summarize the gathered sources """
    
    # Existing summary
    existing_summary = state.running_summary

    # Most recent web research
    most_recent_web_research = state.web_research_results[-1]

    # Build the human message
    if existing_summary:
        human_message_content = (
            f"Extend the existing summary: {existing_summary}\n\n"
            f"Include new search results: {most_recent_web_research} "
            f"That addresses the following topic: {state.research_topic}"
        )
    else:
        human_message_content = (
            f"Generate a summary of these search results: {most_recent_web_research} "
            f"That addresses the following topic: {state.research_topic}"
        )

    # Run the LLM
    configurable = Configuration.from_runnable_config(config)
    llm = ChatOllama(model=configurable.local_llm, temperature=0)
    result = llm.invoke(
        [SystemMessage(content=summarizer_instructions),
        HumanMessage(content=human_message_content)]
    )

    running_summary = result.content

    # TODO: This is a hack to remove the <think> tags w/ Deepseek models 
    # It appears very challenging to prompt them out of the responses 
    while "<think>" in running_summary and "</think>" in running_summary:
        start = running_summary.find("<think>")
        end = running_summary.find("</think>") + len("</think>")
        running_summary = running_summary[:start] + running_summary[end:]

    return {"running_summary": running_summary}

def reflect_on_summary(state: SummaryState, config: RunnableConfig):
    """ Reflect on the summary and generate a follow-up query """

    # Generate a query
    configurable = Configuration.from_runnable_config(config)
    llm_json_mode = ChatOllama(model=configurable.local_llm, temperature=0, format="json")
    result = llm_json_mode.invoke(
        [SystemMessage(content=reflection_instructions.format(research_topic=state.research_topic)),
        HumanMessage(content=f"Identify a knowledge gap and generate a follow-up web search query based on our existing knowledge: {state.running_summary}")]
    )   
    follow_up_query = json.loads(result.content)

    # Overwrite the search query
    return {"search_query": follow_up_query['follow_up_query']}

def finalize_summary(state: SummaryState):
    """ Finalize the summary """
    
    # Format all accumulated sources into a single bulleted list
    all_sources = "\n".join(source for source in state.sources_gathered)
    state.running_summary = f"## Summary\n\n{state.running_summary}\n\n ### Sources:\n{all_sources}"
    return {"running_summary": state.running_summary}

def route_research(state: SummaryState, config: RunnableConfig) -> Literal["finalize_summary", "web_research"]:
    """ Route the research based on the follow-up query """

    configurable = Configuration.from_runnable_config(config)
    if state.research_loop_count <= configurable.max_web_research_loops:
        return "web_research"
    else:
        return "finalize_summary" 

def generate_explanation(state: SummaryState, config: RunnableConfig):
    """Generate student-friendly explanation"""
    configurable = Configuration.from_runnable_config(config)
    prompt = f"Explain {state.current_subtopic} at {configurable.difficulty_level} level"
    llm = ChatOllama(model=configurable.local_llm)
    explanation = llm.invoke(prompt)
    return {"explanation": explanation.content}

def create_quiz(state: SummaryState, config: RunnableConfig):
    """Generate comprehension quiz"""
    configurable = Configuration.from_runnable_config(config)
    llm = ChatOllama(model=configurable.local_llm)
    quiz = llm.invoke(quiz_generator_instructions.format(topic=state.current_subtopic))
    return {"current_quiz": quiz.content}

def recommend_topics(state: SummaryState, config: RunnableConfig):
    """Suggest next learning steps"""
    configurable = Configuration.from_runnable_config(config)
    llm = ChatOllama(model=configurable.local_llm)
    recs = llm.invoke(recommendation_instructions.format(
        current_topic=state.current_subtopic,
        completed_topics=state.completed_topics,
        quiz_scores=state.quiz_scores
    ))
    return {"recommendations": recs.content}

def update_progress(state: SummaryState):
    """Track student progress"""
    return {
        "completed_topics": [*state.completed_topics, state.current_subtopic],
        "learning_path": [*state.learning_path, state.current_subtopic]
    }

def adapt_content(state: SummaryState, config: RunnableConfig):
    """Adjust content based on student performance"""
    if state.quiz_scores.get(state.current_subtopic, 0) < 0.7:
        return {"needs_remediation": True}
    return {"needs_remediation": False}

def generate_learning_path(topic: str, config: Configuration) -> list:
    """Generate structured learning path for a topic"""
    llm = ChatOllama(model=config.local_llm)
    prompt = f"""Break down '{topic}' into 5-7 core subtopics ordered by learning priority.
    Format as JSON: {{"subtopics": ["subtopic1", "subtopic2"]}}"""
    
    response = llm.invoke(prompt)
    subtopics = json.loads(response.content)["subtopics"]
    return subtopics

def grade_quiz(response: dict, correct_answers: dict) -> float:
    """Calculate quiz score and provide feedback"""
    score = 0
    for question, answer in response.items():
        if answer == correct_answers.get(question):
            score += 1
    return score / len(correct_answers)

def provide_feedback(score: float, misconceptions: list) -> str:
    """Generate personalized feedback based on performance"""
    if score >= 0.8:
        return "Great job! You've mastered this concept."
    else:
        return f"Let's review these areas: {', '.join(misconceptions)}"

# Add nodes and edges 
builder = StateGraph(SummaryState, input=SummaryStateInput, output=SummaryStateOutput, config_schema=Configuration)
builder.add_node("generate_query", generate_query)
builder.add_node("web_research", web_research)
builder.add_node("summarize_sources", summarize_sources)
builder.add_node("reflect_on_summary", reflect_on_summary)
builder.add_node("finalize_summary", finalize_summary)
builder.add_node("generate_explanation", generate_explanation)
builder.add_node("create_quiz", create_quiz)
builder.add_node("recommend_topics", recommend_topics)
builder.add_node("update_progress", update_progress)
builder.add_node("generate_learning_path", generate_learning_path)
builder.add_node("adapt_content", adapt_content)
builder.add_node("grade_quiz", grade_quiz)
builder.add_node("provide_feedback", provide_feedback)

# Add edges
builder.add_edge(START, "generate_query")
builder.add_edge("generate_query", "web_research")
builder.add_edge("web_research", "summarize_sources")
builder.add_edge("summarize_sources", "reflect_on_summary")
builder.add_conditional_edges("reflect_on_summary", route_research)
builder.add_edge("finalize_summary", END)
builder.add_edge("reflect_on_summary", "generate_explanation")
builder.add_edge("reflect_on_summary", "create_quiz")
builder.add_edge("reflect_on_summary", "recommend_topics")
builder.add_edge("generate_explanation", "update_progress")
builder.add_edge("create_quiz", "grade_quiz")
builder.add_edge("grade_quiz", "provide_feedback")
builder.add_edge("provide_feedback", "adapt_content")
builder.add_conditional_edges("adapt_content", 
    lambda s: "remediate" if s.get("needs_remediation") else "recommend_topics")

graph = builder.compile()