from pydantic import BaseModel, Field  # Pydantic: Python 数据验证库，类似 Java 的 Bean Validation
from typing import Optional  # 类型标注：表示字段可空，类似 Java 的 Optional<T>


class ChatRequest(BaseModel):
    """
    对话请求模型
    - 继承 BaseModel 后，Pydantic 会自动做数据校验和 JSON 序列化
    - 类似 Java 里加了 @Data @Valid 注解的 DTO
    """
    # Field 参数说明：
    #   第一个参数：... 表示必填（等价于 required=True）
    #   description：字段描述，会显示在 Swagger 文档里
    query: str = Field(..., description="用户问题")
    session_id: Optional[str] = Field(None, description="会话ID，用于多轮对话")
    # Optional[str] = Field(None, ...) 表示：
    #   - 类型是 str 或 None
    #   - 默认值是 None（不传就是 None）
    #   - 类似 Java: private Optional<String> sessionId = Optional.empty();


class ChatResponse(BaseModel):
    """
    对话响应模型
    - 返回给前端的数据结构
    - FastAPI 会自动把它转成 JSON
    """
    answer: str = Field(..., description="AI 回答")
    sources: list[str] = Field(default_factory=list, description="引用的法条来源")
    # default_factory=list 表示：
    #   - 默认值是空列表 []
    #   - 用 factory 而不是 default=[]，避免可变对象共享问题
    #   - 类似 Java: private List<String> sources = new ArrayList<>();
    session_id: str = Field(..., description="会话ID")


class StreamEvent(BaseModel):
    """流式 SSE 事件"""
    type: str = Field(..., description="事件类型: sources | token | done | error")
    content: Optional[str] = Field(None, description="token 内容或 error 信息")
    sources: Optional[list[str]] = Field(None, description="引用的法条来源")
    session_id: Optional[str] = Field(None, description="会话ID")

