import axios from 'axios'

// In production (Render), use current domain. In dev, use localhost:8000
const getApiBase = () => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // Production fallback: use current domain
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
    return `https://${window.location.hostname}`
  }
  
  // Development: use localhost
  return 'http://localhost:8000'
}

const API_BASE = getApiBase()

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface QueryRequest {
  query: string
  user_id?: string
}

export interface QueryResponse {
  query: string
  response: string
  intent: string
  context_chunks: number
  latency_ms: number
  status: 'success' | 'error' | 'no_context'
  timestamp: string
}

export interface HealthResponse {
  status: string
  version: string
  environment: string
  timestamp: string
}

export interface KBStats {
  total_chunks: number
  by_category: Record<string, number>
  timestamp: string
}

export const api = {
  // Query
  query(data: QueryRequest) {
    return client.post<QueryResponse>('/query', data)
  },

  // Health
  health() {
    return client.get<HealthResponse>('/health')
  },

  // KB
  kbStats() {
    return client.get<KBStats>('/knowledge-base/stats')
  },

  kbList() {
    return client.get('/knowledge-base/list')
  },
}

export default client
