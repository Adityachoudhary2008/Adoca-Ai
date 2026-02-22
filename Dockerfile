# Multi-stage Docker build for Adoca AI Assistant
# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package*.json ./
RUN npm ci --prefer-offline --no-audit

COPY frontend . .

# Build frontend
RUN npm run build

# Stage 2: Python runtime with backend and frontend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for curl (health check)
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend
COPY .env.example .

# Copy built frontend from builder stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create required directories
RUN mkdir -p logs data && chmod -R 755 logs data

# Expose port (default to 8000, can be overridden)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Run application (port configurable via PORT env var)
CMD ["python", "-m", "backend.main"]
