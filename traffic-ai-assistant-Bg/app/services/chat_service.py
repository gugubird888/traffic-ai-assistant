import json
from collections.abc import AsyncIterator

from app.graphs.agent_graph import agent_graph
from app.graphs.nodes import classify_intent, retrieve_docs, stream_generate_answer
from app.graphs.edges import route_by_intent
from app.graphs.state import AgentState


async def chat(query: str, session_id: str = None) -> dict:
    """
    处理对话请求（非流式，保留兼容）
    - 调用 LangGraph 工作流
    - 返回回答和来源
    """
    result = agent_graph.invoke({
        "query": query,
        "intent": "",
        "context": "",
        "answer": "",
    })

    return {
        "answer": result["answer"],
        "sources": [],  # TODO: 从 context 里提取来源
        "session_id": session_id or "default",
    }


async def chat_stream(query: str, session_id: str = None) -> AsyncIterator[str]:
    """
    流式对话：先跑 classify + retrieve，再流式 generate
    yield 的是 SSE 格式字符串: "data: {...}\n\n"
    """
    session_id = session_id or "default"

    def _sse(payload: dict) -> str:
        return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"

    state: AgentState = {
        "query": query,
        "intent": "",
        "context": "",
        "answer": "",
    }

    try:
        # 1. 意图识别（同步，很快）
        state.update(classify_intent(state))

        # 2. 按需检索
        if route_by_intent(state) == "retrieve":
            state.update(retrieve_docs(state))
            sources: list[str] = []  # TODO: 从 docs metadata 提取
            yield _sse({"type": "sources", "sources": sources})

        # 3. 流式生成
        async for token in stream_generate_answer(state):
            yield _sse({"type": "token", "content": token})

        yield _sse({"type": "done", "session_id": session_id})

    except Exception as e:
        yield _sse({"type": "error", "content": str(e)})