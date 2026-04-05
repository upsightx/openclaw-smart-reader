# Universal Reader Skill for OpenClaw

一个功能强大的通用文章解析 Skill。它不仅能处理微信公众号，还能通过多级 fallback 机制攻克**海外网站**、**付费墙**及**强反爬**页面。

## 🌟 核心特性

*   **三级智能引擎**：
    1.  **直连模式**：优先尝试本地抓取，速度最快。
    2.  **微信专优**：集成**长风盒子**，完美解决公众号反爬。
    3.  **全球通读**：集成 **Jina AI Reader**，自带海外代理，轻松绕过封锁和付费墙。
*   **强制内容校验**：内置严格的内容完整性检查，拒绝返回残缺或错误的页面。
*   **标准化输出**：无论来源如何，始终返回干净的 `Title` + `Markdown Content`。

## 🚀 使用方法

1.  **安装**：
    ```bash
    clawhub install upsightx/openclaw-wechat-reader
    ```
2.  **使用**：
    在对话框中直接发送任意文章链接（微信、Medium、Twitter、Substack 等），Skill 会自动选择最优引擎进行解析。

## 🛠️ 技术架构

*   `parser.py`: 核心解析逻辑，实现了 `Direct -> Changfengbox -> Jina AI` 的自动降级链路。
*   `SKILL.md`: 定义了严格的操作协议，防止 Agent 产生幻觉。

## ⚠️ 说明

由于部分网站（如 NYT 高级付费区）防护极强，若所有引擎均失败，Skill 会如实反馈并建议手动处理。

---
*License: MIT*
