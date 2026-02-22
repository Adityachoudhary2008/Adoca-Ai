import numpy as np
from typing import List, Dict
from backend.config import settings
from backend.logger import logger

class VectorSearch:
    """Vector search using cosine similarity."""
    
    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        try:
            a = np.array(vec1)
            b = np.array(vec2)
            
            dot_product = np.dot(a, b)
            return float(dot_product)  # Already normalized
        except Exception as e:
            logger.error(f"Cosine similarity error: {str(e)}")
            return 0.0
    
    @staticmethod
    def search(query_embedding: List[float], all_chunks: List[Dict], 
               min_chunks: int = None, max_chunks: int = None) -> List[Dict]:
        """
        Search knowledge base using cosine similarity.
        Returns top-k most similar chunks.
        """
        if min_chunks is None:
            min_chunks = settings.MIN_CONTEXT_CHUNKS
        if max_chunks is None:
            max_chunks = settings.MAX_CONTEXT_CHUNKS
        
        if not all_chunks:
            logger.warning("No chunks to search in knowledge base")
            return []
        
        # Score all chunks
        scored_chunks = []
        for chunk in all_chunks:
            if "embedding" not in chunk:
                logger.warning(f"Chunk {chunk['id']} missing embedding")
                continue
            
            similarity = VectorSearch.cosine_similarity(
                query_embedding,
                chunk["embedding"]
            )
            
            scored_chunks.append({
                **chunk,
                "similarity": similarity
            })
        
        # Sort by similarity
        scored_chunks.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Apply chunk limits
        result_count = max(min_chunks, min(len(scored_chunks), max_chunks))
        results = scored_chunks[:result_count]
        
        logger.info(f"Search returned {len(results)} chunks (min:{min_chunks}, max:{max_chunks})")
        
        return results

class ContextBuilder:
    """Build context from retrieved chunks - STRICT NO MODIFICATION."""
    
    @staticmethod
    def build_context(chunks: List[Dict]) -> str:
        """
        Build context block from chunks.
        RULE: No modification, no summarization, no extra text.
        """
        if not chunks:
            return ""
        
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            # Format: Chunk separator + content only
            context_parts.append(f"--- Chunk {i} ({chunk.get('category', 'unknown')}) ---\n{chunk['content']}")
        
        context = "\n\n".join(context_parts)
        logger.info(f"Built context from {len(chunks)} chunks, length: {len(context)} chars")
        
        return context
