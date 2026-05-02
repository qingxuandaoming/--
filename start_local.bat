@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo Starting Spirit Journey Rider Locally
echo ==========================================
echo.

:: 检测前端可用端口（5500 -> 5510 -> 5520）
set "FRONTEND_PORT="
for %%p in (5500 5510 5520) do (
    netstat -ano | findstr "LISTENING" | findstr ":%%p " >nul 2>&1
    if errorlevel 1 (
        set "FRONTEND_PORT=%%p"
        echo [OK] Frontend port %%p is available.
        goto :port_found
    ) else (
        echo [WARN] Port %%p is in use, trying next...
    )
)

echo [ERROR] All ports ^(5500, 5510, 5520^) are in use! Please free one and retry.
pause
exit /b 1

:port_found
echo.

echo [1/3] Starting Java Backend...
start "Java Backend" cmd /k "cd /d "%~dp0java-backend" && simple-start.bat"

echo [2/3] Starting Python Backend...
start "Python Backend" cmd /k "cd /d "%~dp0python-backend" && .venv\Scripts\python.exe app.py"

echo [3/3] Starting Vue Frontend on port %FRONTEND_PORT%...
start "Vue Frontend" cmd /k "cd /d "%~dp0vue-cycling-app" && npm run dev -- --port %FRONTEND_PORT%"

echo.
echo All services are starting in separate windows.
echo Frontend URL: http://localhost:%FRONTEND_PORT%
echo Java API: http://localhost:8080/api
echo Python API: http://localhost:5000/api
echo.
pause
