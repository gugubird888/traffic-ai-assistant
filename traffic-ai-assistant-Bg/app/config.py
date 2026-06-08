from dotenv import load_dotenv
import os

load_dotenv()

# MIMO_MODEL=mimo-v2.5
# MIMO_API_KEY=tp-cdn54iwsiyu29u6g41jaal4kr3hklwd6o874149qwvtiywdk
# MIMO_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
#
# # DeepSeek（以后要用再填）
# DEEPSEEK_API_KEY=sk-adaba12e47e84f378638e3e27c9a431a
# DEEPSEEK_BASE_URL=https://api.deepseek.com
# DEEPSEEK_MODEL=deepseek-v4-flash

# Chat 模型切换：mimo  | deepseek
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mimo")

if LLM_PROVIDER == "mimo":
    LLM_MODEL = os.getenv("MIMO_MODEL")
    LLM_API_KEY = os.getenv("MIMO_API_KEY")
    LLM_BASE_URL = os.getenv("MIMO_BASE_URL")
elif LLM_PROVIDER == "deepseek":
    LLM_MODEL = os.getenv("DEEPSEEK_MODEL")
    LLM_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    LLM_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

# --- DashScope ---
DASHSCOPE_EMBEDDING_MODEL = os.getenv("DASHSCOPE_EMBEDDING_MODEL", "text-embedding-v4")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "")


# Chroma 配置
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "traffic_laws")

# FastAPI 配置
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8765"))