from app.graphs.state import AgentState


def route_by_intent(state: AgentState) -> str:
    """根据意图决定走哪个分支"""
    intent = state.get("intent", "general")
    if intent in ("law_query", "penalty_query", "violation_guide", "accident_liability"):
        return "retrieve"
    else:
        return "generate"
