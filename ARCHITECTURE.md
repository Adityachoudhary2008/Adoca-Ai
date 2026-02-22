# Adoca AI Assistant - Project Structure & Implementation Summary

## 📁 Project Structure

```
d:\my projects\Adoca AI\
├── backend/                          # Core application code
│   ├── __init__.py                  # Module initialization
│   ├── config.py                    # Configuration management (env variables)
│   ├── logger.py                    # Logging system (file + console)
│   ├── knowledge_base.py            # KB management, chunking, initialization
│   ├── sarvam_client.py             # Sarvam AI API client (embeddings + LLM)
│   ├── search_engine.py             # Vector search + context builder
│   ├── safeguards.py                # Intent detection + anti-hallucination
│   ├── rag_orchestrator.py          # Main RAG pipeline coordinator
│   └── main.py                      # FastAPI server & endpoints
├── knowledge_base/                  # Knowledge base index
│   └── index.json                  # Structured KB chunks
├── data/                            # Runtime data
│   ├── adoca.db                    # SQLite DB (future use)
│   └── vectors.db                  # Vector storage (future optimization)
├── logs/                            # Application logs
│   └── adoca_ai_YYYYMMDD.log       # Daily log files
├── .env.example                     # Environment template
├── .env                             # Local environment (git-ignored)
├── .gitignore                       # Git ignore patterns
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker containerization
├── docker-compose.yml               # Docker compose setup
├── README.md                        # Full documentation
├── QUICK_START.md                   # Quick start guide
├── ARCHITECTURE.md                  # This file
├── client.py                        # Python client for testing
└── test_rag.py                      # Test suite
```

## 🏗️ Architecture Overview

### Data Flow

```
┌─────────────┐
│  User Query │
└──────┬──────┘
       │
       ▼
┌────────────────────┐
│ Intent Detector    │    Classifies query intent
└──────┬─────────────┘    (service_search, info, support, etc)
       │
       ▼
┌────────────────────────┐
│ Query Embedding        │    Converts query to vector using
│ (Sarvam AI)            │    Sarvam AI embedding model
└──────┬─────────────────┘
       │
       ▼
┌────────────────────────┐
│ Vector Search          │    Finds top-3 to 5 similar chunks
│ (Cosine Similarity)    │    using cosine similarity metric
└──────┬─────────────────┘
       │
       ▼
┌────────────────────────┐
│ Context Builder        │    Concatenates chunks WITHOUT
│ (STRICT - No mods)     │    modification or summarization
└──────┬─────────────────┘
       │
       ▼
┌────────────────────────┐
│ LLM Response Gen       │    Calls Sarvam AI with:
│ (Sarvam AI)            │    - System prompt (strict rules)
└──────┬─────────────────┘    - Context
       │                      - User query
       ▼
┌────────────────────────┐
│ Anti-Hallucination     │    Validates response against
│ Validation Film        │    - Context existence
└──────┬─────────────────┘    - Pattern detection
       │                      - External knowledge checks
       ▼
┌──────────────────────┐
│ User Response        │    Structured JSON response with
│ + Metadata           │    latency, intent, chunks used
└──────────────────────┘
```

### RAG Pipeline Components

#### 1. **Knowledge Base System** (`backend/knowledge_base.py`)
- Loads structured chunks from JSON index
- Validates chunk structure (id, title, category, content)
- Enforces chunking rules (50+ words, clear topics)
- Supports dynamic chunk addition
- Persists to disk

**Chunk Format:**
```json
{
  "id": "unique_identifier",
  "title": "Human-readable title",
  "category": "business|feature|flow|fraud|revenue|workflow",
  "content": "50-500 word explanation",
  "embedding": [vector_array]  // Added during search
}
```

#### 2. **Sarvam AI Client** (`backend/sarvam_client.py`)
- Wraps Sarvam AI API for two operations:
  - **Embeddings**: Converts text to normalized vectors
  - **LLM Response**: Generates context-aware responses
- Uses Bearer token authentication
- Handles timeouts and errors gracefully
- Returns normalized embeddings for cosine similarity

