import sys
import os
sys.path.append(os.path.dirname(__file__))

from kedou_parser import extract_with_kedou_api, extract_with_mptext_api
# 后续可以导入其他解析器 (jina_parser, changfeng_parser 等)

def auto_parse(url: str):
    """
    智能解析调度中心。
    采用四级降级策略：
    1. MPText API (无需密钥, 速度快, 稳定)
    2. 长风盒子
    3. Jina AI
    4. Kedou 自动化 (终极兜底, 提取媒体资源)
    """
    print(f"[Parser] Starting auto parse for: {url}")
    
    if "mp.weixin.qq.com" in url:
        print("[Parser] WeChat URL detected. Trying MPText API first...")
        result = extract_with_mptext_api(url)
        
        # 如果 MPText 成功获取了内容，直接返回
        if result.get("content"):
            return result
        
        print("[Parser] MPText API failed or returned empty. Trying Kedou...")
        return extract_with_kedou_api(url)
    
    return {"error": "Not implemented for this URL type yet."}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = auto_parse(sys.argv[1])
        print(f"Title: {result.get('title')}")
        print(f"Content Length: {len(result.get('content', ''))}")
        print(f"Images Found: {len(result.get('images', []))}")
