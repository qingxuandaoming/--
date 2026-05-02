# 使用 Python 3.9 slim 镜像（基于 Debian Bookworm）
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
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg \
    unzip \
    xvfb \
    # Chromium 浏览器与驱动（Debian 官方仓库保证版本一致）
    chromium \
    chromium-driver \
    # Chromium headless 运行所需的共享库
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    # 健康检查工具
    && rm -rf /var/lib/apt/lists/* \
    # 创建兼容性符号链接，使 Selenium 能找到可执行文件
    && ln -sf /usr/bin/chromium /usr/bin/google-chrome \
    && ln -sf /usr/bin/chromedriver /usr/local/bin/chromedriver \
    # 构建时验证：若版本输出失败则中断构建，保证镜像可用性
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
