import { Settings, Key, Database, Bell, Shield, Download } from 'lucide-react'
import { useState } from 'react'

export default function Admin() {
  const [config, setConfig] = useState({
    maxResponseLength: 1000,
    minChunks: 2,
    maxChunks: 5,
    rateLimitRequests: 100,
    rateLimitWindow: 3600,
  })

  const [saved, setSaved] = useState(false)

  const handleSave = () => {
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-slate-900 mb-8">Admin Panel</h1>

      <div className="space-y-6">
        {/* Configuration */}
        <div className="bg-white rounded-lg shadow-premium p-6">
          <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
            <Settings className="w-5 h-5 text-blue-600" />
            System Configuration
          </h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Max Response Length (tokens)
              </label>
              <input
                type="number"
                value={config.maxResponseLength}
                onChange={e => setConfig({ ...config, maxResponseLength: parseInt(e.target.value) })}
                className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Min Context Chunks
                </label>
                <input
                  type="number"
                  value={config.minChunks}
                  onChange={e => setConfig({ ...config, minChunks: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Max Context Chunks
                </label>
                <input
                  type="number"
                  value={config.maxChunks}
                  onChange={e => setConfig({ ...config, maxChunks: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Rate Limit (requests)
                </label>
                <input
                  type="number"
                  value={config.rateLimitRequests}
                  onChange={e => setConfig({ ...config, rateLimitRequests: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Window (seconds)
                </label>
                <input
                  type="number"
                  value={config.rateLimitWindow}
                  onChange={e => setConfig({ ...config, rateLimitWindow: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <button
              onClick={handleSave}
              className="w-full px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg transition font-medium"
            >
              {saved ? '✓ Configuration Saved' : 'Save Configuration'}
            </button>
          </div>
        </div>

        {/* Security */}
        <div className="bg-white rounded-lg shadow-premium p-6">
          <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5 text-green-600" />
            Security & API Keys
          </h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Sarvam AI API Key
              </label>
              <div className="flex gap-2">
                <input
                  type="password"
                  placeholder="••••••••••••••••"
                  className="flex-1 px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled
                />
                <button className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition">
                  <Key className="w-4 h-4" />
                </button>
              </div>
              <p className="text-xs text-slate-500 mt-1">Configured in environment variables</p>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="bg-white rounded-lg shadow-premium p-6">
          <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
            <Database className="w-5 h-5 text-purple-600" />
            System Actions
          </h2>

          <div className="space-y-2">
            <button className="w-full px-4 py-2 text-left text-slate-700 hover:bg-slate-50 rounded-lg transition flex items-center justify-between">
              <span>Rebuild Knowledge Base Index</span>
              <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">Dev</span>
            </button>
            <button className="w-full px-4 py-2 text-left text-slate-700 hover:bg-slate-50 rounded-lg transition flex items-center justify-between">
              <span>Export Query Logs</span>
              <Download className="w-4 h-4" />
            </button>
            <button className="w-full px-4 py-2 text-left text-slate-700 hover:bg-slate-50 rounded-lg transition flex items-center justify-between">
              <span>Clear Cache</span>
              <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded">Caution</span>
            </button>
          </div>
        </div>

        {/* Notifications */}
        <div className="bg-white rounded-lg shadow-premium p-6">
          <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
            <Bell className="w-5 h-5 text-orange-600" />
            Notifications & Alerts
          </h2>

          <div className="space-y-3">
            <label className="flex items-center gap-3">
              <input type="checkbox" defaultChecked className="w-4 h-4" />
              <span className="text-sm text-slate-700">Error rate exceeds 1%</span>
            </label>
            <label className="flex items-center gap-3">
              <input type="checkbox" defaultChecked className="w-4 h-4" />
              <span className="text-sm text-slate-700">Average latency > 500ms</span>
            </label>
            <label className="flex items-center gap-3">
              <input type="checkbox" className="w-4 h-4" />
              <span className="text-sm text-slate-700">Rate limit exceeded</span>
            </label>
          </div>
        </div>
      </div>
    </div>
  )
}
