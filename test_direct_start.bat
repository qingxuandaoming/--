@echo off
cd /d "%~dp0"
set "JAVA_CMD=C:\Users\92534\.jdks\temurin-24\bin\java.exe"
cd /d "%~dp0java-backend"
start /MIN "" "%JAVA_CMD%" -jar target\cycling-route-backend-1.0.0.jar
timeout /t 15 /nobreak >nul
