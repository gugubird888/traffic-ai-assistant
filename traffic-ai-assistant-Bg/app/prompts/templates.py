from langchain_core.prompts import ChatPromptTemplate

# RAG 问答 prompt
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的交通法规助手。请根据法律条文内容回答用户问题。

要求：
1. 回答必须基于提供的法律条文，不要编造
2. 用通俗易懂的语言解释法律条文
3. 如果涉及具体处罚标准，明确说明扣分和罚款金额
4. 在回答末尾注明引用的法律条文来源"""),
    ("human", """法律条文内容：
{context}

用户问题：{question}"""),
])

# 意图识别 prompt
INTENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """请判断用户问题的意图类型，只返回以下类别之一：
- law_query: 法规查询（问某条法规是什么）
- accident_liability: 事故责任判定
- penalty_query: 扣分/罚款查询
- violation_guide: 违章处理流程
- general: 其他/闲聊"""),
    ("human", "{question}"),
])