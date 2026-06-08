# Traffic AI Assistant - 后端

交通法规 AI 助手后端服务，基于 LangChain + LangGraph + FastAPI。

## 项目结构

```
traffic-ai-assistant-Bg/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理（LLM、向量库、环境变量）
│   │
│   ├── models/              # 数据模型
│   │   └── schemas.py       # Pydantic 请求/响应模型
│   │
│   ├── services/            # 业务逻辑层
│   │   ├── rag_service.py   # RAG 检索 + 生成
│   │   └── chat_service.py  # 对话管理（历史、上下文）
│   │
│   ├── graphs/              # LangGraph 工作流
│   │   └── agent_graph.py   # 意图识别 → 路由 → 检索 → 生成
│   │
│   ├── tools/               # Agent 工具
│   │   ├── law_search.py    # 法条检索工具
│   │   └── penalty_query.py # 扣分罚款查询工具
│   │
│   ├── prompts/             # Prompt 模板
│   │   └── templates.py     # 集中管理所有 prompt
│   │
│   ├── vectorstore/         # 向量库相关
│   │   ├── embeddings.py    # Embedding 模型封装
│   │   └── chroma.py        # Chroma 初始化、检索
│   │
│   └── api/                 # 路由层
│       ├── chat.py          # POST /chat - 对话接口
│       └── health.py        # GET /health - 健康检查
│
├── data/                    # 法律语料（原始文档）
├── scripts/                 # 脚本（语料导入、embedding 生成）
├── pyproject.toml
└── .env
```

## 快速启动

```bash
# 安装依赖
uv sync

# 复制环境变量
cp .env.example .env
# 编辑 .env 填入 LLM_API_KEY

# 启动服务
uv run uvicorn app.main:app --reload --port 8765
```

Swagger 文档：http://127.0.0.1:8765/docs

## 依赖说明

| 包 | 用途 |
|---|---|
| langchain | LLM 应用核心框架 |
| langchain-openai | OpenAI 兼容接口 |
| langgraph | Agent 工作流编排 |
| chromadb | 向量数据库 |
| fastapi | HTTP 接口服务 |
| uvicorn | ASGI 服务器 |
| python-dotenv | 环境变量管理 |
