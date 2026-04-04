import httpx
import asyncio

async def test_xueqiu():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    async with httpx.AsyncClient() as client:
        resp1 = await client.get("https://xueqiu.com/", headers=headers, timeout=10)
        print("Xueqiu cookie:", resp1.cookies)
        url = "https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=-1&size=8"
        resp2 = await client.get(url, headers=headers, cookies=resp1.cookies, timeout=10)
        print("Xueqiu status:", resp2.status_code)
        print("Xueqiu resp:", resp2.text[:200])

asyncio.run(test_xueqiu())
