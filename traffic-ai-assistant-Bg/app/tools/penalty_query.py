from langchain_core.tools import tool


@tool(description="查询违章扣分和罚款标准。当用户询问扣几分、罚多少钱时使用此工具。")
def query_penalty(violation: str) -> str:
    # TODO: 接入真实的扣分罚款数据源
    return f"正在查询「{violation}」的扣分罚款标准，功能开发中..."