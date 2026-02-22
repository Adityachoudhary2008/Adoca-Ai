import time
from typing import Dict, List
from backend.knowledge_base import initialize_knowledge_base, KnowledgeBase
from backend.sarvam_client import SarvamAIClient
from backend.search_engine import VectorSearch, ContextBuilder
from backend.safeguards import IntentDetector, AntiHallucinationFilter
from backend.logger import logger, log_query, log_response, log_error

class RAGOrchestrator:
    """
    Main RAG orchestrator - coordinates the entire pipeline.
    Flow: User Input → Intent Detection → Embedding → Search → Context Build 
          → LLM Response → Validation → Output
    """
    
    def __init__(self):
        """Initialize RAG system."""
        logger.info("Initializing RAG Orchestrator...")
        
        # Initialize knowledge base
        self.kb = initialize_knowledge_base()
        
        # Initialize Sarvam AI client
        try:
            self.sarvam = SarvamAIClient()
        except ValueError as e:
            logger.error(f"Failed to initialize Sarvam client: {str(e)}")
            raise
        
        self.system_prompt = """You are Adoca AI Personal Assistant.

You are an expert on the Adoca platform.

STRICT RULES YOU MUST FOLLOW:
1. You MUST answer ONLY using the provided context.
2. You MUST NOT use any external knowledge or general facts.
3. You MUST NOT guess or assume anything.
4. If the answer is not present in the context, respond: "I don't know based on current data."
5. You MUST give structured and clear answers.
6. Maintain a professional and product-specific tone.
7. Do NOT add unrelated explanations.
8. Do NOT hallucinate or make things up.
9. Use short paragraphs and bullet points when needed.
10. Keep responses concise and focused.

Your job is to explain Adoca features, guide users, and clarify product concepts.

REMEMBER: Playing safe is better than guessing. If unsure, say "I don't know."
"""
        
        logger.info("RAG Orchestrator initialized successfully")
    
    def query(self, user_query: str, user_id: str = "anonymous") -> Dict:
        """
        Process user query through RAG pipeline.
        
        Returns:
        {
            "query": user_query,
            "intent": detected_intent,
            "response": ai_response,
            "context_chunks": num_chunks_used,
            "latency_ms": execution_time,
            "status": "success" or "error"
        }
        """
        
        start_time = time.time()
        
        try:
            # STEP 1: Detect intent
            intent = IntentDetector.detect(user_query)
            log_query(user_id, user_query, intent)
            logger.info(f"Step 1 Complete - Intent: {intent}")
            
            # STEP 2: Get embedding for query
            logger.info("Step 2 - Generating embedding for query...")
            query_embedding = self.sarvam.get_embedding(user_query)
            
            if query_embedding is None:
                logger.error("Failed to generate query embedding")
                return {
                    "query": user_query,
                    "response": "Service temporarily unavailable. Please try again.",
                    "status": "error",
                    "latency_ms": (time.time() - start_time) * 1000
                }
            
            logger.info("Step 2 Complete - Query embedding generated")
            
            # STEP 3: Get embeddings for all knowledge chunks (if not cached)
            logger.info("Step 3 - Retrieving knowledge chunks...")
            all_chunks = self.kb.get_all_chunks()
            
            # Embed chunks if not already done
            for chunk in all_chunks:
                if "embedding" not in chunk:
                    chunk_embedding = self.sarvam.get_embedding(chunk["content"])
                    if chunk_embedding:
                        chunk["embedding"] = chunk_embedding
            
            logger.info("Step 3 Complete - Knowledge chunks prepared")
            
            # STEP 4: Vector search
            logger.info("Step 4 - Performing vector search...")
            relevant_chunks = VectorSearch.search(query_embedding, all_chunks)
            
            if not relevant_chunks:
                logger.warning("No relevant chunks found")
                return {
                    "query": user_query,
                    "intent": intent,
                    "response": "I don't know based on current data. Please check the Adoca app or contact support.",
                    "context_chunks": 0,
                    "latency_ms": (time.time() - start_time) * 1000,
                    "status": "no_context"
                }
            
            logger.info(f"Step 4 Complete - Found {len(relevant_chunks)} relevant chunks")
            
            # STEP 5: Build context (STRICT - no modification)
            logger.info("Step 5 - Building context...")
            context = ContextBuilder.build_context(relevant_chunks)
            logger.info("Step 5 Complete - Context built")
            
            # STEP 6: Get LLM response
            logger.info("Step 6 - Calling Sarvam AI for response...")
            response = self.sarvam.get_response(self.system_prompt, user_query, context)
            
            if response is None:
                logger.error("Failed to get response from Sarvam AI")
                return {
                    "query": user_query,
                    "intent": intent,
                    "response": "Service temporarily unavailable. Please try again.",
                    "context_chunks": len(relevant_chunks),
                    "latency_ms": (time.time() - start_time) * 1000,
                    "status": "error"
                }
            
            logger.info("Step 6 Complete - Response generated")
            
            # STEP 7: Validate response (Anti-hallucination)
            logger.info("Step 7 - Validating response...")
            is_valid, reason = AntiHallucinationFilter.validate_response(response, context, user_query)
            
            if not is_valid:
                logger.warning(f"Response validation failed: {reason}")
                response = AntiHallucinationFilter.get_fallback_response(context, user_query)
            
            logger.info("Step 7 Complete - Response validated")
            
            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000
            
            # Log response
            log_response(user_id, response, len(relevant_chunks), latency_ms)
            
            return {
                "query": user_query,
                "intent": intent,
                "response": response,
                "context_chunks": len(relevant_chunks),
                "latency_ms": round(latency_ms, 2),
                "status": "success"
            }
        
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            log_error("RAG_PIPELINE", str(e), user_query)
            logger.exception("Unhandled exception in RAG pipeline")
            
            return {
                "query": user_query,
                "response": "An error occurred. Please try again later.",
                "latency_ms": round(latency_ms, 2),
                "status": "error"
            }
