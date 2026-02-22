import { useState, useEffect } from 'react'
import { BookOpen, Search, Filter, Tag } from 'lucide-react'
import { api } from '../api/client'

interface KBChunk {
  id: string
  title: string
  category: string
  length_chars: number
}

export default function KnowledgeBase() {
  const [chunks, setChunks] = useState<KBChunk[]>([])
  const [filtered, setFiltered] = useState<KBChunk[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)

  useEffect(() => {
    loadKB()
  }, [])

  useEffect(() => {
    filterChunks()
  }, [search, selectedCategory, chunks])

  const loadKB = async () => {
    try {
      const response = await api.kbList()
      setChunks(response.data.chunks)
    } catch (error) {
      console.error('Failed to load KB:', error)
    } finally {
      setLoading(false)
    }
  }

  const filterChunks = () => {
    let result = chunks

    if (selectedCategory) {
      result = result.filter(c => c.category === selectedCategory)
    }

    if (search) {
      const q = search.toLowerCase()
      result = result.filter(
        c =>
          c.title.toLowerCase().includes(q) ||
          c.id.toLowerCase().includes(q)
      )
    }

    setFiltered(result)
  }

  const categories = [...new Set(chunks.map(c => c.category))]

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Knowledge Base</h1>
        <p className="text-slate-600">Browse all {chunks.length} knowledge chunks</p>
      </div>

      {/* Search and Filter */}
      <div className="bg-white rounded-lg shadow-premium p-4 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search knowledge base..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Category Filter */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedCategory(null)}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                selectedCategory === null
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              All
            </button>
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                  selectedCategory === cat
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                <span className="capitalize">{cat.replace('_', ' ')}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Chunks List */}
      {loading ? (
        <div className="text-center py-12">
          <p className="text-slate-600">Loading knowledge base...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map(chunk => (
            <div
              key={chunk.id}
              className="bg-white rounded-lg shadow-premium p-5 hover:shadow-lg transition border border-slate-100"
            >
              <div className="flex items-start justify-between mb-2">
                <h3 className="font-bold text-slate-900 flex-1">{chunk.title}</h3>
                <BookOpen className="w-4 h-4 text-blue-600 flex-shrink-0" />
              </div>

              <p className="text-xs text-slate-500 mb-3">ID: {chunk.id}</p>

              <div className="flex items-center justify-between">
                <span className="inline-flex items-center gap-1 px-2 py-1 bg-slate-100 rounded text-xs font-medium text-slate-700 capitalize">
                  <Tag className="w-3 h-3" />
                  {chunk.category.replace('_', ' ')}
                </span>
                <span className="text-xs text-slate-500">
                  {Math.round(chunk.length_chars / 5)} words
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {filtered.length === 0 && !loading && (
        <div className="text-center py-12">
          <BookOpen className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <p className="text-slate-600">No chunks found</p>
        </div>
      )}
    </div>
  )
}
