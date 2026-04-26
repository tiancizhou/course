@echo off
title Calligraphy Course Manager

echo ========================================
echo   Calligraphy Course Manager - Start
echo ========================================
echo.

echo [1/5] Git pull...
git pull
if %errorlevel% neq 0 (
    echo [WARN] git pull failed, using local code
)
echo.

echo [2/5] Install backend deps...
cd /d "%~dp0backend"
if not exist venv (
    echo Creating venv...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)
call venv\Scripts\activate.bat
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install backend dependencies
    pause
    exit /b 1
)
echo.

echo [3/5] Install frontend deps...
cd /d "%~dp0frontend"
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install frontend dependencies
    pause
    exit /b 1
)
echo.

echo [4/5] Build frontend...
call npm run build
if %errorlevel% neq 0 (
    echo [ERROR] Failed to build frontend
    pause
    exit /b 1
)
echo.

echo [5/5] Start backend...
cd /d "%~dp0backend"
echo.
echo ========================================
echo   Server running
echo   Backend:  http://localhost:6000
echo   API Docs: http://localhost:6000/docs
echo   Press Ctrl+C to stop
echo ========================================
echo.
call venv\Scripts\activate.bat
uvicorn main:app --host 127.0.0.1 --port 6000
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server failed to start
    pause
)
