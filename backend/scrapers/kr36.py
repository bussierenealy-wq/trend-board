import httpx
import json
import re

async def fetch_36kr():
    # 使用快讯页面获取最实时的数据
    url = "https://36kr.com/newsflashes"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://36kr.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            html = response.text
            
            # RCA RCA RCA: 36kr 的数据路径极其深
            # window.initialState -> newsflashCatalogData -> data -> newsflashList -> data -> itemList
            # 或者是直接搜索 JSON 块
            
            json_pattern = r'window\.initialState\s*=\s*(\{.*?\})\s*</script>'
            match = re.search(json_pattern, html, re.DOTALL)
            
            if not match:
                # 最后的兜底：如果 JSON 提取失败，尝试更激进的字符串切割
                if 'window.initialState=' in html:
                    content = html.split('window.initialState=')[1]
                    json_str = content.split('</script>')[0].strip()
                    if json_str.endswith(';'): json_str = json_str[:-1]
                    data_obj = json.loads(json_str)
                else:
                    raise Exception("No initial state found")
            else:
                data_obj = json.loads(match.group(1))

            # 遍历 36kr 复杂的嵌套结构
            results = []
            try:
                # 路径 1: 新版结构
                catalog = data_obj.get("newsflashCatalogData", {})
                item_list = catalog.get("data", {}).get("newsflashList", {}).get("data", {}).get("itemList", [])
                
                if not item_list:
                    # 路径 2: 首页热榜结构 (如果快讯页刚好没数据)
                    item_list = data_obj.get("hotPostsData", {}).get("data", {}).get("itemList", [])

                for item in item_list:
                    # 36kr 不同类型的卡片字段不同
                    # 快讯使用 templateMaterial.widgetTitle
                    # 热门文章使用 templateData.itemTitle
                    material = item.get("templateMaterial", {})
                    template = item.get("templateData", {})
                    
                    title = material.get("widgetTitle") or template.get("itemTitle") or template.get("title")
                    item_id = item.get("itemId") or item.get("id")
                    
                    if not title or not item_id: continue
                    
                    # 清洗标题中的 HTML 标签或转义符
                    title = re.sub(r'<.*?>', '', title).replace('\\u002F', '/').replace('&quot;', '"')
                    
                    results.append({
                        "title": title,
                        "desc": "36Kr 实时商业快讯",
                        "hot": "🚀 深度",
                        "url": f"https://36kr.com/newsflashes/{item_id}",
                        "plat": "36kr"
                    })
                    
                    if len(results) >= 8: break
            except Exception as e:
                print(f"36Kr Extract Error: {e}")

            if results:
                return results
            else:
                # 最终兜底：利用刚才 Command Output 里的 widgetTitle 进行暴力正则
                raw_titles = re.findall(r'"widgetTitle":"(.*?)"', html)
                raw_ids = re.findall(r'"itemId":(\d+)', html)
                for t, mid in zip(raw_titles, raw_ids):
                    results.append({
                        "title": t.encode().decode('unicode_escape', 'ignore'),
                        "desc": "36Kr 暴力提取流",
                        "hot": "🚀 实时",
                        "url": f"https://36kr.com/newsflashes/{mid}",
                        "plat": "36kr"
                    })
                    if len(results) >= 8: break
                return results

    except Exception as e:
        return [{"title": "36氪抓取异常", "desc": str(e), "hot": "⚠️ 降级", "plat": "36kr"}]
