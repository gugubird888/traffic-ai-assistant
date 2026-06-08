from langchain_core.tools import tool
from app.vectorstore.chroma import get_retriever


@tool(description="搜索交通法规条文。当用户询问法规内容、法律条文时使用此工具。")
def search_law(query: str) -> str:
    retriever = get_retriever(k=4)
    docs = retriever.invoke(query)
    results = []
    for doc in docs:
        source = doc.metadata.get("source", "未知来源")
        results.append(f"【{source}】{doc.page_content}")
    return "\n\n".join(results)