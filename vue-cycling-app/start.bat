@echo off
cd /d "%~dp0"
npm run dev -- --port %~1
