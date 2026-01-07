"""
Agent 工作流定义
"""
from langgraph.graph import StateGraph, END

from .state import AgentState
from .content_generator import generate_content_node
from .cover_generator import generate_cover_node


def build_graph() -> StateGraph:
    """构建 LangGraph 工作流"""
    workflow = StateGraph(AgentState)

    workflow.add_node("generate_content", generate_content_node)
    workflow.add_node("generate_cover", generate_cover_node)

    workflow.set_entry_point("generate_content")
    workflow.add_edge("generate_content", "generate_cover")
    workflow.add_edge("generate_cover", END)

    return workflow.compile()
