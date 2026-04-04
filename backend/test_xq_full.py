import asyncio
from playwright.async_api import async_playwright

async def test_xq_full():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Navigate and bypass WAF
        await page.goto("https://xueqiu.com/", wait_until="domcontentloaded")
        print("Waiting for WAF to resolve...")
        await page.wait_for_timeout(5000) # Give it 5s to solve WAF and reload
        
        # Fetch directly inside page using its own context/tokens!
        try:
            data = await page.evaluate('''async () => {
                const res = await fetch("https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=-1&size=8");
                return await res.json();
            }''')
            print("XQ keys:", data.keys() if data else None)
            if data and 'items' in data:
                print("XQ items:", len(data['items']))
        except Exception as e:
            print("XQ Fetch Error:", e)
            
        # Fallback: DOM Extraction
        try:
            dom = await page.evaluate('''() => {
                const nodes = Array.from(document.querySelectorAll('a')).map(a => a.innerText);
                return nodes.filter(t => t && t.length > 10).slice(0, 5);
            }''')
            print("XQ DOM texts:", dom)
        except Exception as e:
             pass

        await browser.close()
asyncio.run(test_xq_full())
