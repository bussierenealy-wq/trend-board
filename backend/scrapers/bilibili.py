import httpx
import uuid

async def fetch_bilibili():
    url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com",
        "Cookie": f"buvid3={uuid.uuid4()}"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10)
            data = response.json()
            
            if data.get("code") != 0:
                return [{"title": "B站API鉴权失败", "desc": str(data), "hot": "⚠️降级", "plat": "bilibili"}]
            
            items = data.get("data", {}).get("list", [])[:8]
            
            return [
                {
                    "title": item["title"],
                    "desc": item.get("desc", "") or item.get("owner", {}).get("name", ""),
                    "hot": f"{item.get('stat', {}).get('view', 0)//10000}W 播放",
                    "url": item.get("short_link_v2") or f"https://www.bilibili.com/video/{item.get('bvid')}",
                    "plat": "bilibili"
                } for item in items
            ]
    except Exception as e:
        return [{"title": "B站请求失败", "desc": str(e), "hot": "⚠️降级", "plat": "bilibili"}]
