"""
封面图生成模块
使用 Pillow 生成小红书风格的封面图
"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
from pathlib import Path
import textwrap


def sanitize_text(text: str) -> str:
    if not text:
        return ""
    result = []
    for ch in text:
        code = ord(ch)
        if 0x4E00 <= code <= 0x9FFF or 0x3400 <= code <= 0x4DBF or 0x3040 <= code <= 0x30FF or 0xAC00 <= code <= 0xD7AF or 0x20 <= code <= 0x7E or 0xFF01 <= code <= 0xFF60 or 0xFF61 <= code <= 0xFF9F or ch.isspace():
            result.append(ch)
    return "".join(result)


def wrap_text_by_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int, max_lines: int = 3):
    if not text:
        return []
    text = text.strip()
    lines = []
    line = ""
    last_break = -1
    preferred = set(" ，。！？：；、,.!?;: ")
    for ch in text:
        line += ch
        if ch in preferred:
            last_break = len(line)
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        if w > max_width:
            if last_break > 0:
                cut = line[:last_break].rstrip()
                remainder = line[last_break:].lstrip()
            else:
                cut = line[:-1].rstrip()
                remainder = line[-1:]
            if cut:
                lines.append(cut)
            line = remainder
            last_break = -1
            for i, c in enumerate(line):
                if c in preferred:
                    last_break = i + 1
        if len(lines) >= max_lines:
            break
    if len(lines) < max_lines and line and len(lines) < max_lines:
        lines.append(line.rstrip())
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    return lines


def find_best_text_region(img: Image.Image, block_width: int, block_height: int, margin: int = 20):
    width, height = img.size
    gray = img.convert("L")

    block_width = min(block_width, width - margin * 2)
    block_height = min(block_height, height - margin * 2)

    positions = [
        (0.25, 0.25),
        (0.75, 0.25),
        (0.25, 0.50),
        (0.75, 0.50),
        (0.25, 0.75),
        (0.75, 0.75),
    ]

    best_score = None
    best_rect = (margin, margin, margin + block_width, margin + block_height)

    for px, py in positions:
        cx = int(width * px)
        cy = int(height * py)
        x0 = max(margin, min(cx - block_width // 2, width - margin - block_width))
        y0 = max(margin, min(cy - block_height // 2, height - margin - block_height))
        x1 = x0 + block_width
        y1 = y0 + block_height
        crop = gray.crop((x0, y0, x1, y1))
        stat = ImageStat.Stat(crop)
        var = stat.var[0]
        if best_score is None or var < best_score:
            best_score = var
            best_rect = (x0, y0, x1, y1)

    return best_rect


def generate_cover(
    product_id: str,
    product_name: str,
    title: str,
    image_prompt: str,
    tone: str,
    selling_point: str = "",
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

    try:
        import os
        font_paths = [
            r"C:\Windows\Fonts\msyh.ttc",
            r"C:\Windows\Fonts\simhei.ttf",
            r"C:\Windows\Fonts\simkai.ttf",
            r"/System/Library/Fonts/STHeiti Medium.ttc",
            r"/System/Library/Fonts/PingFang.ttc",
        ]
        font_path = None
        for p in font_paths:
            if os.path.exists(p):
                font_path = p
                break
        if font_path:
            font_large = ImageFont.truetype(font_path, 80)
            font_medium = ImageFont.truetype(font_path, 60)
            font_small = ImageFont.truetype(font_path, 40)
        else:
            font_large = ImageFont.truetype("arial.ttf", 80)
            font_medium = ImageFont.truetype("arial.ttf", 60)
            font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    layout_seed = sum(ord(c) for c in str(product_id)) % 3
    margin = 60
    max_text_width = width - margin * 2

    product_text = sanitize_text(product_name)
    bbox = draw.textbbox((0, 0), product_text, font=font_medium)
    text_width = bbox[2] - bbox[0]
    if layout_seed == 0:
        text_x = margin
    elif layout_seed == 1:
        text_x = width - text_width - margin
    else:
        text_x = (width - text_width) // 2
    draw.text((text_x, 150), product_text, fill="white", font=font_medium)

    title_clean = sanitize_text(title)
    title_lines = wrap_text_by_width(draw, title_clean, font_large, max_text_width, max_lines=3)

    if layout_seed == 0:
        y_offset = 520
    elif layout_seed == 1:
        y_offset = 580
    else:
        y_offset = 640

    line_height = font_large.size + 10
    block_height = line_height * min(3, len(title_lines or []))
    if block_height > 0 and y_offset + block_height > height - margin:
        y_offset = height - margin - block_height

    for line in title_lines[:3]:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        text_width = bbox[2] - bbox[0]
        if layout_seed == 1:
            text_x = margin
        elif layout_seed == 2:
            text_x = width - text_width - margin
        else:
            text_x = (width - text_width) // 2
        draw.text((text_x, y_offset), line,
                  fill=colors["text"], font=font_large)
        y_offset += line_height

    # 绘制装饰文字
    decoration = "✨ 种草推荐 ✨"
    bbox = draw.textbbox((0, 0), decoration, font=font_small)
    text_width = bbox[2] - bbox[0]
    if layout_seed == 0:
        text_x = margin
    elif layout_seed == 1:
        text_x = width - text_width - margin
    else:
        text_x = (width - text_width) // 2
    text_y = height - 150
    draw.text((text_x, text_y), decoration,
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
            
            # **重要：在AI生成的图片上添加文字元素**
            print(f"   📝 正在叠加文字...")
            try:
                # 读取AI生成的图片
                from PIL import Image
                img = Image.open(output_path)
                
                # 创建绘图对象
                draw = ImageDraw.Draw(img)
                
                # 获取配色方案
                color_schemes = {
                    "温馨治愈": {
                        "bg": (255, 245, 238),
                        "primary": (255, 182, 193),
                        "text": (101, 67, 33)
                    },
                    "活泼俏皮": {
                        "bg": (255, 250, 205),
                        "primary": (255, 105, 180),
                        "text": (255, 69, 0)
                    },
                    "专业测评": {
                        "bg": (240, 248, 255),
                        "primary": (70, 130, 180),
                        "text": (25, 25, 112)
                    },
                    "种草安利": {
                        "bg": (255, 228, 225),
                        "primary": (255, 99, 71),
                        "text": (139, 0, 0)
                    },
                    "简约高级": {
                        "bg": (250, 250, 250),
                        "primary": (169, 169, 169),
                        "text": (47, 79, 79)
                    }
                }
                colors = color_schemes.get(product["tone"], color_schemes["温馨治愈"])
                
                # 加载字体
                try:
                    import os
                    font_paths = [
                        r"C:\Windows\Fonts\msyh.ttc",
                        r"C:\Windows\Fonts\simhei.ttf",
                        r"C:\Windows\Fonts\simkai.ttf",
                        r"/System/Library/Fonts/STHeiti Medium.ttc",
                        r"/System/Library/Fonts/PingFang.ttc",
                    ]
                    font_path = None
                    for p in font_paths:
                        if os.path.exists(p):
                            font_path = p
                            break
                    if font_path:
                        font_medium = ImageFont.truetype(font_path, 50)
                        font_small = ImageFont.truetype(font_path, 35)
                    else:
                        font_medium = ImageFont.truetype("arial.ttf", 50)
                        font_small = ImageFont.truetype("arial.ttf", 35)
                except:
                    font_medium = ImageFont.load_default()
                    font_small = ImageFont.load_default()
                
                width, height = img.size
                layout_seed = sum(ord(c) for c in str(product_id)) % 5
                outer_margin = 36

                name_text = sanitize_text(product.get("name") or "")
                if name_text:
                    bbox = draw.textbbox((0, 0), name_text, font=font_medium)
                    name_width = bbox[2] - bbox[0]
                    if layout_seed in (0, 3):
                        name_x = outer_margin
                    else:
                        name_x = width - name_width - outer_margin
                    name_y = int(height * 0.08)
                    draw.text((name_x, name_y), name_text, fill=(255, 255, 255), font=font_medium, stroke_width=2, stroke_fill=(0, 0, 0))

                import textwrap
                title_text = sanitize_text(state.get("title", ""))
                if title_text:
                    block_width = int(width * 0.7)
                    block_height = int(height * 0.28)
                    x0, y0, x1, y1 = find_best_text_region(img, block_width, block_height, margin=outer_margin)
                    inner_margin = 12
                    max_text_width = (x1 - x0) - inner_margin * 2

                    lines = wrap_text_by_width(draw, title_text, font_medium, max_text_width, max_lines=3)
                    line_height = font_medium.size + 8
                    block_height = line_height * min(3, len(lines))
                    if block_height <= 0:
                        y_offset = y0 + inner_margin
                    else:
                        y_offset = y0 + max(inner_margin, ((y1 - y0) - block_height) // 2)

                    for line in lines[:3]:
                        bbox = draw.textbbox((0, 0), line, font=font_medium)
                        text_width = bbox[2] - bbox[0]
                        text_x = x0 + inner_margin
                        draw.text((text_x, y_offset), line, fill=colors["text"], font=font_medium, stroke_width=2, stroke_fill=(255, 255, 255))
                        y_offset += line_height
                
                # 保存添加文字后的图片
                img.save(output_path, "PNG")
                print(f"   ✅ 文字添加完成!\n")
                
            except Exception as e:
                print(f"   ⚠️ 文字添加失败: {str(e)}，使用原图")
            
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
                tone=product["tone"],
                selling_point=product.get("selling_point", "")
            )
            state["cover_path"] = cover_path
            state["image_prompt"] = image_prompt

    except Exception as e:
        import traceback
        print(f"   ❌ 封面生成错误: {str(e)}")
        traceback.print_exc()
        state["error"] = f"封面生成失败: {str(e)}"

    return state
