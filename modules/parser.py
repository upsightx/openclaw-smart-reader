import sys
import os
sys.path.append(os.path.dirname(__file__))

from kedou_parser import extract_with_kedou_api, extract_with_mptext_api
# 后续可以导入其他解析器 (jina_parser, changfeng_parser 等)

import subprocess

def simple_fetch(url: str) -> dict:
    """
    简单的网页抓取，用于普通网站的第一优先级尝试。
    """
    try:
        output = subprocess.run(
            ["curl", "-s", "-A", "Mozilla/5.0", "-L", url], 
            capture_output=True, text=True, timeout=15
        )
        if output.returncode == 0 and len(output.stdout) > 100:
            return {"content": output.stdout, "source": "simple_fetch", "title": "Fetched"}
    except:
        pass
    return {}

def auto_parse(url: str):
    """
    智能解析调度中心。
    
    策略分流：
    1. 微信文章 (mp.weixin.qq.com)：
       - 优先 MPText API (极速、免密钥)
       - 兜底 Kedou 自动化 (全量媒体提取)
    
    2. 普通网页：
       - 优先直接抓取 (Simple Fetch)
       - 失败后尝试 Smart Reader 的其他引擎 (Jina/Changfeng/Kedou)
    """
    print(f"[Parser] Starting auto parse for: {url}")
    
    if "mp.weixin.qq.com" in url:
        print("[Parser] WeChat URL detected. Route: MPText -> Kedou")
        result = extract_with_mptext_api(url)
        
        # 如果 MPText 成功获取了内容，直接返回
        if result.get("content"):
            return result
        
        print("[Parser] MPText API failed. Fallback to Kedou engine...")
        return extract_with_kedou_api(url)
    
    else:
        print("[Parser] Standard URL detected. Route: Direct Fetch -> Smart Reader Fallback")
        # 第一优先级：直接尝试抓取
        result = simple_fetch(url)
        if result.get("content"):
            return result
            
        # TODO: 如果直接抓取失败，后续可以接入 Jina AI 或 Changfeng 盒子
        print("[Parser] Direct fetch failed. Smart Reader deep engines not yet integrated for non-WeChat URLs.")
        return {"error": "Direct fetch failed and deep engines are pending integration."}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = auto_parse(sys.argv[1])
        print(f"Title: {result.get('title')}")
        print(f"Content Length: {len(result.get('content', ''))}")
        print(f"Images Found: {len(result.get('images', []))}")
