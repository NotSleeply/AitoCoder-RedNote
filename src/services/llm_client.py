"""
LLM 客户端配置 - 支持多种云厂商和API模型
"""
import os
from typing import Optional
from langchain_openai import ChatOpenAI


def get_provider_config(provider: str = None):
    """获取指定云厂商的配置"""
    provider = provider or os.getenv("LLM_PROVIDER", "shengsuanyun")
    
    configs = {
        "custom": {
            "base_url": os.getenv("LLM_BASE_URL", ""),
            "model": os.getenv("LLM_MODEL", ""),
            "api_key_env": "LLM_API_KEY"
        }
    }
    
    return configs.get(provider, configs["shengsuanyun"])


def init_llm_client(provider: Optional[str] = None, model: Optional[str] = None) -> ChatOpenAI:
    """初始化 LLM 客户端"""
    config = get_provider_config(provider)
    
    api_key = os.getenv(config["api_key_env"])
    base_url = os.getenv("LLM_BASE_URL", config["base_url"])
    model_name = model or os.getenv("LLM_MODEL", config["model"])

    if not api_key:
        raise ValueError(f"请设置 {config['api_key_env']} 环境变量")

    return ChatOpenAI(
        model=model_name,
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=0.8,
        default_headers={
            'HTTP-Referer': 'https://github.com/rednote-agent',
            'X-Title': 'RedNote-Agent'
        }
    )


def list_supported_providers():
    """列出支持的云厂商"""
    return ["custom"]