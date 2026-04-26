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
)
call venv\Scripts\activate.bat
pip install -r requirements.txt -q
echo.

echo [3/5] Install frontend deps...
cd /d "%~dp0frontend"
call npm install
echo.

echo [4/5] Build frontend...
call npm run build
echo.

echo [5/5] Start backend...
cd /d "%~dp0backend"
echo.
echo ========================================
echo   Server running
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo ========================================
echo.
uvicorn main:app --host 0.0.0.0 --port 8000
