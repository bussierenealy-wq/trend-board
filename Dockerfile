# 选用官方提供的包含全部浏览器底层库的 Playwright 镜像作为底座
FROM mcr.microsoft.com/playwright/python:v1.38.0-jammy

WORKDIR /app

# 复制依赖配置并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 为了确保 Playwright Chromium 内核能够稳定运行，强制重装一次浏览器核心（保险起见）
RUN playwright install chromium

# 复制代码到容器
COPY . .

# 暴露 8000 端口（云服务器需安全组放行）
EXPOSE 8000

# 启动守护进程，绑定到全部网络接口
CMD ["python", "backend/main.py"]
