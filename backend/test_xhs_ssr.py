import httpx
import re
import json

def test_xhs_ssr():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    }
    resp = httpx.get("https://www.xiaohongshu.com/explore", headers=headers)
    match = re.search(r'window\.__INITIAL_STATE__=({.*?})<\/script>', resp.text)
    if match:
        data = match.group(1)
        data = data.replace("undefined", "null")
        try:
            parsed = json.loads(data)
            print("XHS Success! Found state.")
            queries = parsed.get("explore", {}).get("feeds", [])
            if queries:
                 print("Notes found:", len(queries))
            else:
                 print("Explore feeds NOT IN SSR:", list(parsed.get("explore", {}).keys()))
        except Exception as e:
            print("Failed JSON parse:", e)
    else:
        print("XHS SSR Not found. Snapshot:", resp.text[:200])

test_xhs_ssr()
