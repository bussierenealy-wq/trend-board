import asyncio
from playwright.async_api import async_playwright
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def run():
    try:
        async with async_playwright() as p:
            print("Action: Mobile Infiltration...")
            # Emulate an iPhone 13
            iphone_13 = p.devices['iPhone 13']
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(**iphone_13)
            page = await context.new_page()
            
            # Use the billboard URL which is simpler than the main hot page
            await page.goto("https://www.zhihu.com/billboard", timeout=60000)
            await page.wait_for_timeout(5000)
            
            analysis = await page.evaluate('''() => {
                const results = [];
                // Target generic link containers that look like question links
                const links = Array.from(document.querySelectorAll('a'))
                    .filter(a => a.href.includes('/question/') && a.innerText.length > 5);
                
                return links.slice(0, 8).map(a => ({
                    title: a.innerText.split('\\n')[0].trim(),
                    url: a.href,
                    hot: '🔥 Zhihu Hot'
                }));
            }''')
            
            print(f"Title: {await page.title()}")
            print(f"Captured: {len(analysis)}")
            for idx, item in enumerate(analysis):
                print(f"{idx+1}. {item['title']} | {item['url']}")
            
            await browser.close()
    except Exception as e:
        print(f"Mobile Crash: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run())
