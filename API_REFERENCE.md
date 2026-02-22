# Adoca AI Assistant - API Reference

## Base URL

```
http://localhost:8000      (Development)
https://api.adoca-ai.com   (Production - configure in deployment)
```

## Authentication

API key authentication via environment variable (backend only).

For API calls, no authentication header needed (secure by network).

## Endpoints

### 1. Query Endpoint ⭐ (Main)

**POST** `/query`

Send a user query and receive AI-generated response with metadata.

#### Request

```json
{
  "query": "What is RFQ?",
  "user_id": "user_12345"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | User's question or statement |
| user_id | string | No | User identifier (for logging) |

#### Response

```json
{
  "query": "What is RFQ?",
  "response": "The RFQ (Request for Quote) Engine is Adoca's unique feature for custom products and services. Instead of browsing pre-listed items, users can submit RFQs for products that don't have standard listings. For example: custom tailoring, wedding planning services, home renovation, or bulk orders. Merchants then respond with quotes, timelines, and proposals. This feature bridges the gap between e-commerce and local services by enabling price negotiation and customization.",
  "intent": "info",
  "context_chunks": 2,
  "latency_ms": 245.32,
  "status": "success",
  "timestamp": "2026-02-22T10:30:00"
}
```

| Field | Type | Description |
|-------|------|-------------|
| query | string | Echo of user's query |
| response | string | AI-generated answer (context-backed) |
| intent | string | Detected intent (info, service_search, support, pricing, etc) |
| context_chunks | integer | Number of KB chunks used (2-5) |
| latency_ms | float | Response time in milliseconds |
| status | string | "success", "error", "no_context" |
| timestamp | string | ISO 8601 timestamp of query |

#### Example Requests

**Knowledge Query**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How does masked calling work?"}'
```

**With User ID**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Smart POS?", "user_id": "merchant_456"}'
```

#### Status Codes

| Code | Meaning |
|------|---------|
| 200 | Successful query |
| 400 | Bad request (empty query, invalid format) |
| 500 | Server error |

---

### 2. Health Check

**GET** `/health`

Check if API is running and healthy.

#### Response

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2026-02-22T10:30:00"
}
```

#### Example

```bash
curl http://localhost:8000/health
```

#### Response Codes

| Code | Meaning |
|------|---------|
| 200 | Service is healthy |
| 503 | Service unavailable |

---

### 3. Knowledge Base Statistics

**GET** `/knowledge-base/stats`

Get statistics about the knowledge base.

#### Response

```json
{
  "total_chunks": 20,
  "by_category": {
    "business": 3,
    "user_app": 4,
    "business_app": 2,
    "conversational_commerce": 3,
    "financial_system": 2,
    "risk_fraud": 4,
    "workflow": 5
  },
  "timestamp": "2026-02-22T10:30:00"
}
```

#### Example

```bash
curl http://localhost:8000/knowledge-base/stats
```

---

### 4. List Knowledge Chunks

**GET** `/knowledge-base/list`

List all knowledge chunks (metadata only, not full content).

#### Response

```json
{
  "count": 20,
  "chunks": [
    {
      "id": "adoca_overview",
      "title": "Adoca Overview",
      "category": "business",
      "length_chars": 1234
    },
    {
      "id": "rfq_engine",
      "title": "RFQ Engine - Request for Quote",
      "category": "user_app",
      "length_chars": 956
    },
    ...
  ]
}
```

#### Example

```bash
curl http://localhost:8000/knowledge-base/list
```

---

### 5. Root Endpoint

**GET** `/`

Welcome page with API information.

#### Response

```json
{
  "app": "Adoca AI Personal Assistant",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "query": "/query (POST)",
    "kb_stats": "/knowledge-base/stats",
    "kb_list": "/knowledge-base/list"
  }
}
```

---

## Intent Types

The system classifies queries into intents:

| Intent | Example Query | Use Case |
|--------|---------------|----------|
| `info` | "What is RFQ?" | General information request |
| `service_search` | "I need a plumber" | Looking for a service/product |
| `support` | "I have a login issue" | Getting help with problems |
| `pricing` | "What are the plans?" | Pricing/subscription queries |
| `rfq` | "Can I request a custom quote?" | RFQ-specific questions |
| `fraud` | "Is Adoca safe?" | Security/fraud related |
| `rewards` | "How do I earn coins?" | Rewards/incentives |
| `general_inquiry` | Any other query | Fallback for unknown intents |

---

## Response Scenarios

### ✅ Successful Response (Status: success)

Query found in knowledge base and answered:

