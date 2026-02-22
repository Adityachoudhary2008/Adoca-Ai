import numpy as np
from typing import List, Dict
import requests
from backend.config import settings
from backend.logger import logger

class SarvamAIClient:
    """Client for Sarvam AI API - embeddings and responses"""
    
    def __init__(self):
        self.api_key = settings.SARVAM_API_KEY
        self.api_base = settings.SARVAM_API_BASE
        self.embedding_model = settings.SARVAM_EMBEDDING_MODEL
        self.response_model = settings.SARVAM_RESPONSE_MODEL
        
        if not self.api_key:
            raise ValueError("SARVAM_API_KEY not configured in .env")
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector for text from Sarvam AI.
        Returns normalized vector for cosine similarity.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.embedding_model,
                "input": text
            }
            
            response = requests.post(
                f"{self.api_base}/embeddings",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code != 200:
                logger.error(f"Embedding API error: {response.status_code} - {response.text}")
                return None
            
            data = response.json()
            embedding = data.get("data", [{}])[0].get("embedding", [])
            
            # Normalize for cosine similarity
            embedding = np.array(embedding)
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            
            return embedding.tolist()
        
        except Exception as e:
            logger.error(f"Failed to get embedding: {str(e)}")
            return None
    
    def get_response(self, system_prompt: str, user_message: str, context: str) -> str:
        """
        Get response from Sarvam AI LLM.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Build full prompt with context
            full_prompt = f"""{system_prompt}

Context:
{context}

User Query: {user_message}

Response:"""
            
            payload = {
                "model": self.response_model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuery: {user_message}"
                    }
                ],
                "max_tokens": settings.MAX_RESPONSE_LENGTH,
                "temperature": 0.3  # Lower temp for deterministic responses
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"Response API error: {response.status_code} - {response.text}")
                return None
            
            data = response.json()
            message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            return message.strip()
        
        except Exception as e:
            logger.error(f"Failed to get response: {str(e)}")
            return None
