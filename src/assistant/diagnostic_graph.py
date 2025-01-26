from langgraph.graph import MessageGraph, END
from .diagnostic_nodes import generate_diagnostic_quiz, grade_diagnostic

def build_diagnostic_graph():
    graph = MessageGraph()
    graph.add_node("generate_quiz", generate_diagnostic_quiz)
    graph.add_node("grade_quiz", grade_diagnostic)
    graph.set_entry_point("generate_quiz")
    graph.add_edge("generate_quiz", "grade_quiz")
    graph.add_edge("grade_quiz", END)
    return graph.compile() 