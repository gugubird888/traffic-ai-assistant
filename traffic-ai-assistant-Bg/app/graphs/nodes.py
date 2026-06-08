from collections.abc import AsyncIterator

from app.services.llm_factory import create_llm
from app.vectorstore.chroma import get_retriever
from app.prompts.templates import RAG_PROMPT, INTENT_PROMPT
from app.graphs.state import AgentState


def classify_intent(state: AgentState) -> dict:
    """意图识别节点"""
    llm = create_llm()
    chain = INTENT_PROMPT | llm
    result = chain.invoke({"question": state["query"]})
    return {"intent": result.content.strip()}


def retrieve_docs(state: AgentState) -> dict:
    """检索法条节点"""
    retriever = get_retriever(k=4)
    docs = retriever.invoke(state["query"])
    context = "\n\n".join([doc.page_content for doc in docs])
    return {"context": context}


def generate_answer(state: AgentState) -> dict:
    """生成回答节点"""
    llm = create_llm()
    chain = RAG_PROMPT | llm
    result = chain.invoke({
        "context": state["context"],
        "question": state["query"],
    })
    return {"answer": result.content}


async def stream_generate_answer(state: AgentState) -> AsyncIterator[str]:
    """流式生成回答，逐 token yield"""
    llm = create_llm(streaming=True)
    chain = RAG_PROMPT | llm
    async for chunk in chain.astream({
        "context": state.get("context", ""),
        "question": state["query"],
    }):
        if chunk.content:
            yield chunk.content

