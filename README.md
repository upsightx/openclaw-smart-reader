# OpenClaw Smart Reader

A powerful multi-level content parser for OpenClaw, featuring deep WeChat article extraction via Kedou automation.

## Features
- **4-Level Degradation Strategy**: Direct Fetch -> Changfeng -> Jina -> Kedou Automation.
- **Full Media Extraction**: Captures text, images, and videos from protected WeChat articles.
- **Feishu Integration**: Auto-syncs parsed content to Feishu Docs.

## Modules
- `modules/kedou_parser.py`: The ultimate engine for bypassing WeChat anti-scraping.
- `modules/parser.py`: The central scheduler for content parsing.
