"""
产品处理主流程
"""
import json
import sys
import os
from pathlib import Path

if sys.platform == 'win32':
    os.system('chcp 65001 > nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from .state import AgentState
from .agent import build_graph


def load_products(file_path: str = "inputs.json") -> list[dict]:
    """加载产品数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def process_products(input_file: str = "inputs.json", output_dir: str = "outputs"):
    """处理所有产品"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    (output_path / "covers").mkdir(exist_ok=True)

    products = load_products(input_file)
    app = build_graph()
    results = []

    for product in products:
        print(f"\n[处理] 产品: {product['name']} ({product['product_id']})")

        initial_state = AgentState(
            product=product,
            title="",
            content="",
            tags=[],
            cover_path="",
            error=None
        )

        final_state = app.invoke(initial_state)

        if final_state.get("error"):
            print(f"[错误] {final_state['error']}")
            continue

        result = {
            "product_id": product["product_id"],
            "cover": f"{product['product_id']}_cover.png",
            "title": final_state["title"],
            "content": final_state["content"],
            "tags": final_state["tags"]
        }
        results.append(result)

        print(f"[完成]")
        print(f"   产品ID: {product['product_id']}")

    with open(output_path / "results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n[完成] 所有产品处理完成! 结果已保存到 {output_dir}/")
    print(f"   共生成 {len(results)} 个产品的内容")

