"""
RedNote-Agent 主程序入口
小红书图文生成工具
"""
from dotenv import load_dotenv
from src.app import process_products

if __name__ == "__main__":
    load_dotenv()
    process_products()
