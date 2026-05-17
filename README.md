# RedNote-Agent | 小红书图文生成

[胜算云](https://www.shengsuanyun.com/) [PK大赛](https://www.shengsuanyun.com/activity/dc092badb3d1408d81b285d4d243678f)中的小红书图文赛道。

## 功能特点

- 🤖 使用 LangGraph 构建智能工作流
- 🎨 自动生成符合小红书风格的文案和封面
- 🎯 支持多种语气风格（温馨治愈、活泼俏皮、专业测评等）
- 🖼️ 支持 AI 图像生成（Doubao Seed 1.6）
- 📦 使用 uv 进行快速依赖管理

## 快速开始

### 1. 安装依赖

```bash
uv sync
```

### 2. 配置环境变量

首先，将 `.env.example` 文件复制一份并重命名为 `.env`。然后，编辑 `.env` 文件：

```
MODE_API_KEY="your_api_key" # 替换为你的胜算云 API Key
MODE_BASE_URL=https://router.shengsuanyun.com/api/v1
MODE_MODEL=moonshot/Kimi-thinking-preview
MODE_IMG_MODEL=bytedance/doubao-seed-1.6
```

### 3. 准备输入数据

编辑 `inputs.json`，可以放入一个或多个产品信息：

```json
[
  {
    "product_id": "P001",
    "name": "产品名称",
    "category": "产品类别",
    "price": 129,
    "target_audience": "目标人群",
    "features": ["特点1", "特点2"],
    "selling_point": "核心卖点",
    "tone": "温馨治愈"
  }
]
```

### 4. 运行程序

```bash
uv run main.py
```

### 5. 查看结果

程序运行结束后，所有生成的内容会保存在 `outputs` 目录下：

- **文案**: `outputs/results.json` (包含所有产品的生成结果)
- **封面**: `outputs/covers/{product_id}_cover.png` (例如 `P001_cover.png`)

## 工作流程

```mermaid
graph TD
    A[开始] --> B{加载所有产品数据};
    B --> C{循环处理每个产品};
    C --> D[生成文案内容 (Kimi)];
    D --> E[生成封面描述 (Kimi)];
    E --> F[生成封面图片 (Doubao/Pillow)];
    F --> G{是否所有产品都已处理?};
    G -- 否 --> C;
    G -- 是 --> H[汇总所有结果];
    H --> I[保存到 results.json];
    I --> J[结束];
```

## `tone` 可选值

- `温馨治愈` - 温暖、治愈、像朋友般贴心
- `活泼俏皮` - 活泼、可爱、充满活力
- `专业测评` - 专业、客观、详细
- `种草安利` - 热情、推荐、真诚分享
- `简约高级` - 简洁、高级、有品质感

## 输出格式

`results.json` 文件中的每一项内容格式如下：

```json
{
  "product_id": "P001",
  "cover": "P001_cover.png",
  "title": "标题文案",
  "content": "正文内容",
  "tags": ["标签1", "标签2"]
}
```

## 注意事项

- **Windows 用户**: 项目已内置对 Windows 终端的编码处理 (`chcp 65001`)，以尽量避免在运行时出现乱码问题。如果依然存在问题，请确保您的终端（如 PowerShell, CMD）默认使用 UTF-8 编码。

