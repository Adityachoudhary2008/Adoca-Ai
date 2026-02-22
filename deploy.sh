#!/bin/bash
# Deploy script for production

set -e

echo "🚀 Adoca AI Deployment Script"
echo "================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check environment
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found${NC}"
    echo "Create .env from .env.example first"
    exit 1
fi

# Load env
source .env

echo -e "${YELLOW}📦 Building application...${NC}"
docker-compose build --no-cache

echo -e "${YELLOW}🧹 Stopping existing containers...${NC}"
docker-compose down || true

echo -e "${YELLOW}🚀 Starting application...${NC}"
docker-compose up -d

# Wait for health check
echo -e "${YELLOW}⏳ Waiting for application to be healthy...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo -e "${GREEN}✅ Application is healthy!${NC}"
        break
    fi
    echo "  Attempt $i/30..."
    sleep 1
done

# Show status
echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📊 Application Status:"
docker-compose ps
echo ""
echo "📝 Logs:"
docker-compose logs --tail=20
echo ""
echo "🌐 Access at:"
echo "  Frontend: http://localhost"
echo "  API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/api/docs"
