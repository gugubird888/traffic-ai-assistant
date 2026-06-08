from langchain_chroma import Chroma
from chromadb import HttpClient
from app.vectorstore.embeddings import get_embedding_model
from app.config import CHROMA_COLLECTION_NAME


def get_vectorstore() -> Chroma:
    """获取向量库实例（客户端模式，连接 Chroma 服务）"""
    client = HttpClient(host="localhost", port=8000)
    return Chroma(
        client=client,
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=get_embedding_model(),
    )


def get_retriever(k: int = 4):
    """获取检索器，k 为返回的文档数量"""
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": k})