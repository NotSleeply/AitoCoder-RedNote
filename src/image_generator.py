"""
图像生成模块
"""
import os
import time
import requests
from pathlib import Path


def generate_image_with_api(prompt: str, output_path: str, aspect_ratio: str = "3:4") -> bool:
    """
    图像生成 API

    Args:
        prompt: 图像描述提示词（英文）
        output_path: 输出路径
        aspect_ratio: 图片比例，支持 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9

    Returns:
        是否成功生成图像
    """
    api_key = os.getenv("MODE_IMG_API_KEY")
    base_url = os.getenv("MODE_IMG_BASE_URL")

    if not api_key:
        print("   ❌ 未找到 MODE_IMG_API_KEY 环境变量")
        return False

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    try:
        payload = {
            "model": os.getenv("MODE_IMG_MODEL"),
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "response_modalities": ["IMAGE"]
        }

        print(f"   📤 提交图像生成任务...")
        print(f"   📝 提示词: {prompt[:80]}...")

        response = requests.post(
            f"{base_url}/v1/tasks/generations",
            json=payload,
            headers=headers,
            timeout=30
        )

        print(f"   🔍 调试: HTTP状态码 {response.status_code}")

        if response.status_code != 200:
            print(f"   ❌ API请求失败 (HTTP {response.status_code})")
            print(f"   响应: {response.text[:500]}")
            return False

        result = response.json()
        print(f"   🔍 调试: API响应 = {result}")

        if result.get("code") != "success":
            print(f"   ❌ API返回错误: {result.get('message', 'unknown error')}")
            return False

        if "data" not in result or not result["data"]:
            print(f"   ❌ 响应格式错误,data字段为空")
            print(f"   完整响应: {result}")
            return False

        request_id = result["data"].get("request_id", "")
        if not request_id:
            print(f"   ❌ 响应中缺少 request_id")
            print(f"   完整响应: {result}")
            return False

        print(f"   ✅ 任务已提交 (ID: {request_id})")

        max_attempts = 60
        for attempt in range(max_attempts):
            time.sleep(2)

            query_response = requests.get(
                f"{base_url}/v1/tasks/generations/{request_id}",
                headers=headers,
                timeout=10
            )

            if query_response.status_code != 200:
                print(f"   ⚠️ 查询失败 (HTTP {query_response.status_code})")
                continue

            query_result = query_response.json()

            if query_result.get("code") != "success":
                print(f"   ⚠️ 查询错误: {query_result.get('message', 'unknown')}")
                continue

            data = query_result.get("data", {})
            status = data.get("status")
            progress = data.get("progress", "N/A")

            if attempt % 5 == 0:
                print(f"   ⏳ 生成中... 状态: {status}, 进度: {progress}")

            if status == "COMPLETED":
                result_data = data.get("data", {})
                image_urls = result_data.get("image_urls", [])

                if not image_urls:
                    print(f"   ❌ 未找到生成的图片URL")
                    return False

                print(f"   📥 下载图片...")
                img_response = requests.get(image_urls[0], timeout=30)
                if img_response.status_code == 200:
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    print(f"   ✅ 图片生成成功: {output_path}")
                    return True
                else:
                    print(f"   ❌ 下载图片失败 (HTTP {img_response.status_code})")
                    return False

            elif status == "FAILED":
                fail_reason = data.get("fail_reason", "未知原因")
                print(f"   ❌ 任务失败: {fail_reason}")
                return False

        print(f"   ⏰ 超时: {max_attempts * 2}秒内未完成生成")
        return False

    except Exception as e:
        print(f"   ❌ 异常错误: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

