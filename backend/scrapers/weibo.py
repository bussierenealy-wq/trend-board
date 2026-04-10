import httpx

async def fetch_weibo():
    # Attempting a more direct route via the side panel API which is often more permissive
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://weibo.com/hot/weibo/102803",
        "Accept": "application/json, text/plain, */*"
    }
    
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # 1. Get initial cookies
            await client.get("https://weibo.com/hot/weibo/102803", headers=headers)
            
            # 2. Request the AJAX hot search data
            response = await client.get(url, headers=headers, timeout=10)
            
            if response.status_code == 403:
                # Fallback to mobile search API with extra params
                url_m = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtime"
                response = await client.get(url_m, headers=headers)
                
            data = response.json()
            
            # Parsing logic for different API structures
            hot_items = []
            
            # Case 1: weibo.com/ajax structure
            if "data" in data and isinstance(data["data"], dict) and "realtime" in data["data"]:
                for item in data["data"]["realtime"][:8]:
                    if item.get("is_ad"): continue
                    hot_items.append({
                        "title": item.get("word", ""),
                        "desc": f"微博热搜: {item.get('num', 0)} 实时流",
                        "hot": f"🔥 {item.get('category', '热搜')}",
                        "url": f"https://s.weibo.com/weibo?q=%23{item.get('word')}%23",
                        "plat": "weibo"
                    })
            
            # Case 2: m.weibo.cn structure
            elif "data" in data and "cards" in data["data"]:
                for card in data["data"]["cards"]:
                    group = card.get("card_group", [])
                    for item in group:
                        if item.get("promotion"): continue
                        hot_items.append({
                            "title": item.get("desc", ""),
                            "desc": item.get("desc_extr", "微博实时热搜"),
                            "hot": f"🔥 {item.get('desc_extr', '热')}",
                            "url": item.get("scheme", ""),
                            "plat": "weibo"
                        })
            
            return hot_items[:8] if hot_items else [{"title": "微博热搜暂无内容", "desc": "API 结构变化或触发风控", "hot": "⚠️ 降级", "plat": "weibo"}]
            
    except Exception as e:
        return [{"title": "微博抓取异常", "desc": str(e), "hot": "⚠️ 降级", "plat": "weibo"}]
