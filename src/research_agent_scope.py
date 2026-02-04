
"""User Clarification and Research Brief Generation.

This module implements the scoping phase of the research workflow, where we:
1. Assess if the user's request needs clarification
2. Generate a detailed research brief from the conversation

The workflow uses structured output to make deterministic decisions about
whether sufficient context exists to proceed with research.
"""
import os
from datetime import datetime
from typing_extensions import Literal

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, get_buffer_string
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langchain_openai import ChatOpenAI

from prompts import clarify_with_user_instructions, transform_messages_into_research_topic_prompt
from state_scope import AgentState, ClarifyWithUser, ResearchQuestion, AgentInputState

# ===== UTILITY FUNCTIONS =====


def get_today_str() -> str:
    """Get current date in a human-readable format."""
    now = datetime.now()
    return f"{now:%a %b} {now.day}, {now:%Y}"


model = ChatOpenAI(
    model="deepseek-v3.2", 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"), 
    temperature=0.0)


def clarify_with_user(state: AgentState) -> AgentState:
    """
    Determine if the user's request contains sufficient information to proceed with research.
    
    Uses structured output to make deterministic decisions and avoid hallucination.
    Routes to either research brief generation or ends with a clarification question.
    """

    structured_output_model = model.with_structured_output(ClarifyWithUser)

    response = structured_output_model.invoke(
        [HumanMessage(content=clarify_with_user_instructions.format(
            date=get_today_str(),
            messages=get_buffer_string(state["messages"])))
        ]
    )

    if response.need_clarification:
        return Command(
            goto=END,
            update={"messages":[AIMessage(content=response.question)]}
            )

    else:
        return Command(
            goto="write_research_brief",
            update={"messages":[AIMessage(content=response.verification)]}
            )

def write_research_brief(state: AgentState) -> AgentState:
    """
    Transform the conversation history into a comprehensive research brief.
    
    Uses structured output to ensure the brief follows the required format
    and contains all necessary details for effective research.
    """

    structured_output_model = model.with_structured_output(ResearchQuestion, method="json_mode")

    response = structured_output_model.invoke([
        HumanMessage(content=transform_messages_into_research_topic_prompt.format(
            date=get_today_str(),
            messages=get_buffer_string(state["messages"])))
    ])

    # Update state with generated research brief and pass it to the supervisor
    return {
        "research_brief": response.research_brief,
        "supervisor_messages": [HumanMessage(content=f"{response.research_brief}.")]
    }

# Build the scoping workflow
deep_research_builder = StateGraph(AgentState,              
input_schema=AgentInputState)

# Add workflow nodes
deep_research_builder.add_node("clarify_with_user", clarify_with_user)
deep_research_builder.add_node("write_research_brief", write_research_brief)

# Add workflow edges
deep_research_builder.add_edge(START, "clarify_with_user")
deep_research_builder.add_edge("write_research_brief", END)

# Compile the workflow
scope_research = deep_research_builder.compile()
