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
        "shengsuanyun": {
            "base_url": os.getenv("MODE_TXT_BASE_URL", "https://router.shengsuanyun.com/api/v1"),
            "model": os.getenv("MODE_TXT_MODEL", "Kimi-latest"),
            "api_key_env": "MODE_TXT_API_KEY"
        },
        "custom": {
            "base_url": os.getenv("LLM_BASE_URL", ""),
            "model": os.getenv("LLM_MODEL", ""),
            "api_key_env": "LLM_API_KEY"
        }
    }

    if provider not in configs:
        raise ValueError(
            f"不支持的 LLM 供应商: '{provider}'。"
            f"支持的供应商: {', '.join(configs.keys())}。"
            f"请设置 LLM_PROVIDER 环境变量或在 .env 中正确配置。"
        )

    return configs[provider]


def init_llm_client(provider: Optional[str] = None, model: Optional[str] = None) -> ChatOpenAI:
    """初始化 LLM 客户端"""
    provider = provider or os.getenv("LLM_PROVIDER", "shengsuanyun")
    config = get_provider_config(provider)
    
    api_key = os.getenv(config["api_key_env"])
    base_url = os.getenv("LLM_BASE_URL", config["base_url"])
    model_name = model or os.getenv("LLM_MODEL", config["model"])

    if not api_key:
        raise ValueError(
            f"未找到 API Key。请设置 {config['api_key_env']} 环境变量。"
            f"（当前供应商: {provider}，参考 .env.example 配置）"
        )

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
    return list(configs.keys())