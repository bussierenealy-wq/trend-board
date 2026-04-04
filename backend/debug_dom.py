from playwright.async_api import async_playwright
import asyncio

async def test_dom():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = await context.new_page()
        
        print("Testing Xueqiu DOM")
        await page.goto("https://xueqiu.com/", wait_until="networkidle")
        xq_text = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('a')).map(a => a.innerText).filter(t => t.length > 5);
        }''')
        print("XQ Elements found:", len(xq_text), xq_text[:10])
        
        print("Testing XHS DOM")
        await page.goto("https://www.xiaohongshu.com/explore", wait_until="networkidle")
        xhs_titles = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('.title, .name')).map(x => x.innerText || x.textContent);
        }''')
        print("XHS Elements found:", len(xhs_titles), xhs_titles[:10])

        await browser.close()

asyncio.run(test_dom())
