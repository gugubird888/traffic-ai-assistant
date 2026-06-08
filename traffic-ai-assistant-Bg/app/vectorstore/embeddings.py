from langchain_openai import OpenAIEmbeddings
from app.config import DASHSCOPE_EMBEDDING_MODEL, DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL


def get_embedding_model() -> OpenAIEmbeddings:
    """获取 Embedding 模型实例（统一用 DashScope）"""
    return OpenAIEmbeddings(
        model=DASHSCOPE_EMBEDDING_MODEL,
        api_key=DASHSCOPE_API_KEY,
        base_url=DASHSCOPE_BASE_URL,
        check_embedding_ctx_length=False,
        chunk_size=10,
    )