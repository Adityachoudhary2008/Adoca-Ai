# Quick Start Guide for Adoca AI Assistant

## 🚀 5-Minute Setup

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Environment Variables
```bash
# Copy example file
copy .env.example .env

# Edit .env and add:
SARVAM_API_KEY=sk_your_actual_key_here
```

⚠️ **IMPORTANT**: Replace `sk_your_actual_key_here` with your actual Sarvam AI API key. Never commit `.env` to git.

### Step 3: Run the Server
```bash
python -m backend.main
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Test It
Open another terminal:

```bash
# Interactive mode
python client.py

# Demo mode
python client.py demo
```

## 📡 Quick API Test

Using curl:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RFQ?", "user_id": "test"}'
```

Expected response:
```json
{
  "query": "What is RFQ?",
  "response": "The RFQ (Request for Quote) Engine...",
  "intent": "info",
  "context_chunks": 3,
  "latency_ms": 245.32,
  "status": "success",
  "timestamp": "2026-02-22T10:30:00"
}
```

## 🧪 Test Cases

### Test 1: Knowledge Retrieval
```bash
python client.py
> What is Adoca?
```
Expected: Detailed Adoca overview

### Test 2: Anti-Hallucination
```bash
python client.py
> What is the stock price of Adoca?
```
Expected: "I don't know based on current data."

### Test 3: Intent Detection
```bash
python client.py
> I need a plumber
```
Expected: Intent = "service_search"

## 📊 Monitoring

Check logs:
```bash
# View today's logs
type logs\adoca_ai_20260222.log

# Or follow real-time
Get-Content logs\adoca_ai_20260222.log -Tail 10 -Wait
```

## 🔧 Configuration

Edit `.env` to adjust:
- `MAX_RESPONSE_LENGTH`: Max response tokens
- `MIN_CONTEXT_CHUNKS`: Minimum context chunks (default: 2)
- `MAX_CONTEXT_CHUNKS`: Maximum context chunks (default: 5)
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR

## 🐳 Using Docker (Optional)

```bash
# Build image
docker build -t adoca-ai .

# Run container
docker run -p 8000:8000 \
  -e SARVAM_API_KEY=sk_your_key_here \
  adoca-ai

# Or use docker-compose
docker-compose up
```

## 📚 Adding More Knowledge

Edit `backend/knowledge_base.py` and add chunks:
```python
{
    "id": "my_topic",
    "title": "My Topic",
    "category": "business",
    "content": "Explanation..."
}
```

Then restart the server.

## ❌ Troubleshooting

**"Connection refused"**
- Ensure server is running: `python -m backend.main`

**"SARVAM_API_KEY not configured"**
- Check `.env` file exists
- Verify key is set correctly

**"No relevant chunks found"**
- Add more knowledge base content
- Try rephrasing query

**"500 Error"**
- Check logs in `logs/` folder
- Verify Sarvam AI API is accessible

## 📞 Support

1. Check logs: `logs/adoca_ai_*.log`
2. Review README.md for detailed documentation
3. Test with demo queries: `python client.py demo`

---

**Remember**: This system is built on strict rules, not just code. The quality comes from discipline in adhering to RAG principles. 🎯
