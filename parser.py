#!/usr/bin/env python3
"""
Universal Article Parser
Supports: Direct Fetch, WeChat (Changfengbox), and Global Sites (Jina AI).
"""
import json
import sys
import urllib.request
import urllib.error
from openclaw.tools import web_fetch

CHANGFENG_API = "https://changfengbox.top/wechat/"
JINA_BASE = "https://r.jina.ai/"

def parse_with_changfeng(url: str) -> dict:
    """Attempt to parse WeChat articles using Changfengbox."""
    try:
        api_url = f"{CHANGFENG_API}?url={url}"
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("code") == 200 or data.get("title"):
                return {"success": True, "title": data.get("title"), "content": data.get("content"), "source": "changfengbox"}
    except Exception:
        pass
    return None

def parse_with_jina(url: str) -> dict:
    """Attempt to parse global sites using Jina AI Reader."""
    try:
        jina_url = f"{JINA_BASE}{url}"
        content = web_fetch(url=jina_url, extractMode="markdown")
        if len(content) > 50 and "Title:" in content:
            lines = content.split("\n", 2)
            title = lines[0].replace("Title: ", "").strip()
            body = lines[2] if len(lines) > 2 else content
            return {"success": True, "title": title, "content": body, "source": "jina-ai"}
    except Exception:
        pass
    return None

def parse_article(url: str) -> dict:
    """
    Universal parser with three-stage fallback.
    """
    # Stage 1: Direct Fetch (Fastest)
    try:
        content = web_fetch(url=url, extractMode="markdown")
        if len(content) > 50:
            title = ""
            if "# " in content:
                parts = content.split("\n", 1)
                title = parts[0].replace("# ", "").strip()
                content = parts[1]
            return {"success": True, "title": title, "content": content, "source": "direct"}
    except Exception:
        pass

    # Stage 2: WeChat Fallback (Changfengbox)
    if "mp.weixin.qq.com" in url:
        cf_result = parse_with_changfeng(url)
        if cf_result:
            return cf_result

    # Stage 3: Global Fallback (Jina AI)
    jina_result = parse_with_jina(url)
    if jina_result:
        return jina_result

    return {"success": False, "error": "Failed to parse via all available engines."}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = parse_article(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
