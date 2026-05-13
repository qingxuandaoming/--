# 使用 Python 3.9 slim 镜像（基于 Debian）
FROM python:3.9-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    CHROME_BINARY_PATH=/usr/bin/google-chrome \
    CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# 安装系统依赖与 Chromium（含自动匹配版本的 chromedriver）
# 合并为单个 RUN 以减少镜像层数，并在最后清理 apt 缓存
# 注意：不要在 RUN 的 \ 继续行中插入 Dockerfile 注释，会中断命令
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl gnupg unzip xvfb \
    chromium chromium-driver \
    libglib2.0-0 libnss3 libfontconfig1 libxrender1 \
    libxtst6 libxi6 libxss1 libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 \
    libnspr4 libxcomposite1 libxdamage1 \
    libxfixes3 libxkbcommon0 libxrandr2 \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/chromium /usr/bin/google-chrome \
    && ln -sf /usr/bin/chromedriver /usr/local/bin/chromedriver \
    && echo "=== Chromium ===" && chromium --version \
    && echo "=== ChromeDriver ===" && chromedriver --version

# 复制并安装 Python 依赖（利用 Docker 层缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建日志目录
RUN mkdir -p /app/logs

# 暴露端口
EXPOSE 5000

# 健康检查：服务启动后 40 秒开始，每 30 秒检查一次
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# 启动命令
CMD ["python", "start.py"]
