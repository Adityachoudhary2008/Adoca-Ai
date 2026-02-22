import { Link } from 'react-router-dom'
import { MessageCircle, BarChart3, BookOpen, Settings, Zap } from 'lucide-react'

interface NavigationProps {
  health?: boolean | null
}

export default function Navigation({ health }: NavigationProps) {
  return (
    <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-lg border-b border-slate-200 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <div className="p-2 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg group-hover:shadow-lg transition">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg gradient-text">Adoca AI</h1>
            <p className="text-xs text-slate-500">Personal Assistant</p>
          </div>
        </Link>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-1">
          <NavLink icon={MessageCircle} label="Chat" path="/" />
          <NavLink icon={BarChart3} label="Analytics" path="/analytics" />
          <NavLink icon={BookOpen} label="KB" path="/knowledge-base" />
          <NavLink icon={Settings} label="Admin" path="/admin" />
        </div>

        {/* Status */}
        <div className="flex items-center gap-3">
          {health !== null && (
            <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${
              health
                ? 'bg-green-100 text-green-700'
                : 'bg-red-100 text-red-700'
            }`}>
              <div className={`w-2 h-2 rounded-full ${health ? 'bg-green-500' : 'bg-red-500'}`} />
              {health ? 'Online' : 'Offline'}
            </div>
          )}
          <button className="p-2 hover:bg-slate-100 rounded-lg transition">
            <Settings className="w-5 h-5 text-slate-600" />
          </button>
        </div>
      </div>
    </nav>
  )
}

function NavLink({ icon: Icon, label, path }: any) {
  return (
    <Link
      to={path}
      className="flex items-center gap-2 px-3 py-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition"
    >
      <Icon className="w-4 h-4" />
      <span className="text-sm font-medium">{label}</span>
    </Link>
  )
}
