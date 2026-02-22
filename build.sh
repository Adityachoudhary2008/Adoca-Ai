#!/bin/bash
# Development startup script

echo "🚀 Adoca AI - Development Mode"
echo "================================"

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js"
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "🔧 Setting up backend..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run in development:"
echo "  Terminal 1: python -m backend.main"
echo "  Terminal 2: cd frontend && npm run dev"
echo ""
echo "Or use docker-compose for production-like environment:"
echo "  docker-compose up"
