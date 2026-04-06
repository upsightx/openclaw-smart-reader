# OpenClaw Smart Reader

A powerful multi-level content parser for OpenClaw, featuring deep WeChat article extraction via Kedou automation.

## Features
- **5-Level Degradation Strategy**: **MPText API** -> Direct Fetch -> Changfeng -> Jina -> Kedou Automation.
- **High-Speed WeChat Parsing**: Integrated `mptext.top` public API for fast, keyless text extraction.
- **Full Media Extraction**: Captures text, images, and videos from protected WeChat articles.
- **Feishu Integration**: Auto-syncs parsed content to Feishu Docs.

## Modules
- `modules/kedou_parser.py`: Ultimate engine. Supports both **MPText API** (fast text) and **Kedou API** (media extraction).
- `modules/parser.py`: The central scheduler for content parsing.
