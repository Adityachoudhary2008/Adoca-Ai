from typing import Dict, Tuple
from backend.logger import logger

class IntentDetector:
    """Detect user intent from query."""
    
    INTENT_KEYWORDS = {
        "service_search": ["plumber", "need", "want", "looking for", "find", "chai", "chahiye"],
        "support": ["issue", "problem", "help", "error", "login", "broken", "not working"],
        "info": ["what is", "kya hai", "explain", "how does", "tell me", "information"],
        "pricing": ["price", "cost", "plan", "subscription", "fee", "charge", "kitna"],
        "rfq": ["quote", "custom", "bargain", "negotiate", "mausam", "rate"],
        "fraud": ["fraud", "fake", "scam", "security", "safe"],
        "rewards": ["coin", "referral", "fire coin", "bonus", "earn"],
    }
    
    @staticmethod
    def detect(query: str) -> str:
        """Detect intent from user query."""
        query_lower = query.lower()
        
        for intent, keywords in IntentDetector.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    logger.info(f"Intent detected: {intent}")
                    return intent
        
        # Default
        return "general_inquiry"

class AntiHallucinationFilter:
    """Prevent hallucination - RULE: No answer if no context."""
    
    @staticmethod
    def validate_response(response: str, context: str, query: str) -> Tuple[bool, str]:
        """
        Validate response against anti-hallucination rules.
        Returns (is_valid, reason)
        """
        
        # RULE 1: If context empty, reject
        if not context or context.strip() == "":
            logger.warning(f"ANTI-HALLUCINATION: Empty context for query: {query}")
            return False, "no_context"
        
        # RULE 2: Check for "I don't know" patterns
        reject_patterns = [
            "i'm not sure",
            "i'm not aware",
            "cannot find",
            "no information",
            "not in my knowledge"
        ]
        
        response_lower = response.lower()
        for pattern in reject_patterns:
            if pattern in response_lower:
                logger.info(f"Response contains uncertainty pattern: {pattern}")
                # This is acceptable - model is being honest
                return True, "honest_rejection"
        
        # RULE 3: Check for suspicious external knowledge
        external_patterns = [
            "according to the internet",
            "in general",
            "most people",
            "typically",
            "usually",  # Risky without context
            "however",  # Might be adding external knowledge
        ]
        
        for pattern in external_patterns:
            if pattern in response_lower:
                logger.warning(f"Response contains external knowledge pattern: {pattern}")
                # Not necessarily invalid, but flag it
        
        return True, "passed_validation"
    
    @staticmethod
    def get_fallback_response(context: str, query: str) -> str:
        """Get safe fallback if response fails validation."""
        if not context:
            return "I don't know based on current data. Please check the Adoca app or contact support."
        
        return "I don't have specific information to answer that question accurately. Please check the Adoca app or contact support@adoca.com."
