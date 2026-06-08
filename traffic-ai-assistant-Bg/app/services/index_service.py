from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.vectorstore.chroma import get_vectorstore

# 项目根目录（index_service.py 的上两级）
PROJECT_ROOT = Path(__file__).parent.parent.parent


def build_index(data_dir: str = None) -> dict:
    """
    构建向量索引，支持 txt/pdf/docx
    流程：加载文档 → 分割 chunks → 写入向量库
    """
    # 如果没传 data_dir，默认用项目根目录下的 data 文件夹
    if data_dir is None:
        data_dir = str(PROJECT_ROOT / "data")

    # 文件后缀 → Loader 映射
    # 不同格式的文件用不同的 Loader 解析
    loader_map = {
        ".txt": TextLoader,      # 纯文本
        ".pdf": PyPDFLoader,     # PDF（需要 pypdf 包）
        ".docx": Docx2txtLoader, # Word 文档（需要 docx2txt 包）
    }

    # 1. 加载文档
    all_docs = []
    # loader_map.items() 返回键值对，比如 (".txt", TextLoader)
    # ext: 文件后缀，如 ".txt"、".pdf"
    # loader_cls: 对应的 Loader 类，如 TextLoader、PyPDFLoader
    for ext, loader_cls in loader_map.items():
        # DirectoryLoader: 批量加载目录下的文件
        #   data_dir: 要扫描的目录路径
        #   glob: 文件匹配模式，**/*{ext} 表示递归查找所有该后缀的文件
        #   loader_cls: 指定用哪个 Loader 类解析文件
        loader = DirectoryLoader(data_dir, glob=f"**/*{ext}", loader_cls=loader_cls)
        # load() 执行加载，返回 Document 对象列表
        docs = loader.load()
        # extend: 把 docs 列表里的元素逐个添加到 all_docs
        all_docs.extend(docs)

    # 2. 分割 chunks（文本分块）
    # 为什么要分割？
    # - LLM 有 token 限制，不能一次传太长的文本
    # - 检索时更细粒度，提高相关性
    # - 500 字符一块，重叠 50 字符避免切断语义
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # 每块最大 500 字符
        chunk_overlap=50,    # 相邻块重叠 50 字符，避免切断句子
    )
    # split_documents: 把 Document 列表分割成更小的块
    chunks = splitter.split_documents(all_docs)

    # 3. 写入 Chroma 向量库
    # 调试：打印 chunks 信息
    print(f"chunks 数量: {len(chunks)}")
    if chunks:
        print(f"第一个 chunk 内容: {chunks[0].page_content[:100]}")
        print(f"第一个 chunk 类型: {type(chunks[0].page_content)}")
    else:
        print("警告：没有 chunks")

    vectorstore = get_vectorstore()
    # add_documents: 自动调用 Embedding 模型把文本转成向量，存入 Chroma
    vectorstore.add_documents(chunks)

    return {
        "doc_count": len(all_docs),      # 原始文档数
        "chunk_count": len(chunks),      # 分割后的块数
    }
