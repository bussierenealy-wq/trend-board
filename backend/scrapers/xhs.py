from playwright.async_api import async_playwright

async def fetch_xhs():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 800}
            )
            page = await context.new_page()
            
            await page.goto("https://www.xiaohongshu.com/explore", wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(3000)
            dom_items = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('.note-item')).map(el => {
                    const title = el.querySelector('.title, .name')?.innerText || 'No Title';
                    const author = el.querySelector('.author, .name')?.innerText || 'XHS User';
                    const like = el.querySelector('.like, .count')?.innerText || 'Hot';
                    const linkUrl = el.querySelector('a')?.href || '';
                    return {title, desc: author, hot: like + ' 赞', url: linkUrl, plat: 'xhs'};
                });
            }''')
            results = [x for x in dom_items if x['title'] != 'No Title'][:8]
            await browser.close()
            
            if not results:
                return [{"title": "小红书 DOM解析无数据", "desc": "可能被滑块拦截", "hot": "⚠️降级", "plat": "xhs"}]
            return results
    except Exception as e:
        return [{"title": "小红书引擎遇到了强风控拦截", "desc": str(e), "hot": "⚠️降级", "plat": "xhs"}]
