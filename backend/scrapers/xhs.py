import httpx

async def fetch_xhs():
    # Strategy 3: Target the secondary CDN or mobile web search entry point
    # Some older endpoints or specific search routes are less heavily guarded by WAF
    url = "https://www.xiaohongshu.com/discovery/item/656eb3b1000000000d00f6b3" # Example static node to get cookies
    hot_search_url = "https://www.xiaohongshu.com/web_api/sns/v2/system/hot_query" # Public search hot queries
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Referer": "https://www.xiaohongshu.com/",
        "Accept": "application/json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            # Get basic cookies to avoid 403 on API
            await client.get("https://www.xiaohongshu.com/", headers=headers)
            
            # Try to get the hot queries/trends directly
            resp = await client.get(hot_search_url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                queries = data.get("data", {}).get("queries", [])
                if queries:
                    return [
                        {
                            "title": q.get("query", "小红书热议"),
                            "desc": "热门搜索动态词",
                            "hot": "🌸 热搜中",
                            "url": f"https://www.xiaohongshu.com/search_result?keyword={q.get('query')}",
                            "plat": "xhs"
                        } for q in queries[:8]
                    ]
            
            # Fallback to a fixed but interesting set if the API is totally blocked
            # This ensures the UI never looks "broken" while we fight the WAF
            return [
                {
                    "title": "小红书社区风控维护中",
                    "desc": "数据抓取引擎正在对抗 WAF 盾",
                    "hot": "⚠️ 降级",
                    "url": "https://www.xiaohongshu.com/",
                    "plat": "xhs"
                }
            ]
            
    except Exception as e:
        return [{"title": "小红书网络异常", "desc": str(e), "hot": "⚠️ 降级", "plat": "xhs"}]
