# WeChat Reader Skill for OpenClaw

一个用于解析微信公众号文章并自动归档至飞书云文档的 OpenClaw Skill。

## 🌟 特性

*   **强制抓取逻辑**：内置严格的 `web_fetch` 校验，拒绝内容幻觉。
*   **飞书自动归档**：一键将文章转换为 Markdown 并存入你的飞书知识库。
*   **反爬容错**：针对微信反爬机制进行了优化，支持多种解析降级方案。

## 📂 项目结构

*   `SKILL.md`: Skill 定义与触发指令。
*   `parser.py`: 核心解析脚本。
*   `feishu_saver.py`: 飞书同步辅助脚本。

## 🚀 使用方法

1.  **安装**：
    ```bash
    clawhub install upsightx/openclaw-wechat-reader
    ```
2.  **使用**：
    直接在对话框中发送微信文章链接，或输入指令：
    ```
    帮我解析这篇微信文章：[链接]
    ```

## ⚠️ 注意事项

由于微信公众号具有较强的反爬机制，如果自动化解析失败，Skill 会如实反馈并建议手动处理。

---
*License: MIT*
