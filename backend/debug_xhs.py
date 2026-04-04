from playwright.async_api import async_playwright
import asyncio

async def test_xhs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = await context.new_page()
        
        async def handle_response(response):
            if "explore" in response.url or "homefeed" in response.url or "notes" in response.url:
                print("Intercepted:", response.url, "Status:", response.status)
                try:
                    data = await response.json()
                    print("Data keys:", data.keys())
                except:
                    pass
        
        page.on("response", handle_response)
        
        print("Navigating to explore...")
        try:
            await page.goto("https://www.xiaohongshu.com/explore", wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(3000)
        except Exception as e:
            print("Error navigating:", e)
        print("Done wait")
        await browser.close()

asyncio.run(test_xhs())
