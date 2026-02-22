@echo off
REM Deploy script for production (Windows)

setlocal enabledelayedexpansion

echo 🚀 Adoca AI Deployment Script
echo ================================

if not exist ".env" (
    echo ❌ .env file not found
    echo Create .env from .env.example first
    exit /b 1
)

echo 📦 Building application...
docker-compose build --no-cache

echo 🧹 Stopping existing containers...
docker-compose down

echo 🚀 Starting application...
docker-compose up -d

echo ⏳ Waiting for application to be healthy...
timeout /t 10 /nobreak

echo.
echo ✅ Deployment complete!
echo.
echo 📊 Application Status:
docker-compose ps
echo.
echo 🌐 Access at:
echo   Frontend: http://localhost
echo   API: http://localhost:8000
echo   API Docs: http://localhost:8000/api/docs
echo.

pause
