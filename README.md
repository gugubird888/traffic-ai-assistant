# Traffic AI Assistant - 交通法规 AI 助手

> 基于 RAG + Agent 的交通法规智能客服，帮助司机快速查询交通法规、事故责任判定、扣分罚款标准等。

## 项目简介

针对驾驶场景的 AI 法律助手，用户可以用自然语言提问交通法规相关问题，系统基于法律语料库进行检索增强生成（RAG），给出准确、有依据的回答。

### 核心功能

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 交通法规查询 | 输入问题，检索法条并用自然语言解读 | P0 |
| 事故责任咨询 | 描述事故场景，给出责任判定参考 | P0 |
| 扣分/罚款查询 | 精确查询各类违章的扣分和罚款标准 | P1 |
| 违章处理指引 | 事故/违章后的处理流程说明 | P1 |
| 多轮对话 | 支持追问，保持上下文 | P0 |

## 技术栈

### 后端（Python）

| 技术 | 用途 |
|------|------|
| LangChain | LLM 应用框架 |
| LangGraph | Agent 工作流编排（意图识别 → 检索 → 生成） |
| RAG | 法律语料检索增强生成 |
| Chroma | 向量数据库，存储法律条文 embedding |
| FastAPI | HTTP 接口服务 |
| uv | Python 包管理 |

### 前端（Vue 2）

| 技术 | 用途 |
|------|------|
| Vue 2 | 前端框架 |
| 聊天界面 | 用户交互 |

## 项目结构

```
traffic-ai-assistant/
├── backend/                # 后端（Python + LangChain）
│   ├── app/
│   │   ├── config.py       # 配置（LLM Provider、环境变量）
│   │   ├── services/       # 业务服务
│   │   ├── graphs/         # LangGraph 工作流定义
│   │   ├── tools/          # Agent 工具（扣分查询等）
│   │   ├── data/           # 法律语料
│   │   └── main.py         # FastAPI 入口
│   ├── pyproject.toml
│   └── .env
├── frontend/               # 前端（Vue 2）
│   └── ...
└── README.md
```

## 快速启动

### 后端

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8765
```

Swagger 文档：http://127.0.0.1:8765/docs

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 语料来源

- 《中华人民共和国道路交通安全法》
- 《道路交通安全法实施条例》
- 《机动车驾驶证申领和使用规定》（公安部令第162号）
- 典型交通事故案例（公开裁判文书）

## 免责声明

本项目仅供学习和参考，AI 生成的回答不构成法律意见。涉及实际法律问题，请咨询专业律师或联系当地交管部门。
