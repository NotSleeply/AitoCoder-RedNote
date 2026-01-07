"""
封面图生成模块
使用 Pillow 生成小红书风格的封面图
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap


def generate_cover(
    product_id: str,
    product_name: str,
    title: str,
    image_prompt: str,
    tone: str,
    output_dir: str = "outputs/covers"
) -> str:
    """
    生成小红书风格封面图

    Args:
        product_id: 产品ID
        product_name: 产品名称
        title: 标题文案
        image_prompt: 图片描述（暂未使用，可接入图像生成API）
        tone: 语气风格
        output_dir: 输出目录

    Returns:
        封面图路径
    """
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 图片尺寸 (3:4)
    width, height = 1080, 1440

    # 根据 tone 选择配色
    color_schemes = {
        "温馨治愈": {
            "bg": (255, 245, 238),  # 温暖米色
            "primary": (255, 182, 193),  # 粉色
            "text": (101, 67, 33)  # 深棕色
        },
        "活泼俏皮": {
            "bg": (255, 250, 205),  # 柠檬黄
            "primary": (255, 105, 180),  # 亮粉
            "text": (255, 69, 0)  # 橙红
        },
        "专业测评": {
            "bg": (240, 248, 255),  # 浅蓝
            "primary": (70, 130, 180),  # 钢青色
            "text": (25, 25, 112)  # 深蓝
        },
        "种草安利": {
            "bg": (255, 228, 225),  # 浅粉
            "primary": (255, 99, 71),  # 番茄红
            "text": (139, 0, 0)  # 深红
        },
        "简约高级": {
            "bg": (250, 250, 250),  # 浅灰
            "primary": (169, 169, 169),  # 灰色
            "text": (47, 79, 79)  # 深灰
        }
    }

    colors = color_schemes.get(tone, color_schemes["温馨治愈"])

    # 创建图像
    img = Image.new('RGB', (width, height), colors["bg"])
    draw = ImageDraw.Draw(img)

    # 绘制装饰元素
    # 顶部色块
    draw.rectangle([(0, 0), (width, 400)], fill=colors["primary"])

    # 底部渐变效果（简化为色块）
    draw.rectangle([(0, height-300), (width, height)],
                   fill=colors["primary"] + (128,))

    # 绘制产品名称区域
    try:
        # 尝试使用系统字体
        font_large = ImageFont.truetype("arial.ttf", 80)
        font_medium = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        # 如果没有找到字体，使用默认字体
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 绘制产品名称（居中，顶部）
    product_text = product_name
    bbox = draw.textbbox((0, 0), product_text, font=font_medium)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    draw.text((text_x, 150), product_text, fill="white", font=font_medium)

    # 绘制标题（中间，多行）
    title_lines = textwrap.wrap(title, width=15)
    y_offset = 600

    for line in title_lines[:3]:  # 最多3行
        bbox = draw.textbbox((0, 0), line, font=font_large)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        draw.text((text_x, y_offset), line,
                  fill=colors["text"], font=font_large)
        y_offset += 100

    # 绘制装饰文字
    decoration = "✨ 种草推荐 ✨"
    bbox = draw.textbbox((0, 0), decoration, font=font_small)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    draw.text((text_x, height - 150), decoration,
              fill="white", font=font_small)

    # 保存图片
    output_path = Path(output_dir) / f"{product_id}_cover.png"
    img.save(output_path, "PNG")

    return str(output_path)


if __name__ == "__main__":
    # 测试
    test_cover = generate_cover(
        product_id="TEST001",
        product_name="测试产品",
        title="这是一个测试标题！",
        image_prompt="测试图片描述",
        tone="温馨治愈"
    )
    print(f"测试封面已生成: {test_cover}")


def generate_cover_node(state):
    """生成封面图节点 - 使用 Gemini AI 生成"""
    from langchain_core.messages import HumanMessage
    from .kimi_client import init_kimi_client
    from .image_generator import generate_image_with_api

    if state.get("error"):
        return state

    product = state["product"]
    product_id = product["product_id"]

    try:
        # 使用 Kimi 生成图片描述
        client = init_kimi_client()

        prompt = f"""你是一位专业的AI图像提示词工程师,请为小红书封面生成详细的英文AI图像提示词。

产品信息:
- 产品名称: {product['name']}
- 产品类别: {product['category']}
- 核心卖点: {product['selling_point']}
- 标题文案: {state['title']}
- 风格调性: {product['tone']}

要求:
1. **使用英文**描述,适合 Gemini 2.5 Flash 图像模型
2. **主体突出**: 产品必须占据画面主要位置,清晰可见
3. **视觉具体**: 详细描述颜色、材质、光线、构图
4. **氛围营造**: 符合"{product['tone']}"的风格氛围
5. **小红书风格**: 适合社交媒体,吸引眼球,美观时尚
6. **3:4竖版构图**: 适合手机屏幕浏览
7. **避免文字**: 不要在提示词中包含任何文字、标签、数字

提示词结构建议:
[主体物品描述], [场景环境], [光线色调], [整体氛围], [艺术风格], professional product photography, high quality, 3:4 aspect ratio

请直接返回英文提示词,不要解释,不要中文。"""

        response = client.invoke([HumanMessage(content=prompt)])
        image_prompt = response.content.strip()

        # 清理可能的markdown格式
        if image_prompt.startswith("```"):
            lines = image_prompt.split("\n")
            image_prompt = "\n".join(
                [l for l in lines if not l.startswith("```")])

        image_prompt = image_prompt.strip()

        print(f"\n   🎨 AI提示词生成:")
        print(f"   {image_prompt}\n")

        # 优先使用 Gemini AI 生成封面
        output_path = f"outputs/covers/{product_id}_cover.png"

        print(f"   🚀 开始生成AI封面...")
        if generate_image_with_api(image_prompt, output_path, aspect_ratio="3:4"):
            print(f"   ✨ AI封面生成完成!\n")
            state["cover_path"] = output_path
            state["image_prompt"] = image_prompt  # 保存提示词
        else:
            # 失败时使用 Pillow 备用方案
            print(f"   ⚠️ AI生成失败,使用备用方案...\n")
            cover_path = generate_cover(
                product_id=product_id,
                product_name=product["name"],
                title=state["title"],
                image_prompt=image_prompt,
                tone=product["tone"]
            )
            state["cover_path"] = cover_path
            state["image_prompt"] = image_prompt

    except Exception as e:
        import traceback
        print(f"   ❌ 封面生成错误: {str(e)}")
        traceback.print_exc()
        state["error"] = f"封面生成失败: {str(e)}"

    return state
