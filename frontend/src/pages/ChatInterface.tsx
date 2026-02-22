import { useState, useRef, useEffect } from 'react'
import { Send, Loader, Zap, Copy, Download } from 'lucide-react'
import { api, QueryResponse } from '../api/client'

interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  metadata?: any
  timestamp: Date
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [userId, setUserId] = useState(() => `user_${Date.now()}`)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    // Add user message
    const userMessage: Message = {
      id: `msg_${Date.now()}`,
      type: 'user',
      content: input,
      timestamp: new Date(),
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await api.query({
        query: input,
        user_id: userId,
      })

      const assistantMessage: Message = {
        id: `msg_${Date.now()}_resp`,
        type: 'assistant',
        content: response.data.response,
        metadata: {
          intent: response.data.intent,
          chunks: response.data.context_chunks,
          latency: response.data.latency_ms,
          status: response.data.status,
        },
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: `msg_${Date.now()}_err`,
        type: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-64px)] flex flex-col bg-white rounded-lg m-4 shadow-premium">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="p-4 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full mb-4">
              <Zap className="w-12 h-12 text-blue-600" />
            </div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">Welcome to Adoca AI</h2>
            <p className="text-slate-600 max-w-md">
              Ask me anything about Adoca. I'll provide accurate, knowledge-backed answers from our comprehensive database.
            </p>
          </div>
        )}

        {messages.map(msg => (
          <div
            key={msg.id}
            className={`animate-slide flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xl px-4 py-3 rounded-lg ${
                msg.type === 'user'
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-br-none'
                  : 'bg-slate-100 text-slate-900 rounded-bl-none'
              }`}
            >
              <p className="text-sm mb-2">{msg.content}</p>

              {msg.metadata && (
                <div className="flex items-center gap-2 text-xs opacity-75 mt-2">
                  <span>Intent: {msg.metadata.intent}</span>
                  <span>•</span>
                  <span>Chunks: {msg.metadata.chunks}</span>
                  <span>•</span>
                  <span>{msg.metadata.latency.toFixed(0)}ms</span>
                </div>
              )}

              {msg.type === 'assistant' && (
                <button
                  onClick={() => copyToClipboard(msg.content)}
                  className="mt-2 text-xs opacity-60 hover:opacity-100 flex items-center gap-1"
                >
                  <Copy className="w-3 h-3" />
                  Copy
                </button>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-100 text-slate-900 px-4 py-3 rounded-lg rounded-bl-none">
              <div className="flex items-center gap-2">
                <Loader className="w-4 h-4 animate-spin" />
                <span className="text-sm">Thinking...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-slate-200 p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask about Adoca features, RFQ, Fire Coins, or anything else..."
            disabled={loading}
            className="flex-1 px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg disabled:opacity-50 transition"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>

        {/* Help text */}
        <p className="text-xs text-slate-500 mt-2">
          💡 Try: "What is RFQ?", "How do Fire Coins work?", or "Explain the hybrid model"
        </p>
      </div>
    </div>
  )
}
