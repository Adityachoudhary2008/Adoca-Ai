@echo off
REM Development startup script (Windows)

setlocal enabledelayedexpansion

echo 🚀 Adoca AI - Development Setup
echo ================================

where /q node
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js
    exit /b 1
)

where /q python
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    exit /b 1
)

echo 📦 Building frontend...
cd frontend
call npm install
call npm run build
cd ..

echo 🔧 Setting up backend...
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo To run in development:
echo   Terminal 1: python -m backend.main
echo   Terminal 2: cd frontend ^&^& npm run dev
echo.
echo Or use docker-compose for production-like environment:
echo   docker-compose up
echo.

pause
