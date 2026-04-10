import asyncio
from playwright.async_api import async_playwright
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def run():
    try:
        async with async_playwright() as p:
            print("Action: Deep Crawl Zhihu...")
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Disable heavy resources
            await page.route("**/*.{png,jpg,jpeg,ttf,woff,woff2,css}", lambda route: route.abort())
            
            await page.goto("https://www.zhihu.com/hot", timeout=60000)
            await page.wait_for_timeout(3000)
            
            # Analyze page content
            analysis = await page.evaluate('''() => {
                const res = {};
                res.title = document.title;
                res.hotItems = Array.from(document.querySelectorAll('.HotItem'))
                    .map(div => ({
                        title: div.querySelector('.HotItem-title')?.innerText || 'NoTitle',
                        metrics: div.querySelector('.HotItem-metrics')?.innerText || 'NoMetrics'
                    }));
                // Fallback links
                res.fallbackLinks = Array.from(document.querySelectorAll('a'))
                    .filter(a => a.href.includes('zhihu.com/question/'))
                    .slice(0, 5)
                    .map(a => a.innerText.substring(0, 30));
                return res;
            }''')
            
            print(f"Page Title: {analysis['title']}")
            print(f"Found {len(analysis['hotItems'])} HotItems")
            for item in analysis['hotItems'][:5]:
                print(f"- {item['title']} ({item['metrics']})")
            
            if not analysis['hotItems']:
                print(f"Fallback Links: {analysis['fallbackLinks']}")
                
            await browser.close()
    except Exception as e:
        print(f"Final Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run())
