from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import chat, chat_stream

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """对话接口（非流式，保留兼容）"""
    result = await chat(
        query=request.query,
        session_id=request.session_id,
    )
    return ChatResponse(**result)


@router.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """流式对话接口（SSE）"""
    return StreamingResponse(
        chat_stream(
            query=request.query,
            session_id=request.session_id,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )