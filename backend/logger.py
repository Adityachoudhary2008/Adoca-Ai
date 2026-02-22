import logging
import os
from datetime import datetime
from backend.config import settings

# Create logs directory if it doesn't exist
os.makedirs(settings.LOG_PATH, exist_ok=True)

# Configure logging
logger = logging.getLogger("adoca_ai")
logger.setLevel(getattr(logging, settings.LOG_LEVEL))

# File handler
log_filename = os.path.join(settings.LOG_PATH, f"adoca_ai_{datetime.now().strftime('%Y%m%d')}.log")
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_query(user_id: str, query: str, intent: str):
    """Log user query."""
    logger.info(f"QUERY | User: {user_id} | Intent: {intent} | Query: {query}")

def log_response(user_id: str, response: str, context_chunks: int, latency_ms: float):
    """Log AI response."""
    logger.info(f"RESPONSE | User: {user_id} | Chunks: {context_chunks} | Latency: {latency_ms}ms")

def log_error(error_type: str, error_msg: str, context: str = None):
    """Log errors."""
    msg = f"ERROR | Type: {error_type} | Message: {error_msg}"
    if context:
        msg += f" | Context: {context}"
    logger.error(msg)
