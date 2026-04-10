from playwright.async_api import async_playwright

async def fetch_zhihu():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 800}
            )
            page = await context.new_page()

            await page.goto("https://www.zhihu.com/hot", wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(3000)

            dom_items = await page.evaluate('''() => {
                // 知乎热榜的每个条目结构: .HotList-item
                const items = document.querySelectorAll('.HotList-item');
                if (items.length > 0) {
                    return Array.from(items).slice(0, 8).map(item => {
                        const titleEl = item.querySelector('.HotList-itemTitle');
                        const metricEl = item.querySelector('.HotList-itemMetrics');
                        const linkEl = item.querySelector('a');
                        return {
                            title: titleEl ? titleEl.innerText.trim() : '无标题',
                            desc: metricEl ? metricEl.innerText.trim() : '知乎热榜',
                            hot: '🔥 热议中',
                            url: linkEl ? linkEl.href : 'https://www.zhihu.com/hot',
                            plat: 'zhihu'
                        };
                    });
                }
                // Fallback: 尝试从通用链接中提取
                return Array.from(document.querySelectorAll('a'))
                    .map(a => ({ text: a.innerText.trim(), href: a.href }))
                    .filter(a => a.text.length > 8 && a.href.includes('/question/') && !a.text.includes('登录'))
                    .slice(0, 8)
                    .map(a => ({
                        title: a.text.substring(0, 50) + (a.text.length > 50 ? '...' : ''),
                        desc: '知乎热榜提取',
                        hot: '🔥 热议中',
                        url: a.href,
                        plat: 'zhihu'
                    }));
            }''')
            await browser.close()
            if not dom_items:
                return [{"title": "知乎 DOM 结构变更", "desc": "风控拦截或页面暂无内容", "hot": "⚠️降级", "plat": "zhihu"}]
            return dom_items
    except Exception as e:
        return [{"title": "知乎请求失败", "desc": str(e), "hot": "⚠️降级", "plat": "zhihu"}]
