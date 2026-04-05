#!/usr/bin/env python3
"""
WeChat Article Parser
Extracts title, content, and images from WeChat MP links.
"""
import json
import sys
import os
from openclaw.tools import web_fetch

def parse_wechat_article(url: str) -> dict:
    """
    Parse a WeChat article URL and return structured data.
    """
    try:
        # Use OpenClaw's built-in web_fetch for robustness
        content = web_fetch(url=url, extractMode="markdown")
        
        # Basic cleanup
        title = ""
        body = ""
        
        if "# " in content:
            parts = content.split("\n", 1)
            title = parts[0].replace("# ", "").strip()
            body = parts[1] if len(parts) > 1 else ""
        else:
            body = content
            
        return {
            "success": True,
            "title": title,
            "content": body,
            "url": url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = parse_wechat_article(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