```json
{
  "query": "What are Fire Coins?",
  "response": "Fire Coin is the digital wallet and rewards currency within Adoca...",
  "intent": "info",
  "context_chunks": 2,
  "latency_ms": 234.56,
  "status": "success"
}
```

### ⚠️ No Context Found (Status: no_context)

Query doesn't match any knowledge base entries:

```json
{
  "query": "What is the weather today?",
  "response": "I don't know based on current data. Please check the Adoca app or contact support.",
  "intent": "general_inquiry",
  "context_chunks": 0,
  "latency_ms": 145.23,
  "status": "no_context"
}
```

### ❌ Error Response (Status: error)

Server error occurred:

```json
{
  "query": "What is RFQ?",
  "response": "Service temporarily unavailable. Please try again.",
  "latency_ms": 5000,
  "status": "error"
}
```

---

## Error Handling

### 400 Bad Request

```json
{
  "error": "Query cannot be empty",
  "status_code": 400,
  "timestamp": "2026-02-22T10:30:00"
}
```

**Causes:**
- Empty query string
- Missing required fields
- Invalid JSON format

### 500 Internal Server Error

```json
{
  "error": "An error occurred processing your query",
  "status_code": 500,
  "timestamp": "2026-02-22T10:30:00"
}
```

**Causes:**
- Sarvam AI API unavailable
- Database error
- Unexpected system error

---

## Rate Limiting

Rate limiting is configured in `.env`:

```
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

**Default**: 100 requests per hour per IP

Exceeding limit returns **429 Too Many Requests**

---

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Average Latency | 200-400 ms |
| P95 Latency | <1000 ms |
| Knowledge Retrieval | 1-5 ms |
| Embedding Generation | 100-200 ms |
| Context Building | <1 ms |
| LLM Response | 50-100 ms |
| Validation | <10 ms |

---

## Code Examples

### Python

```python
import requests

BASE_URL = "http://localhost:8000"

def query_adoca_ai(question):
    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "query": question,
            "user_id": "python_client"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Answer: {data['response']}")
        print(f"Intent: {data['intent']}")
        print(f"Latency: {data['latency_ms']}ms")
    else:
        print(f"Error: {response.status_code}")

# Usage
query_adoca_ai("What is RFQ?")
```

### JavaScript/Node.js

```javascript
const BASE_URL = "http://localhost:8000";

async function queryAdocaAI(question) {
  try {
    const response = await fetch(`${BASE_URL}/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        query: question,
        user_id: "js_client"
      })
    });
    
    const data = await response.json();
    console.log("Answer:", data.response);
    console.log("Intent:", data.intent);
    console.log("Latency:", data.latency_ms, "ms");
  } catch (error) {
    console.error("Error:", error);
  }
}

// Usage
queryAdocaAI("What is RFQ?");
```

### cURL

```bash
# Simple query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Fire Coin?"}'

# With user ID
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Fire Coin?", "user_id": "user_123"}'

# Save response to file
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain RFQ"}' \
  > response.json
```

---

## Integration Examples

### React Frontend

```jsx
import React, { useState } from 'react';

function AdocaAIWidget() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleQuery = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleQuery}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask me anything about Adoca..."
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Ask'}
        </button>
      </form>
      {response && <p>{response}</p>}
    </div>
  );
}

export default AdocaAIWidget;
```

### Vue Template

```vue
<template>
  <div class="adoca-ai-widget">
    <form @submit.prevent="handleQuery">
      <input
        v-model="query"
        placeholder="Ask me anything..."
      />
      <button :disabled="loading">
        {{ loading ? 'Loading...' : 'Ask' }}
      </button>
    </form>
    <p v-if="response">{{ response }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: '',
      response: '',
      loading: false
    };
  },
  methods: {
    async handleQuery() {
      this.loading = true;
      try {
        const res = await fetch('http://localhost:8000/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: this.query })
        });
        const data = await res.json();
        this.response = data.response;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
```

---

## Webhooks (Future)

Planned for v2.0:

```
POST /webhooks/query-result
POST /webhooks/intent-detected
POST /webhooks/error-occurred
```

---

## API Versioning

Current version: **1.0.0**

Backward compatibility guaranteed within 1.x.

---

## SLA & Support

- **Uptime**: 99.9% (production)
- **Response Time**: <1000ms (P95)
- **Error Rate**: <0.1%

---

## Documentation & Support

- API Docs: `/docs` (Swagger UI)
- ReDoc: `/redoc` (Alternative docs)
- Source: `backend/main.py`
- Logs: `logs/adoca_ai_*.log`

---

**API Version**: 1.0.0  
**Last Updated**: 2026-02-22  
**Status**: ✅ Production Ready
