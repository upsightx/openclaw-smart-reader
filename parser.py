#!/usr/bin/env python3
"""
WeChat Article Parser
Supports direct fetch and Changfengbox API fallback.
"""
import json
import sys
import urllib.request
import urllib.error
from openclaw.tools import web_fetch

CHANGFENG_API = "https://api.changfengbox.top/wechat/"

def parse_with_changfeng(url: str) -> dict:
    """Attempt to parse using Changfengbox API."""
    try:
        api_url = f"{CHANGFENG_API}?url={url}"
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("code") == 200 or data.get("title"):
                return {
                    "success": True,
                    "title": data.get("title", "Untitled"),
                    "content": data.get("content", ""),
                    "source": "changfengbox"
                }
    except Exception:
        pass
    return None

def parse_wechat_article(url: str) -> dict:
    """
    Parse a WeChat article URL with fallback logic.
    """
    # Strategy 1: Direct Fetch (Fastest, no external dependency)
    try:
        content = web_fetch(url=url, extractMode="markdown")
        if len(content) > 50: # Basic validity check
            title = ""
            if "# " in content:
                parts = content.split("\n", 1)
                title = parts[0].replace("# ", "").strip()
                content = parts[1]
            return {"success": True, "title": title, "content": content, "source": "direct"}
    except Exception:
        pass

    # Strategy 2: Changfengbox Fallback (More robust against anti-scraping)
    cf_result = parse_with_changfeng(url)
    if cf_result:
        return cf_result

    return {"success": False, "error": "Failed to parse via both direct fetch and Changfengbox."}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = parse_wechat_article(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
