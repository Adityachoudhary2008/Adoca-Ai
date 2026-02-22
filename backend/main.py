from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import os
from pathlib import Path

from backend.rag_orchestrator import RAGOrchestrator
from backend.config import settings
from backend.logger import logger

# Initialize FastAPI app
app = FastAPI(
    title="Adoca AI Assistant API",
    description="Production-grade RAG-based AI assistant for Adoca",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
try:
    rag_orchestrator = RAGOrchestrator()
    logger.info("RAG Orchestrator loaded successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG Orchestrator: {str(e)}")
    raise

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    user_id: str = "anonymous"

class QueryResponse(BaseModel):
    query: str
    response: str
    intent: str = None
    context_chunks: int = 0
    latency_ms: float = 0
    status: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    timestamp: str

# Routes

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.APP_ENV,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Main query endpoint.
    
    POST /query
    {
        "query": "What is RFQ?",
        "user_id": "user123"
    }
    """
    
    if not request.query or len(request.query.strip()) == 0:
        logger.warning("Empty query received")
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Process query through RAG
    try:
        result = rag_orchestrator.query(
            user_query=request.query,
            user_id=request.user_id
        )
        
        # Format response
        return {
            "query": request.query,
            "response": result["response"],
            "intent": result.get("intent", "unknown"),
            "context_chunks": result.get("context_chunks", 0),
            "latency_ms": result.get("latency_ms", 0),
            "status": result.get("status", "error"),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Query endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred processing your query"
        )

@app.get("/knowledge-base/stats")
async def kb_stats():
    """Get knowledge base statistics."""
    chunks = rag_orchestrator.kb.get_all_chunks()
    
    categories = {}
    for chunk in chunks:
        cat = chunk.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "total_chunks": len(chunks),
        "by_category": categories,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/knowledge-base/list")
async def kb_list():
    """List all knowledge base chunks (metadata only)."""
    chunks = rag_orchestrator.kb.get_all_chunks()
    
    metadata = [
        {
            "id": chunk["id"],
            "title": chunk.get("title", ""),
            "category": chunk.get("category", ""),
            "length_chars": len(chunk.get("content", ""))
        }
        for chunk in chunks
    ]
    
    return {
        "count": len(metadata),
        "chunks": metadata
    }

# Static files - serve frontend build
frontend_path = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_path.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_path / "assets")), name="assets")

@app.get("/")
async def root():
    """Serve index.html for SPA"""
    index_file = frontend_path / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    
    return {
        "app": "Adoca AI Personal Assistant",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/query (POST)",
            "kb_stats": "/knowledge-base/stats",
            "kb_list": "/knowledge-base/list",
            "docs": "/api/docs"
        }
    }

# Catch-all for SPA
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve index.html for all unmatched routes (SPA routing)."""
    index_file = frontend_path / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    raise HTTPException(status_code=404, detail="Frontend build not found")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Adoca AI Assistant API server...")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.LOG_LEVEL.lower()
    )
