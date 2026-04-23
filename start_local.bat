@echo off
echo ==========================================
echo Starting Spirit Journey Rider Locally
echo ==========================================
echo.

echo [1/3] Starting Java Backend...
:: 使用用户目录下原有的 simple-start.bat，里面包含了您特定的 JDK 23 路径配置
start "Java Backend" cmd /k "cd /d "%~dp0java-backend" && simple-start.bat"

echo [2/3] Starting Python Backend...
:: 加入国内镜像加速 pip install
start "Python Backend" cmd /k "cd /d "%~dp0python-backend" && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && python app.py"

echo [3/3] Starting Vue Frontend...
:: 加入淘宝镜像加速 npm install
start "Vue Frontend" cmd /k "cd /d "%~dp0vue-cycling-app" && npm config set registry https://registry.npmmirror.com && npm install && npm run dev"

echo.
echo All services are starting in separate windows.
echo Frontend URL: http://localhost:5173
echo.
pause
