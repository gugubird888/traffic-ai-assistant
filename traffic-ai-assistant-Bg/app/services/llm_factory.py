from langchain_openai import ChatOpenAI
from app.config import LLM_MODEL, LLM_API_KEY, LLM_BASE_URL


def create_llm(*, streaming: bool = False) -> ChatOpenAI:
    """根据配置创建 LLM 实例"""
    return ChatOpenAI(
        model=LLM_MODEL,
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
        streaming=streaming,
    )