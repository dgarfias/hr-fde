import { useState, useEffect } from 'react'
import { Routes, Route, Link, useLocation } from 'react-router-dom'
import { Moon, Sun, LogOut, LayoutDashboard, Phone, BarChart3 } from 'lucide-react'
import { logout } from './services/api'
import Dashboard from './pages/Dashboard'
import Calls from './pages/Calls'
import CallDetail from './pages/CallDetail'

function ThemeToggle() {
  const [dark, setDark] = useState(() => {
    if (typeof window !== 'undefined') {
      return document.documentElement.classList.contains('dark')
    }
    return false
  })

  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [dark])

  return (
    <button
      onClick={() => setDark(!dark)}
      className="inline-flex items-center justify-center rounded-lg w-9 h-9 text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-colors"
    >
      {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
    </button>
  )
}

const navItems = [
  { to: '/', label: 'Overview', icon: LayoutDashboard },
  { to: '/calls', label: 'Calls', icon: Phone },
]

function Sidebar() {
  const location = useLocation()

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r bg-card hidden lg:flex flex-col">
      <div className="flex h-16 items-center gap-3 px-6 border-b">
        <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
          <BarChart3 className="h-4 w-4 text-primary-foreground" />
        </div>
        <span className="font-semibold text-lg tracking-tight">Acme Logistics</span>
      </div>

      <nav className="flex-1 px-4 py-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon
          const active = location.pathname === item.to || (item.to !== '/' && location.pathname.startsWith(item.to))
          return (
            <Link
              key={item.to}
              to={item.to}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                active
                  ? 'bg-primary/10 text-primary'
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
              }`}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          )
        })}
      </nav>

      <div className="border-t p-4">
        <div className="flex items-center justify-between">
          <ThemeToggle />
          <button
            onClick={async () => {
              try { await logout() } catch (e) {}
              window.location.reload()
            }}
            className="inline-flex items-center justify-center rounded-lg w-9 h-9 text-muted-foreground hover:bg-accent hover:text-destructive transition-colors"
            title="Logout"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </div>
    </aside>
  )
}

function MobileHeader() {
  const location = useLocation()
  const current = navItems.find(n => location.pathname === n.to || (n.to !== '/' && location.pathname.startsWith(n.to)))

  return (
    <header className="lg:hidden sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur">
      <div className="flex h-14 items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <div className="h-7 w-7 rounded-lg bg-primary flex items-center justify-center">
            <BarChart3 className="h-3.5 w-3.5 text-primary-foreground" />
          </div>
          <span className="font-semibold">Acme Logistics</span>
        </div>
        <span className="text-sm text-muted-foreground">{current?.label || 'Dashboard'}</span>
      </div>
    </header>
  )
}

function App() {
  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <MobileHeader />
      <main className="lg:ml-64 min-h-screen">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/calls" element={<Calls />} />
            <Route path="/calls/:callId" element={<CallDetail />} />
          </Routes>
        </div>
      </main>
    </div>
  )
}

export default App
