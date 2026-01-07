"""
RedNote-Agent 主程序入口
小红书图文生成工具
"""
from dotenv import load_dotenv
from src.processor import process_products


def main():
    """主函数"""
    load_dotenv()
    process_products()


if __name__ == "__main__":
    main()
