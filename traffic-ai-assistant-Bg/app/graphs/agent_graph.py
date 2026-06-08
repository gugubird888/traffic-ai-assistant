from langgraph.graph import StateGraph, END

from app.graphs.state import AgentState
from app.graphs.nodes import classify_intent, retrieve_docs, generate_answer
from app.graphs.edges import route_by_intent


def build_agent_graph() -> StateGraph:
    """构建 LangGraph 工作流"""
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("classify", classify_intent)
    workflow.add_node("retrieve", retrieve_docs)
    workflow.add_node("generate", generate_answer)

    # 设置入口
    workflow.set_entry_point("classify")

    # 添加边：classify → 根据意图路由
    workflow.add_conditional_edges(
        "classify",
        route_by_intent,
        {
            "retrieve": "retrieve",
            "generate": "generate",
        }
    )

    # 添加边：retrieve → generate
    workflow.add_edge("retrieve", "generate")

    # 添加边：generate → END
    workflow.add_edge("generate", END)

    return workflow.compile()


# 编译图（供外部直接导入使用）
agent_graph = build_agent_graph()
