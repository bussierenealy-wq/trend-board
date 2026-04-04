import asyncio
from playwright.async_api import async_playwright

async def test_bili_dom():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.bilibili.com/v/popular/rank/all", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        dom = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('.video-card')).map(el => {
                const titleEl = el.querySelector('.video-name');
                const title = titleEl ? titleEl.innerText || titleEl.textContent : '';
                
                const upEl = el.querySelector('.up-name');
                const author = upEl ? upEl.innerText || upEl.textContent : '';
                
                const viewEl = el.querySelector('.play-text');
                const view = viewEl ? viewEl.innerText || viewEl.textContent : '';
                
                const url = titleEl?.href || el.querySelector('a')?.href || '';
                
                return { title, desc: author, hot: view + " 播放", url, plat: "bilibili" };
            });
        }''')
        
        # If .video-card doesn't work, maybe .rank-item
        if not dom:
            dom = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('.rank-item')).map(el => {
                    const titleEl = el.querySelector('.title');
                    const title = titleEl ? titleEl.innerText || titleEl.textContent : '';
                    
                    const upEl = el.querySelector('.up-name');
                    const author = upEl ? upEl.innerText || upEl.textContent : '';
                    
                    const viewEl = el.querySelector('.detail-state .data-box');
                    const view = viewEl ? viewEl.innerText || viewEl.textContent : '';
                    
                    const url = titleEl?.href || el.querySelector('a')?.href || '';
                    
                    return { title, desc: author, hot: view, url, plat: "bilibili" };
                });
            }''')

        print("DOM output:", len(dom), dom[:2] if dom else "EMPTY")
        await browser.close()

asyncio.run(test_bili_dom())
