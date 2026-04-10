import httpx
import re

async def fetch_wscn():
    url = "https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=global&limit=10"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, headers=headers)
            items = r.json().get("data", {}).get("items", [])
            results = []
            for it in items:
                content = it.get("content_text") or it.get("content")
                if not content: continue
                # Clean HTML tags
                clean_content = re.sub(r'<[^>]+>', '', content).strip()
                # Take first line or first 100 chars
                title = clean_content.split('\n')[0][:80]
                if not title: continue
                
                results.append({
                    "title": title,
                    "desc": "华尔街见闻 实时快讯",
                    "hot": "🌍 国际",
                    "url": f"https://wallstreetcn.com/live/global",
                    "plat": "wscn"
                })
                if len(results) >= 8: break
            return results
    except Exception as e:
        return [{"title": "华尔街见闻异常", "desc": str(e), "hot": "⚠️ 降级", "plat": "wscn"}]

async def fetch_cls():
    url = "https://www.cls.cn/nodeapi/telegraphList?rn=10&os=web&sv=7.7.2"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, headers=headers)
            items = r.json().get("data", {}).get("roll_data", [])
            results = []
            for it in items:
                title = it.get("title") or it.get("brief") or it.get("content")
                if not title: continue
                
                clean_title = re.sub(r'<[^>]+>', '', title).strip()
                
                results.append({
                    "title": clean_title[:80],
                    "desc": "财联社 电报快讯",
                    "hot": "💰 财经",
                    "url": f"https://www.cls.cn/roll",
                    "plat": "cls"
                })
                if len(results) >= 8: break
            return results
    except Exception as e:
        return [{"title": "财联社抓取异常", "desc": str(e), "hot": "⚠️ 降级", "plat": "cls"}]
