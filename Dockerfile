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

# Install system dependencies for curl (health check) and venv support
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl gcc libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and install Python dependencies into it
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip setuptools wheel \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend
COPY .env.example .

# Copy built frontend from builder stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create runtime directories and a non-root user
RUN mkdir -p /app/logs /app/data \
    && groupadd --system appgroup || true \
    && useradd --system --gid appgroup --create-home --home-dir /nonexistent appuser || true \
    && chown -R appuser:appgroup /app

# Expose the port used by the app (Render uses 10000 in logs)
ENV PORT=10000
EXPOSE 10000

# Health check (uses PORT env var)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Ensure runtime uses venv
ENV PATH="/opt/venv/bin:$PATH"

# Run as non-root user
USER appuser

# Run application (port configurable via PORT env var)
CMD ["python", "-m", "backend.main"]
