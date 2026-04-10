import httpx
import re

async def fetch_36kr():
    url = "https://36kr.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=headers)
            html = response.text
            
            # Simple direct regex to extract titles and IDs from 36kr's landing page cards
            # 36kr has a clear /p/ID structure
            titles = re.findall(r'title="(.*?)"', html)
            ids = re.findall(r'/p/(\d+)', html)
            
            results = []
            seen = set()
            for t, pid in zip(titles, ids):
                if pid in seen: continue
                if len(t) < 5: continue
                
                results.append({
                    "title": t,
                    "desc": "36氪前沿商业洞察",
                    "hot": "💡 深度",
                    "url": f"https://36kr.com/p/{pid}",
                    "plat": "36kr"
                })
                seen.add(pid)
                if len(results) >= 8: break
                
            return results if results else [{"title": "36氪暂无更新", "desc": "DOM 结构可能发生迁移", "hot": "⚠️ 降级", "plat": "36kr"}]
            
    except Exception as e:
        return [{"title": "36氪抓取异常", "desc": str(e), "hot": "⚠️ 降级", "plat": "36kr"}]
