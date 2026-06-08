"""最简 LangChain 流式示例: uv run python -m app.testStream"""
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_factory import create_llm



def main() -> None:
    a=input("请输入问题：")
    llm = create_llm()
    query = ChatPromptTemplate.from_messages([
        ('system', "你是一个专业的交通法律相关的从业者"),
        ('human', "{question}"),
    ]
    )

    chain=query | llm

    stream = chain.stream({"question": a})
    for chunk in stream:
        print(chunk.content, end="", flush=True)


        


if __name__ == "__main__":
    main()
