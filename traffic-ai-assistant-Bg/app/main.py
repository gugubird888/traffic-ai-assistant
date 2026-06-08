from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, chat, index
from app.config import APP_HOST, APP_PORT

app = FastAPI(
    title="交通法规 AI 助手",
    description="基于 RAG + Agent 的交通法规智能客服",
    version="0.1.0",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(index.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)