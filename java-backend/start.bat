@echo off
cd /d "%~dp0"
"%~1" -jar target\cycling-route-backend-1.0.0.jar > ..\java_logs.txt 2>&1
