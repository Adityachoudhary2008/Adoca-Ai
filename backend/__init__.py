"""
Initialization file for backend module.
"""

from backend.config import settings
from backend.logger import logger
from backend.knowledge_base import initialize_knowledge_base, KnowledgeBase
from backend.sarvam_client import SarvamAIClient
from backend.search_engine import VectorSearch, ContextBuilder
from backend.safeguards import IntentDetector, AntiHallucinationFilter
from backend.rag_orchestrator import RAGOrchestrator

__all__ = [
    "settings",
    "logger",
    "initialize_knowledge_base",
    "KnowledgeBase",
    "SarvamAIClient",
    "VectorSearch",
    "ContextBuilder",
    "IntentDetector",
    "AntiHallucinationFilter",
    "RAGOrchestrator",
]
