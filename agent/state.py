"""
Agent 状态定义
"""
from typing import TypedDict


class AgentState(TypedDict):
    """Agent 状态定义"""
    product: dict
    title: str
    content: str
    tags: list[str]
    cover_path: str
    error: str | None

