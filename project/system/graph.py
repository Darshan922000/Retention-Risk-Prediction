from project.structure.schema import State
from project.agents.nodes import email_ai
from langgraph.graph import StateGraph, START, END


def email_generator():
    # Build workflow
    builder = StateGraph(State)

    # Add the nodes
    builder.add_node("email_ai", email_ai)

    # Add edges to connect nodes
    builder.add_edge(START, "email_ai")
    builder.add_edge("email_ai", END)

    # Compile the workflow
    graph = builder.compile()

    return graph

email = email_generator()




