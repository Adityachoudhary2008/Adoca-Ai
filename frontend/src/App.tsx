import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Navigation from './components/Navigation'
import ChatInterface from './pages/ChatInterface'
import Analytics from './pages/Analytics'
import KnowledgeBase from './pages/KnowledgeBase'
import Admin from './pages/Admin'
import { api } from './api/client'
import './index.css'

function App() {
  const [health, setHealth] = useState<boolean | null>(null)
  
  useEffect(() => {
    checkHealth()
    const interval = setInterval(checkHealth, 10000)
    return () => clearInterval(interval)
  }, [])

  const checkHealth = async () => {
    try {
      await api.health()
      setHealth(true)
    } catch {
      setHealth(false)
    }
  }

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <Navigation health={health} />
        <main className="pt-16">
          <Routes>
            <Route path="/" element={<ChatInterface />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/knowledge-base" element={<KnowledgeBase />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
