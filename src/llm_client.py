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
        # 胜算云代理（支持多种模型）
        "shengsuanyun": {
            "base_url": "https://router.shengsuanyun.com/api/v1",
            "model": "Kimi-thinking-preview",
            "api_key_env": "MODE_API_KEY"
        },
        # OpenAI 官方
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o",
            "api_key_env": "OPENAI_API_KEY"
        },
        # 阿里云通义千问
        "aliyun": {
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model": "qwen-max",
            "api_key_env": "DASHSCOPE_API_KEY"
        },
        # 腾讯云混元
        "tencent": {
            "base_url": "https://hunyuan.tencentcloudapi.com/v1/chat/completions",
            "model": "hunyuan",
            "api_key_env": "TENCENT_API_KEY"
        },
        # 百度文心一言
        "baidu": {
            "base_url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions",
            "model": "ernie-4.0",
            "api_key_env": "BAIDU_API_KEY"
        },
        # 字节跳动豆包
        "bytedance": {
            "base_url": "https://api.doubao.com/v1/chat/completions",
            "model": "Doubao-3",
            "api_key_env": "DOUBAO_API_KEY"
        },
        # 自定义配置
        "custom": {
            "base_url": os.getenv("LLM_BASE_URL", ""),
            "model": os.getenv("LLM_MODEL", ""),
            "api_key_env": "LLM_API_KEY"
        }
    }
    
    return configs.get(provider, configs["shengsuanyun"])


def init_llm_client(provider: Optional[str] = None, model: Optional[str] = None) -> ChatOpenAI:
    """初始化 LLM 客户端（支持多种云厂商）"""
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
    return ["shengsuanyun", "openai", "aliyun", "tencent", "baidu", "bytedance", "custom"]