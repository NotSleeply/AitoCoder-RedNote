# RedNote-Agent | 小红书图文生成

基于 LangGraph 和胜算云 API 的小红书图文内容自动生成工具。

## 功能特点

- 🤖 使用 LangGraph 构建智能工作流
- 🎨 自动生成符合小红书风格的文案和封面
- 🎯 支持多种语气风格（温馨治愈、活泼俏皮、专业测评等）
- 🖼️ 支持 AI 图像生成（Gemini 3 Pro Image Preview）
- 📦 使用 uv 进行快速依赖管理

## 快速开始

### 1. 安装依赖

```bash
uv sync
```

### 2. 配置环境变量

编辑 `.env` 文件：

```json
MODE_API_KEY=`your_api_key` // 替换为你的胜算云 API Key 
MODE_BASE_URL=https://router.shengsuanyun.com/api/v1
MODE_MODEL=moonshot/Kimi-thinking-preview
MODE_IMG_MODEL=google/gemini-3-pro-image-preview
```

### 3. 准备输入数据

编辑 `inputs.json`：

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

- 文案：`outputs/results.json`
- 封面：`outputs/covers/`

## 工作流程

```
加载产品数据
    ↓
生成文案内容 (Kimi API)
    ↓
生成封面描述 (Kimi API)
    ↓
生成封面图片 (Gemini Image API / Pillow)
    ↓
保存结果
```

## tone 可选值

- `温馨治愈` - 温暖、治愈、像朋友般贴心
- `活泼俏皮` - 活泼、可爱、充满活力
- `专业测评` - 专业、客观、详细
- `种草安利` - 热情、推荐、真诚分享
- `简约高级` - 简洁、高级、有品质感

## 输出格式

```json
{
  "product_id": "P001",
  "cover": "P001_cover.png",
  "title": "标题文案",
  "content": "正文内容",
  "tags": ["标签1", "标签2"]
}
```
