# 选用官方提供的包含全部浏览器底层库的 Playwright 镜像作为底座
FROM mcr.microsoft.com/playwright/python:v1.38.0-jammy

WORKDIR /app

# 复制依赖配置
COPY requirements.txt .

# 关键：生产环境直接安装业务依赖，利用阿里云镜像加速
# 镜像已带 Playwright 内核，只需安装 python 包
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ \
    fastapi==0.103.2 \
    uvicorn==0.23.2 \
    httpx==0.25.0 \
    playwright==1.38.0

# 复制代码到容器
COPY . .

# 确保 Python 能跨文件夹找到 scrapers 模块
ENV PYTHONPATH=/app

# 暴露 8000 端口
EXPOSE 8000

# 启动 (Ubuntu 环境下 python3 更稳)
CMD ["python3", "backend/main.py"]
