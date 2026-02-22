#!/bin/bash
# startup.sh - Quick startup script for development

echo "================================"
echo "Adoca AI Assistant - Startup"
echo "================================"

# Check Python
if ! command -v python &> /dev/null; then
    echo "Python not found. Please install Python 3.11+"
    exit 1
fi

# Check virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/Update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check .env file
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and add your SARVAM_API_KEY"
    exit 1
fi

# Create required directories
mkdir -p logs data knowledge_base

# Start server
echo ""
echo "================================"
echo "Starting server..."
echo "================================"
echo "Server will run at http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
echo "Redoc at http://localhost:8000/redoc"
echo ""

python -m backend.main
