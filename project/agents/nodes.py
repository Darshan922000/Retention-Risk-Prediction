from project.instructor.instructions import email_instruction
from project.structure.schema import State
from project.llm.planner import emailai
from langchain_core.messages import SystemMessage, HumanMessage
from project.logging.logger import logging
from project.exception_handler.exception import Exception
import sys
import os
from dotenv import load_dotenv
load_dotenv()


# os.environ["LANGSMITH_TRACING"] = "true"
# os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
# os.environ["LANGSMITH_PROJECT"]=os.getenv("LANGSMITH_PROJECT")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


# Nodes
def email_ai(state: State):
    """AI agent that understand user query and generate string for news extraction"""
    logging.info("Entered in node email_ai")
    try:
        response = emailai.invoke(
            [
            SystemMessage(content=email_instruction),
            HumanMessage(
                content=f"Here is the user query: {state['input_data']}"
            ),
        ]
    )

        return {"response": response}
    except Exception as e:
        raise Exception(e, sys)