#### 3. **Vector Search Engine** (`backend/search_engine.py`)
- **Cosine Similarity**: Compares normalized vectors
- **Configurable**: Min/max chunk limits (default: 2-5)
- **Ranking**: Returns sorted results by similarity score
- **Context Builder**: Concatenates chunks without modification

#### 4. **Safeguards** (`backend/safeguards.py`)
- **Intent Detection**: Classifies query type
- **Anti-Hallucination**: Multi-layer validation
  - Empty context rejection
  - Uncertainty pattern detection
  - External knowledge pattern detection
  - Fallback responses

#### 5. **RAG Orchestrator** (`backend/rag_orchestrator.py`)
- Coordinates entire pipeline
- 7-step process with logging at each stage
- Returns structured response with metadata
- Includes error handling and fallbacks

#### 6. **FastAPI Server** (`backend/main.py`)
- **Endpoints**:
  - `POST /query`: Main query endpoint
  - `GET /health`: Health check
  - `GET /knowledge-base/stats`: KB statistics
  - `GET /knowledge-base/list`: List all chunks
- CORS middleware for frontend integration
- Rate limiting (via config)
- Error handling with proper HTTP codes

## 🧠 Knowledge Base

### Included Topics (20 Chunks)

**Business Core (3)**
- Adoca Overview
- Philosophy
- Zero CAC Strategy

**User App (4)**
- Local Mode
- Enterprise Mode
- RFQ Engine
- Fire Coin Wallet

**Business App (2)**
- Smart POS
- CRM (implied in workflows)

**Conversational Commerce (3)**
- Masked Calling
- Transactional Chat
- Deal Lock

**Financial System (2)**
- Seller Coin System
- (Fire Coin included above)

**Risk & Fraud (4)**
- Fake Billing Fraud
- Bidding Fraud
- Privacy System
- Customer Fraud

**Workflows (5)**
- User Onboarding
- Merchant Onboarding
- Discovery Process
- Communication Flow
- Transaction Flow
- Rewards System

### Initialization
- Automatic initialization on first run
- Creates index.json with all chunks
- Chunks embedded on-demand during search
- Already embedded chunks are cached

## 🔐 Security & Anti-Hallucination

### Rule-Based Safeguards

1. **No Empty Context**: If no relevant chunks found, reject response
2. **Strict System Prompt**: Forces context-only answers
3. **Pattern Detection**: Identifies and blocks uncertainty signals
4. **Fallback Responses**: Safe defaults for edge cases

### System Prompt (ENFORCED)

```
You are Adoca AI Personal Assistant.

STRICT RULES:
1. Answer ONLY using provided context
2. Do NOT use external knowledge
3. Do NOT guess or assume
4. If answer not present: "I don't know based on current data"
5. Give structured and clear answers
6. Maintain professional tone
7. No unrelated explanations
8. No hallucination
```

### Validation Checks

```python
Valid Responses:
✓ Answers directly from context
✓ "I don't know..." when context missing
✓ Structured, clear explanations

Invalid Responses:
✗ External knowledge
✗ General statements without context
✗ Vague or uncertain answers
✗ Hallucinated facts
```

## 📊 Data Flow & Processing

### Query Processing Timeline

```
User Query
    ↓ [1ms]
Intent Detection → "info" / "service_search" / etc
    ↓ [50-100ms]
Get Query Embedding (Sarvam AI)
    ↓ [100-200ms]
Prepare & Embed Knowledge Chunks (cached after first use)
    ↓ [1-5ms]
Vector Search (Cosine Similarity)
    ↓ [<1ms]
Build Context (concatenate chunks)
    ↓ [50-100ms]
LLM Response Generation (Sarvam AI)
    ↓ [50-100ms]
Validate Response (Anti-hallucination)
    ↓ [<1ms]
Return Response
─────────────────────────
[200-400ms] Total latency
```

## 🚀 Deployment Options

### Option 1: Local Development

```bash
python -m backend.main
# Runs on http://localhost:8000
```

