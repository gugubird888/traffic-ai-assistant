from typing import TypedDict


class AgentState(TypedDict):
    """Agent 工作流状态"""
    query: str  # 用户问题
    intent: str  # 意图类型
    context: str  # 检索到的法条
    answer: str  # 最终回答
