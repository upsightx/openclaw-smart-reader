import subprocess
import time
import json
import urllib.parse

def extract_with_mptext_api(url: str) -> dict:
    """
    使用 mptext.top 公共 API 提取微信公众号文章内容。
    支持 text/markdown/html/json 格式，无需密钥（仅部分功能需密钥）。
    """
    base_url = "https://down.mptext.top/api/public/v1/download"
    result = {
        "title": "",
        "content": "",
        "media_type": "text",
        "source": "mptext_api"
    }

    try:
        encoded_url = urllib.parse.quote(url, safe='')
        api_url = f"{base_url}?url={encoded_url}&format=markdown"
        
        print(f"[MPText-API] Fetching: {api_url}")
        output = subprocess.run(
            ["curl", "-s", "-A", "Mozilla/5.0", api_url], 
            capture_output=True, text=True, timeout=30
        )
        
        if output.returncode == 0 and output.stdout.strip():
            # mptext 返回的内容可能包含一些 CSS 或 JS，这里简单清洗
            content = output.stdout
            # 尝试提取标题（如果是 markdown 格式，标题通常在第一行）
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    result["title"] = line[2:].strip()
                    break
            result["content"] = content
            print(f"[MPText-API] Success! Content length: {len(content)}")
        else:
            print(f"[MPText-API] Fetch failed or empty response.")
            
        return result

    except Exception as e:
        print(f"[MPText-API] Critical Error: {str(e)}")
        return result

def extract_with_kedou_api(url: str) -> dict:
    """
    使用 Kedou 核心 API (通过 agent-browser 注入) 提取微信公众号内容。
    相比自动化点击，这种方式速度快 10 倍且更稳定。
    """
    KEDOU_URL = "https://www.kedou.life/extract/gzh"
    result = {
        "title": "",
        "content": "", # API 通常只返回媒体链接，文本建议配合 Jina/Changfeng
        "images": [],
        "videos": [],
        "source": "kedou_api_inject"
    }

    try:
        # 1. 打开 Kedou 页面
        print(f"[Kedou-API] Opening Kedou...")
        subprocess.run(["agent-browser", "open", KEDOU_URL], check=True, capture_output=True)
        time.sleep(3)

        # 2. 填入链接
        subprocess.run(["agent-browser", "fill", "input, textarea", url], check=True, capture_output=True)
        
        # 3. 注入拦截器并点击
        print(f"[Kedou-API] Injecting interceptor and clicking...")
        js_intercept = """
        window._kedouResult = null;
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            if (args[0].includes('/api/video/extract/v2')) {
                const res = await originalFetch(...args);
                window._kedouResult = await res.clone().json();
            }
            return originalFetch(...args);
        };
        document.querySelector('button')?.click();
        """
        subprocess.run(["agent-browser", "eval", js_intercept], check=True, capture_output=True)
        
        # 4. 等待结果
        time.sleep(10)
        output = subprocess.run(
            ["agent-browser", "eval", "JSON.stringify(window._kedouResult)"], 
            capture_output=True, text=True
        )
        
        # 3. 解析返回的 JSON 数据
        if output.stdout:
            # agent-browser 有时会返回带引号的字符串，尝试去除首尾引号
            raw_data = output.stdout.strip().strip('"').replace('\\"', '"')
            data = json.loads(raw_data)
            if isinstance(data, dict) and data.get("code") == 200 and data.get("data"):
                info = data["data"]
                result["title"] = info.get("title", "Unknown")
                result["images"] = info.get("imageList", []) or info.get("images", [])
                result["videos"] = info.get("videoList", []) or info.get("videos", [])
                print(f"[Kedou-API] Success! Found {len(result['images'])} images.")
            else:
                print(f"[Kedou-API] API returned error: {data}")
        else:
            print("[Kedou-API] No output from browser eval.")

        subprocess.run(["agent-browser", "close"], check=True, capture_output=True)
        return result

    except Exception as e:
        print(f"[Kedou-API] Critical Error: {str(e)}")
        try:
            subprocess.run(["agent-browser", "close"], check=True, capture_output=True)
        except: pass
        return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        res = extract_with_kedou_api(sys.argv[1])
        print(json.dumps(res, indent=2, ensure_ascii=False))
