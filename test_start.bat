@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo Starting Spirit Journey Rider Locally
echo ==========================================
echo.

set "JAVA_CMD=C:\Users\92534\.jdks\temurin-24\bin\java.exe"
echo [INFO] Using: %JAVA_CMD%
echo [TEST] java version check skipped
echo.

if not exist "%~dp0java-backend\target\cycling-route-backend-1.0.0.jar" (
    echo [ERROR] Java backend JAR not found!
    pause
    exit /b 1
)

if not exist "%~dp0python-backend\.venv\Scripts\python.exe" (
    echo [ERROR] Python virtual env not found!
    pause
    exit /b 1
)

if not exist "%~dp0vue-cycling-app\node_modules" (
    echo [ERROR] Frontend dependencies not found!
    pause
    exit /b 1
)

echo [INFO] Checking backend ports...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080 " ^| findstr "LISTENING"') do (
    echo [WARN] Port 8080 is in use by PID %%a. Stopping it...
    taskkill /F /PID %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000 " ^| findstr "LISTENING"') do (
    echo [WARN] Port 5000 is in use by PID %%a. Stopping it...
    taskkill /F /PID %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
)

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

echo [ERROR] All ports are in use!
pause
exit /b 1

:port_found
echo.

echo [1/3] Starting Java Backend...
echo [TEST] Would start Java backend here

echo [2/3] Starting Python Backend (with scheduler)...
echo [TEST] Would start Python backend here

echo [3/3] Starting Vue Frontend on port %FRONTEND_PORT%...
echo [TEST] Would start frontend here
echo.
echo ==========================================
echo   Frontend URL: http://localhost:%FRONTEND_PORT%
echo   Java API:     http://localhost:8080/api
echo   Python API:   http://localhost:5000/api
echo ==========================================
echo.

cd /d "%~dp0vue-cycling-app"
echo [TEST] cd result: %cd%
echo [TEST] Would run: npm run dev -- --port %FRONTEND_PORT%

echo.
echo [INFO] Stopping backend services...
echo [TEST] Cleanup complete.

echo.
echo All services stopped.
pause