### Option 2: Docker Container

```bash
docker build -t adoca-ai .
docker run -p 8000:8000 \
  -e SARVAM_API_KEY=sk_xxx \
  adoca-ai
```

### Option 3: Docker Compose

```bash
docker-compose up
# Includes networking, volume management
```

### Option 4: Production Deployment

```bash
# With Gunicorn + Nginx
gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

## 📈 Monitoring & Operations

### Logging System

**Log Location**: `logs/adoca_ai_YYYYMMDD.log`

**Logged Events**:
- User queries (with intent)
- AI responses (with metadata)
- Errors and exceptions
- Latency metrics
- KB operations

**Log Format**:
```
2026-02-22 10:30:45,123 - adoca_ai - INFO - [rag_orchestrator.py:42] - Step 1 Complete - Intent: info
```

### Health Monitoring

```bash
GET /health
→ Returns: status, version, environment, timestamp

GET /knowledge-base/stats
→ Returns: total_chunks, by_category breakdown
```

## 🧪 Testing

### Unit Tests

```bash
python test_rag.py
```

Tests:
- RFQ Explanation
- Coin System
- Adoca Overview
- Fraud System
- Unknown Questions (anti-hallucination)
- Service Search Intent
- Subscription Info

### Integration Testing

```bash
python client.py        # Interactive mode
python client.py demo   # Demo queries
```

## ⚙️ Configuration

### Environment Variables

```bash
# API Keys
SARVAM_API_KEY=sk_xxxxxxx
SARVAM_EMBEDDING_MODEL=sarvam-embeddings-1
SARVAM_RESPONSE_MODEL=sarvam-chat-1

# App Config
APP_ENV=production
LOG_LEVEL=INFO
MAX_RESPONSE_LENGTH=1000

# Context Limits
MIN_CONTEXT_CHUNKS=2
MAX_CONTEXT_CHUNKS=5

# Paths
DATABASE_PATH=./data/adoca.db
KB_PATH=./knowledge_base
LOG_PATH=./logs
```

## 🔄 Workflow

### Adding New Knowledge

1. **Create Chunk**:
```python
chunk = {
    "id": "new_feature",
    "title": "New Feature Name",
    "category": "feature",
    "content": "Detailed explanation..."
}
```

2. **Add to KB**:
```python
from backend.knowledge_base import KnowledgeBase
kb = KnowledgeBase()
kb.add_chunk(chunk)
```

3. **Restart Server** (for embedding generation)

### Performance Optimization

1. **Caching**: Embeddings cached after first generation
2. **Chunk Limits**: Configurable 2-5 chunks for context
3. **Vector Similarity**: Fast O(n) cosine similarity
4. **Async Processing**: Ready for async/await patterns

## 🎯 Design Principles

1. **Strictness Over Flexibility**: Rules enforced, not suggested
2. **Context-First**: Every response backed by knowledge
3. **Transparency**: All decisions logged and traceable
4. **Fault-Safe**: Prefers "I don't know" over guessing
5. **Simplicity**: Each component has single responsibility

## 📝 API Contract

### Query Endpoint

**Request:**
```json
{
  "query": "What is RFQ?",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "query": "What is RFQ?",
  "response": "RFQ (Request for Quote) is...",
  "intent": "info",
  "context_chunks": 3,
  "latency_ms": 245.32,
  "status": "success",
  "timestamp": "2026-02-22T10:30:00"
}
```

## 🚨 Common Failure Modes & Recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| No context found | Query doesn't match KB | Return safe "I don't know" |
| API timeout | Sarvam AI slow | Timeout at 30s, return error |
| Empty KB | First init incomplete | Auto-initialize on startup |
| Invalid embedding | Sarvam API error | Log and fallback |
| Hallucination detected | Pattern match | Reject, use fallback |

## 🎓 Learning Resources

- [RAG Patterns](https://docs.llamaindex.ai/en/stable/guide/querying/)
- [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Vector Databases](https://www.pinecone.io/)

---

**Built with discipline. Rules are the greatest strength.** 🛡️
