import asyncio
from playwright.async_api import async_playwright

async def test_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        print("--- XUEQIU ---")
        try:
            await page.goto("https://xueqiu.com/", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            data = await page.evaluate('''async () => {
                const res = await fetch("https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=-1&size=8");
                return await res.json();
            }''')
            print("XQ keys:", data.keys() if data else None)
        except Exception as e:
            print("XQ Error:", e)

        print("--- Xiaohongshu ---")
        try:
            await page.goto("https://www.xiaohongshu.com/explore", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            dom_items = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('.note-item')).map(el => {
                    const title = el.querySelector('.title, .name')?.innerText || 'No Title';
                    const author = el.querySelector('.author, .name')?.innerText || 'XHS User';
                    const like = el.querySelector('.like, .count')?.innerText || 'Hot';
                    return {title, desc: author, hot: like + ' 赞', plat: 'xhs'};
                });
            }''')
            print("XHS Dom len:", len(dom_items), dom_items[:2])
            
            # XHS alternative endpoints if DOM is weak
            state = await page.evaluate('() => window.__INITIAL_STATE__')
            print("XHS State initialized:", type(state))
        except Exception as e:
            print("XHS Error:", e)

        await browser.close()

asyncio.run(test_all())
