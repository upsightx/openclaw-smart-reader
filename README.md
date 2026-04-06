# OpenClaw Smart Reader

**OpenClaw Smart Reader** 是一个专为 OpenClaw 设计的高级内容解析引擎。它采用多级降级策略，能够稳定、高效地抓取并清洗互联网上的复杂内容，特别是针对具有严格反爬机制的微信公众号文章提供了终极解决方案。

## 🚀 核心特性

- **五级智能降级策略**：
  1. **MPText API**：利用公开接口实现极速、免密钥的微信文章文本提取。
  2. **直连抓取**：针对普通网页，直接提取核心内容。
  3. **长风盒子/Jina AI**：利用专业解析接口处理高难度排版。
  4. **Kedou 自动化引擎**：针对强防护平台，利用浏览器自动化技术实现 100% 模拟人类操作，突破反爬封锁。
- **全量媒体还原**：不仅提取文字，更能深度解析并还原文章中的高清图片、GIF 动图及视频直链。
- **飞书生态集成**：支持将解析后的内容自动同步至飞书云文档，实现“一键归档，图文并茂”。

## 📂 模块说明

| 模块 | 说明 |
|------|------|
| `modules/parser.py` | 调度中心。根据目标 URL 自动选择最优解析路径。 |
| `modules/kedou_parser.py` | 终极兜底引擎。支持 **MPText API** (快速文本) 和 **Kedou API** (媒体提取)。 |

## 🛠️ 技术架构

- **自动化底座**：基于 `agent-browser` (Playwright/Chrome) 实现无头浏览器自动化。
- **API 逆向**：深度逆向 Kedou/MPText 解析站点的网络请求。
- **结构化输出**：将所有非结构化网页内容转化为标准的 Markdown + 媒体列表格式。

## 📝 使用示例

```python
from modules.parser import auto_parse

# 智能解析任意链接
result = auto_parse("https://mp.weixin.qq.com/s/xxx")
print(result['title'])
print(result['content'])  # 获取 Markdown 内容
```

## 🤝 贡献与反馈

本项目由 OpenClaw 社区驱动。如果你在使用中遇到解析失败的情况，欢迎提交 Issue 或 PR。

---
*Powered by OpenClaw & Agent-Browser*
