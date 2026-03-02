"""
API 客户端配置 - 支持胜算云代理
"""
import os
from langchain_openai import ChatOpenAI


def init_kimi_client() -> ChatOpenAI:
    """初始化 API 客户端（胜算云代理）"""
    api_key = os.getenv("MODE_API_KEY")
    base_url = os.getenv("MODE_BASE_URL", "https://router.shengsuanyun.com/api/v1")
    model = os.getenv("MODE_MODEL", "Kimi-thinking-preview")

    if not api_key:
        raise ValueError("请设置 MODE_API_KEY 环境变量")

    return ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=0.8,
        default_headers={
            'HTTP-Referer': 'https://github.com/rednote-agent',
            'X-Title': 'RedNote-Agent'
        }
    )

