import os
import requests

API_KEY = os.environ.get("SARVAM_API_KEY")
BASE = os.environ.get("SARVAM_API_BASE", "https://api.sarvam.ai")

if not API_KEY:
    print("SARVAM_API_KEY not set in environment")
    raise SystemExit(1)

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def try_url(url, payload):
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        print(url, r.status_code)
        print(r.text[:1000])
    except Exception as e:
        print(url, "ERROR", e)

if __name__ == '__main__':
    emb_payload = {"model": "sarvam-embeddings-1", "input": "hello world"}
    chat_payload = {"model": "sarvam-chat-1", "messages": [{"role": "user", "content": "hello"}]}

    print("Testing embeddings endpoints:")
    try_url(f"{BASE}/v1/embeddings", emb_payload)
    try_url(f"{BASE}/embeddings", emb_payload)

    print("\nTesting chat endpoints:")
    try_url(f"{BASE}/v1/chat/completions", chat_payload)
    try_url(f"{BASE}/chat/completions", chat_payload)
