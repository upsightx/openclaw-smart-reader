---
name: wechat-reader
description: |
  微信文章解析与归档助手。
  强制利用 web_fetch 获取实时内容，严禁依赖标题推测。
  支持将文章转换为 Markdown 并保存至飞书云文档。
---

# WeChat Reader Skill

## 核心工作流 (Core Workflow)

1.  **强制抓取 (Mandatory Fetch)**：
    *   收到微信链接后，**必须**首先调用 `web_fetch` 尝试提取全文。
    *   **校验机制**：如果 `web_fetch` 返回的内容过短或与标题明显不符（如只返回了“阅读全文”），则判定为抓取失败。

2.  **备选方案 (Fallback Strategy)**：
    *   若直接抓取失败，尝试通过第三方解析接口（如长风盒子等）获取内容。
    *   若所有自动化手段均失效，**必须**如实告知用户“微信反爬限制”，并提供手动解析的建议，严禁编造文章内容。

3.  **结构化归档 (Structured Archiving)**：
    *   调用 `parser.py` 提取标题和正文。
    *   调用 `feishu_create_doc` 存入指定的飞书文件夹（默认：`Zxw7fE4zBlnUgFdAtWjcTb5Vnzb`）。

## 脚本说明 (Scripts)

*   `parser.py`: 核心解析逻辑，支持 Markdown 格式化。
*   `feishu_saver.py`: 辅助脚本，用于将结果同步至飞书。

## 错误处理 (Error Handling)

*   **反爬应对**：微信链接具有强反爬特性。若 `web_fetch` 无法获取正文，Skill 应自动切换到“元数据提取模式”，至少保证标题和摘要的准确性。
*   **内容完整性**：在生成飞书文档前，检查正文是否包含核心段落。若内容残缺，需在文档开头标注“【部分解析】”。

## 使用示例

*   **输入**：`https://mp.weixin.qq.com/s/xxxx`
*   **输出**：一份包含完整正文和排版的飞书文档链接。

---

*Version: 1.1.0 (Enhanced with Strict Fetch Protocol)*
