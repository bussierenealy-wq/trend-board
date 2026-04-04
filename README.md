<p align="center">
  <h1 align="center">📡 TrendBoard — 多平台实时热点聚合大盘</h1>
  <p align="center">
    <em>一键穿透 Bilibili · 小红书 · 雪球，实时捕获全网热议资讯</em>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python" />
    <img src="https://img.shields.io/badge/FastAPI-0.103-009688?logo=fastapi" />
    <img src="https://img.shields.io/badge/Playwright-1.38-2EAD33?logo=playwright" />
    <img src="https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker" />
    <img src="https://img.shields.io/badge/License-MIT-green" />
  </p>
</p>

---

## ✨ 项目简介

**TrendBoard** 是一个高端画报风格的实时资讯聚合 Web 应用，支持从多个国内主流内容/金融平台抓取当前最热门的话题与内容，并以极简、高品质的卡片式界面统一呈现。

用户通过 **"立即同步"** 按钮主动触发数据抓取，点击任意卡片即可直达原文详情页——所见即所得，零中间环节。

### 🎯 支持平台

| 平台 | 数据源 | 抓取方式 |
|------|--------|---------|
| **Bilibili** | 全站热门排行榜 | REST API + buvid3 鉴权绕过 |
| **小红书** | 热门精选笔记 | Playwright 无头浏览器 DOM 提取 |
| **雪球** | 实时社区热议 | Playwright WAF 绕过 + DOM 剥离 |

---

## 🖼️ 界面预览

> 深色画报风格 · 卡片悬浮微交互 · 中文本地化 · 点击穿透原文

---

## 🚀 快速开始

### 方式一：本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/trend-board.git
cd trend-board

# 2. 安装依赖
pip install -r requirements.txt
playwright install chromium

# 3. 启动服务
python backend/main.py
```

浏览器访问 `http://localhost:8000` 即可。

### 方式二：Docker 一键部署（推荐）

```bash
# 构建镜像（含 Playwright Chromium 内核）
docker build -t trend-board .

# 启动容器
docker run -d --name trend-board -p 8000:8000 trend-board
```

浏览器访问 `http://<服务器IP>:8000`。

---

## 📁 项目结构

```
trend-board/
├── index.html              # 前端入口页面
├── style.css               # 高端画报风格样式表
├── script.js               # 前端交互逻辑（手动同步 + 卡片点击穿透）
├── Dockerfile              # 容器化构建文件
├── requirements.txt        # Python 依赖清单
└── backend/
    ├── main.py             # FastAPI 服务主入口（含静态文件托管）
    └── scrapers/
        ├── bilibili.py     # B站爬虫（API 直连 + buvid3 伪造）
        ├── xhs.py          # 小红书爬虫（Playwright DOM 提取）
        └── xueqiu.py       # 雪球爬虫（Playwright WAF 绕过）
```

---

## ⚙️ 技术架构

```
┌─────────────────────────────────────────────────┐
│                  浏览器前端                        │
│         index.html + style.css + script.js       │
│         (由 FastAPI StaticFiles 托管)              │
└──────────────────┬──────────────────────────────┘
                   │  fetch /api/trends | /api/sync
                   ▼
┌─────────────────────────────────────────────────┐
│              FastAPI 后端 (8000)                   │
│                 backend/main.py                   │
│           ┌─────┬─────────┬──────┐               │
│           ▼     ▼         ▼      │               │
│      bilibili  xhs     xueqiu   │               │
│      (httpx)  (PW)     (PW)     │               │
│           └─────┴─────────┴──────┘               │
│              asyncio.gather 并发                   │
└─────────────────────────────────────────────────┘
```

- **前端**：纯 HTML/CSS/JS，深色画报风格，无框架依赖
- **后端**：FastAPI + Uvicorn，异步并发抓取三大平台
- **爬虫引擎**：Bilibili 使用轻量 httpx API 直连；小红书/雪球使用 Playwright 无头浏览器绕过风控
- **部署**：Docker 容器化，基于微软官方 Playwright 镜像

---

## 🔧 API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/api/trends` | 获取当前缓存的各平台热点数据 |
| `POST` | `/api/sync` | 触发全平台数据同步并返回最新结果 |

---

## ☁️ 云端部署指南 (Ubuntu / 腾讯云)

> **核心原则**：生产环境务必使用 Docker 镜像化部署，以规避复杂的 Playwright 浏览器依赖。

### 1. 环境初始化
在 Ubuntu 服务器上快速安装 Docker：
```bash
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
sudo usermod -aG docker $USER && newgrp docker
```

### 2. 部署步骤
直接使用经过生产环境验证的 Dockerfile：
```bash
# 克隆仓库
git clone https://github.com/bussierenealy-wq/trend-board.git
cd trend-board

# 强制构建（建议禁用缓存以对齐最新依赖）
docker build --no-cache -t trend-board .

# 启动容器并持久化运行
docker run -d \
  --name trend-board \
  -p 8000:8000 \
  --restart always \
  trend-board
```

### ⚠️ 关键注意事项 (必读)

1. **内网加速**：若在腾讯云构建缓慢，建议配置 Docker 国内镜像加速（`/etc/docker/daemon.json`）。
2. **端口穿透（三级检查）**：
   - **云平台层**：腾讯云后台安全组必须开放 **TCP 8000** 端口。
   - **系统层**：Ubuntu `ufw` 防火墙需执行 `sudo ufw allow 8000/tcp`。
   - **业务层**：监听地址已锁死为 `0.0.0.0`，请勿修改。
3. **依赖闭环**：Dockerfile 已预装 `playwright==1.38.0` 及其运行时环境，请勿在宿主机直接 `pip install`。
4. **日志监控**：若无法启动，执行 `docker logs -f trend-board` 查看实时 Traceback。

---

## 📝 开发说明

- **数据缓存**：当前采用内存缓存，服务重启后需重新同步。如需持久化可接入 Redis/SQLite。
- **请求频率**：前端已移除自动轮询，仅在用户点击"立即同步"时触发抓取，降低被平台风控拦截的概率。
- **风控应对**：各平台爬虫内置了降级兜底机制，即使某一平台暂时不可用，其他平台数据仍正常展示。

---

## 📜 License

[MIT](LICENSE) — 仅供学习交流使用，请勿用于商业用途或高频爬取。

---

<p align="center">
  <sub>Built with ❤️ by TrendBoard Team</sub>
</p>
