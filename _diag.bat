@echo off
setlocal enabledelayedexpansion
echo ==========================================
echo DIAGNOSTIC OUTPUT
echo ==========================================
echo.
echo dp0 = [%~dp0]
echo.
echo --- JAR check ---
echo Path tested: [%~dp0java-backend\target\cycling-route-backend-1.0.0.jar]
if exist "%~dp0java-backend\target\cycling-route-backend-1.0.0.jar" (
    echo JAR: FOUND
) else (
    echo JAR: MISSING
    echo Trying relative path...
    if exist "java-backend\target\cycling-route-backend-1.0.0.jar" (
        echo JAR via relative: FOUND
    ) else (
        echo JAR via relative: MISSING
    )
)
echo.
echo --- VENV check ---
echo Path: [%~dp0python-backend\.venv\Scripts\python.exe]
if exist "%~dp0python-backend\.venv\Scripts\python.exe" (echo VENV: FOUND) else (echo VENV: MISSING)
echo.
echo --- node_modules check ---
if exist "%~dp0vue-cycling-app\node_modules" (echo node_modules: FOUND) else (echo node_modules: MISSING)
echo.
echo --- JAVA_HOME ---
echo JAVA_HOME=[%JAVA_HOME%]
echo.
echo --- where java ---
where java.exe 2>nul || echo java NOT IN PATH
echo.
echo DONE
pause
