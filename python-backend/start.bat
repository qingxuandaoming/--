@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" start.py > ..\python_logs.txt 2>&1
