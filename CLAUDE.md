# Traffic AI Assistant - 项目规范

## 项目简介

基于 RAG + Agent 的交通法规智能客服，帮助司机快速查询交通法规、事故责任判定、扣分罚款标准等。

## 技术栈

### 后端（Python）
- LangChain + LangGraph：LLM 应用框架 + Agent 工作流编排
- Chroma：向量数据库
- FastAPI：HTTP 接口服务
- uv：Python 包管理

### 前端（Vue 2）
- Vue 2 + 聊天界面

## 后端目录结构

```
traffic-ai-assistant-Bg/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── models/              # 数据模型
│   ├── services/            # 业务逻辑层
│   ├── graphs/              # LangGraph 工作流
│   ├── tools/               # Agent 工具
│   ├── prompts/             # Prompt 模板
│   ├── vectorstore/         # 向量库
│   └── api/                 # 路由层
├── data/                    # 法律语料
├── scripts/                 # 脚本
└── .env
```

## 开发规范

### Prompt 编写
- 必须使用 `ChatPromptTemplate.from_messages()`，不要用 `from_template()`
- 明确区分 system（指令）和 human（用户输入）角色
- Prompt 集中在 `app/prompts/templates.py` 管理，不要散落各处

### 配置管理
- 环境变量统一在 `.env` 文件配置
- `config.py` 根据 `LLM_PROVIDER` 统一组装配置
- 后续代码只用 `LLM_MODEL`、`LLM_API_KEY`、`LLM_BASE_URL`，不关心具体 provider

### Embedding
- 统一用 DashScope 的 `text-embedding-v4`
- 在 `app/vectorstore/embeddings.py` 封装

### LLM 实例创建
- 使用工厂模式，在 `app/services/llm_factory.py` 封装
- 后续需要 LLM 的地方调用 `create_llm()`

### 依赖管理
- 使用 `uv add` 安装依赖
- 不要手动修改 pyproject.toml

## 工程化最佳实践

### 设计原则
- **单一职责**：每个模块/函数只做一件事
- **依赖倒置**：高层模块不依赖低层模块，都依赖抽象
- **开放封闭**：对扩展开放，对修改封闭（用注册表/工厂模式）
- **配置与代码分离**：所有可变配置放 `.env`，代码只读配置

### 代码规范
- **变量命名**：用 `kwargs` 处理可选参数，全必传直接传参
- **函数设计**：参数少于 4 个直接传，超过 4 个用 dataclass/Pydantic 封装
- **错误处理**：在边界层（API 入口、外部调用）统一处理，内部不做重复捕获
- **类型标注**：公开函数必须有类型标注，私有函数按需

### 架构分层
```
api/        →  路由、参数校验、返回格式（不写业务逻辑）
services/   →  业务编排（调用 tools、graphs、vectorstore）
graphs/     →  工作流定义（LangGraph 状态机）
tools/      →  可调用的工具（单一职责）
prompts/    →  Prompt 模板（集中管理）
vectorstore/ →  向量检索（封装 embedding 和检索逻辑）
models/     →  数据结构（请求/响应 schema）
```

### Prompt 工程
- 使用 `from_messages()` 明确角色（system/human/ai）
- system 指令写清楚"你是谁"+"要求"+"输出格式"
- human 部分只放用户输入和上下文
- Prompt 集中管理，方便调优和版本控制

### 依赖注入
- 通过函数参数传递依赖，不要在函数内部直接 import 全局实例
- 便于测试（mock）和替换实现

### 可测试性
- 纯函数优先（无副作用）
- 外部依赖（LLM、向量库）通过参数注入，便于 mock
- 关键逻辑写单元测试

## 注意事项

1. 不要把 API Key 硬编码在代码里
2. Prompt 修改后需要重新测试效果
3. Embedding 模型和 Chat 模型是分开的，用不同的 provider
4. 每次改完代码先本地测试，再提交
