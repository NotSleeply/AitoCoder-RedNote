"""
文案内容生成模块
"""
import json
from langchain_core.messages import HumanMessage, SystemMessage

from .kimi_client import init_kimi_client
from .state import AgentState


def generate_content_node(state: AgentState) -> AgentState:
    """生成文案内容节点"""
    product = state["product"]

    tone_map = {
        "温馨治愈": "温暖、治愈、像朋友般贴心的语气",
        "活泼俏皮": "活泼、可爱、充满活力的语气",
        "专业测评": "专业、客观、详细的测评语气",
        "种草安利": "热情、推荐、真诚分享的语气",
        "简约高级": "简洁、高级、有品质感的语气"
    }

    tone_desc = tone_map.get(product["tone"], "自然友好的语气")

    system_prompt = f"""你是一位专业的小红书内容创作者。请根据产品信息生成符合小红书风格的图文笔记。

小红书内容特点：
1. 标题：使用疑问句/感叹句/数字，吸引眼球，15-25字
2. 正文：短句分段，像朋友聊天，多用emoji，突出卖点
3. 标签：3-5个相关标签
4. 语气：{tone_desc}

禁止使用：最、第一、100%等绝对化用语

请以JSON格式返回，包含：title（标题）、content（正文）、tags（标签数组）"""

    user_prompt = f"""产品信息：
名称：{product['name']}
类别：{product['category']}
价格：{product['price']}元
目标人群：{product['target_audience']}
特点：{', '.join(product['features'])}
卖点：{product['selling_point']}
语气风格：{product['tone']}

请生成小红书笔记内容。"""

    try:
        client = init_kimi_client()
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = client.invoke(messages)
        content_text = response.content

        if "```json" in content_text:
            content_text = content_text.split("```json")[1].split("```")[0].strip()
        elif "```" in content_text:
            content_text = content_text.split("```")[1].split("```")[0].strip()

        result = json.loads(content_text)

        state["title"] = result.get("title", "")
        state["content"] = result.get("content", "")
        state["tags"] = result.get("tags", [])

    except Exception as e:
        state["error"] = f"文案生成失败: {str(e)}"

    return state
