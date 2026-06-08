from fastapi import APIRouter
from app.services.index_service import build_index

router = APIRouter()


@router.post("/index")
async def build_index_endpoint():
    """构建/重建向量索引"""
    result = build_index()
    return result