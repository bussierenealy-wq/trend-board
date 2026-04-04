from playwright.async_api import async_playwright

async def fetch_xueqiu():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 800}
            )
            page = await context.new_page()
            
            await page.goto("https://xueqiu.com/", wait_until="domcontentloaded", timeout=15000)
            # Wait longer for Xueqiu's WAF challenge to self-resolve
            await page.wait_for_timeout(4000)
            
            dom_items = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('a'))
                    .map(a => ({ text: a.innerText.trim(), href: a.href }))
                    .filter(a => a.text.length > 10 && !a.text.includes('指数') && !a.text.includes('修改于') && !a.text.includes('登录'))
                    .slice(0, 8)
                    .map(a => ({
                        title: a.text.substring(0, 45) + (a.text.length > 45 ? '...' : ''),
                        desc: "雪球实时社区提取",
                        hot: "🔥 热议中",
                        url: a.href,
                        plat: "xueqiu"
                    }));
            }''')
            await browser.close()
            if not dom_items:
                 return [{"title": "雪球 DOM结构变更", "desc": "WAF 拦截或页面暂无内容", "hot": "⚠️降级", "plat": "xueqiu"}]
            return dom_items
    except Exception as e:
        return [{"title": "雪球网络超时或抛出异常", "desc": str(e), "hot": "⚠️降级", "plat": "xueqiu"}]
