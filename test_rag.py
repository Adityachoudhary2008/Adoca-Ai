"""
Development/Testing script for the RAG system.
This script provides utilities for testing and debugging.
"""

import asyncio
import json
from backend.rag_orchestrator import RAGOrchestrator
from backend.logger import logger

class RAGTester:
    """Test utility for RAG system."""
    
    def __init__(self):
        self.rag = RAGOrchestrator()
    
    def test_query(self, query: str, user_id: str = "test_user"):
        """Test a single query."""
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"User: {user_id}")
        print(f"{'='*60}")
        
        result = self.rag.query(query, user_id)
        
        print(f"\nIntent: {result.get('intent', 'unknown')}")
        print(f"Context Chunks Used: {result.get('context_chunks', 0)}")
        print(f"Latency: {result.get('latency_ms', 0)}ms")
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"\nResponse:\n{result.get('response', 'No response')}")
        
        return result
    
    def test_suite(self):
        """Run test cases."""
        test_cases = [
            {
                "query": "What is RFQ?",
                "expected_intent": "info",
                "description": "RFQ Explanation"
            },
            {
                "query": "How do Fire Coins work?",
                "expected_intent": "info",
                "description": "Coin System"
            },
            {
                "query": "What is Adoca?",
                "expected_intent": "info",
                "description": "Adoca Overview"
            },
            {
                "query": "How to prevent fraud?",
                "expected_intent": "info",
                "description": "Fraud System"
            },
            {
                "query": "What is the stock price of Adoca?",
                "expected_intent": "general_inquiry",
                "description": "Unknown Question (Should say 'I don't know')"
            },
            {
                "query": "I need a plumber",
                "expected_intent": "service_search",
                "description": "Service Search Intent"
            },
            {
                "query": "How to apply for subscription?",
                "expected_intent": "info",
                "description": "Subscription Info"
            },
        ]
        
        results = []
        for test in test_cases:
            logger.info(f"Running test: {test['description']}")
            result = self.test_query(test['query'])
            result['description'] = test['description']
            result['expected_intent'] = test['expected_intent']
            results.append(result)
        
        return results

def run_tests():
    """Run test suite."""
    print("\n" + "="*80)
    print("ADOCA AI ASSISTANT - TEST SUITE")
    print("="*80)
    
    tester = RAGTester()
    results = tester.test_suite()
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for i, result in enumerate(results, 1):
        status = "✓" if result['status'] == 'success' else "✗"
        print(f"{i}. {status} {result['description']}")
        print(f"   Intent: {result.get('intent')} (expected: {result.get('expected_intent')})")
        print(f"   Latency: {result.get('latency_ms')}ms")
        print()

if __name__ == "__main__":
    run_tests()
