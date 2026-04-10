from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import asyncio
from scrapers.bilibili import fetch_bilibili
from scrapers.xueqiu import fetch_xueqiu
from scrapers.xhs import fetch_xhs
from scrapers.weibo import fetch_weibo
from scrapers.kr36 import fetch_36kr
from scrapers.financial import fetch_wscn, fetch_cls
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = {
    "bilibili": [],
    "xueqiu": [],
    "xhs": [],
    "weibo": [],
    "36kr": [],
    "wscn": [],
    "cls": []
}

fallback_data = {
    "bilibili": [{"title": "System Booting", "desc": "等待B站 API 并发连接...", "hot": "Init"}],
    "xueqiu": [{"title": "Data Pipeline", "desc": "正在向雪球申请令牌 Token...", "hot": "Init"}],
    "xhs": [{"title": "Playwright Engine", "desc": "正在拉起隐身浏览器突破小红书风控墙...", "hot": "Init"}],
    "weibo": [{"title": "Weibo Connect", "desc": "正在连接微博热搜实时接口...", "hot": "Init"}],
    "36kr": [{"title": "36Kr Insight", "desc": "正在获取商业前沿快讯...", "hot": "Init"}],
    "wscn": [{"title": "WSCN Live", "desc": "正在连接华尔街见闻实时电报...", "hot": "Init"}],
    "cls": [{"title": "CLS Telegraph", "desc": "正在请求财联社一线电报数据...", "hot": "Init"}]
}

async def update_cache():
    tasks = [
        fetch_bilibili(),
        fetch_xueqiu(),
        fetch_xhs(),
        fetch_weibo(),
        fetch_36kr(),
        fetch_wscn(),
        fetch_cls()
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    if not isinstance(results[0], Exception) and results[0]: cache["bilibili"] = results[0]
    else: print("Bilibili Error:", results[0])
        
    if not isinstance(results[1], Exception) and results[1]: cache["xueqiu"] = results[1]
    else: print("Xueqiu Error:", results[1])

    if not isinstance(results[2], Exception) and results[2]: cache["xhs"] = results[2]
    else: print("XHS Error:", results[2])

    if not isinstance(results[3], Exception) and results[3]: cache["weibo"] = results[3]
    else: print("Weibo Error:", results[3])

    if not isinstance(results[4], Exception) and results[4]: cache["36kr"] = results[4]
    else: print("36Kr Error:", results[4])

    if not isinstance(results[5], Exception) and results[5]: cache["wscn"] = results[5]
    else: print("WSCN Error:", results[5])

    if not isinstance(results[6], Exception) and results[6]: cache["cls"] = results[6]
    else: print("CLS Error:", results[6])

@app.on_event("startup")
async def startup_event():
    global cache
    cache = fallback_data.copy()
    asyncio.create_task(update_cache())

@app.get("/api/trends")
async def get_trends():
    return cache

@app.post("/api/sync")
async def force_sync():
    await update_cache()
    return cache

frontend_path = os.path.join(os.path.dirname(__file__), "..")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
