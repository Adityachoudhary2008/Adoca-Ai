"""
Simple client for testing the Adoca AI Assistant API.
Run the server first: python -m backend.main
"""

import requests
import json
import time

class AdocaAIClient:
    """Client for Adoca AI Assistant API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def query(self, query: str, user_id: str = "test_user") -> dict:
        """Send query to assistant."""
        url = f"{self.base_url}/query"
        payload = {
            "query": query,
            "user_id": user_id
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
    
    def health(self) -> dict:
        """Check API health."""
        url = f"{self.base_url}/health"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
    
    def kb_stats(self) -> dict:
        """Get knowledge base statistics."""
        url = f"{self.base_url}/knowledge-base/stats"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

def interactive_mode():
    """Interactive query mode."""
    client = AdocaAIClient()
    
    print("\n" + "="*70)
    print("Adoca AI Assistant - Interactive Mode")
    print("="*70)
    print("Type 'exit' to quit, 'health' to check status, 'stats' for KB stats\n")
    
    while True:
        try:
            query = input("You: ").strip()
            
            if query.lower() == 'exit':
                print("Goodbye!\n")
                break
            elif query.lower() == 'health':
                result = client.health()
                print(f"Status: {json.dumps(result, indent=2)}\n")
                continue
            elif query.lower() == 'stats':
                result = client.kb_stats()
                print(f"KB Stats: {json.dumps(result, indent=2)}\n")
                continue
            elif not query:
                continue
            
            # Query the assistant
            start = time.time()
            result = client.query(query)
            elapsed = time.time() - start
            
            if result:
                print(f"\nAdoca AI ({result.get('latency_ms')}ms):")
                print(f"Intent: {result.get('intent')}")
                print(f"Chunks: {result.get('context_chunks')}")
                print(f"Status: {result.get('status')}")
                print(f"\nResponse:\n{result.get('response')}\n")
            else:
                print("Failed to get response.\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!\n")
            break
        except Exception as e:
            print(f"Error: {e}\n")

def demo_queries():
    """Run demo queries."""
    client = AdocaAIClient()
    
    # Check health
    print("\n" + "="*70)
    print("Checking API Health...")
    health = client.health()
    if health:
        print(f"✓ API is {health.get('status')}")
    
    # Get KB stats
    print("\n" + "="*70)
    print("Knowledge Base Statistics")
    stats = client.kb_stats()
    if stats:
        print(f"Total chunks: {stats.get('total_chunks')}")
        print("By category:", stats.get('by_category'))
    
    # Demo queries
    demo_queries_list = [
        "What is Adoca?",
        "How does RFQ work?",
        "What are Fire Coins?",
        "How do I prevent fraud?",
        "What is masked calling?",
    ]
    
    print("\n" + "="*70)
    print("Running Demo Queries")
    print("="*70)
    
    for i, query in enumerate(demo_queries_list, 1):
        print(f"\n[Query {i}] {query}")
        result = client.query(query)
        
        if result:
            print(f"Intent: {result.get('intent')}")
            print(f"Chunks: {result.get('context_chunks')}")
            print(f"Latency: {result.get('latency_ms')}ms")
            print(f"Response: {result.get('response')[:200]}...")
        
        time.sleep(0.5)  # Avoid rate limiting

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_queries()
    else:
        interactive_mode()
