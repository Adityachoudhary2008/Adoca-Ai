@echo off
REM startup.bat - Quick startup script for development (Windows)

echo ================================
echo Adoca AI Assistant - Startup
echo ================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Check virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/Update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check .env file
if not exist ".env" (
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo WARNING: Edit .env and add your SARVAM_API_KEY
    echo.
    pause
    exit /b 1
)

REM Create required directories
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "knowledge_base" mkdir knowledge_base

REM Start server
echo.
echo ================================
echo Starting server...
echo ================================
echo Server will run at http://localhost:8000
echo API docs at http://localhost:8000/docs
echo Redoc at http://localhost:8000/redoc
echo.

python -m backend.main
pause
