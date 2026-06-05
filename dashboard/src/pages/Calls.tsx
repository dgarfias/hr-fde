import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Phone, ChevronRight, AlertTriangle, Search } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, Badge, Skeleton } from '../components/ui'
import api from '../services/api'
import type { CallRecord } from '../types'

export default function Calls() {
  const [calls, setCalls] = useState<CallRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')

  useEffect(() => {
    async function load() {
      try {
        setLoading(true)
        const res = await api.get('/api/dashboard/calls')
        setCalls(res.data)
      } catch (err: any) {
        if (err?.response?.status === 401) {
          localStorage.removeItem('dashboard_auth')
          window.location.reload()
        }
        setError(err?.response?.data?.detail || err.message || 'Failed to load calls')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const filtered = calls.filter((c) => {
    const q = search.toLowerCase()
    return (
      c.run_id.toLowerCase().includes(q) ||
      c.mc_number?.toLowerCase().includes(q) ||
      c.carrier_name?.toLowerCase().includes(q) ||
      c.load_id?.toLowerCase().includes(q)
    )
  })

  if (loading) {
    return (
      <div className="space-y-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-20" />
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <Card className="border-destructive">
        <CardHeader>
          <CardTitle className="text-destructive flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            Error loading calls
          </CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-muted-foreground">{error}</CardContent>
      </Card>
    )
  }

  const getOutcomeBadge = (outcome?: string | null) => {
    if (!outcome) return <Badge variant="outline">No data</Badge>
    const variants: Record<string, 'default' | 'secondary' | 'destructive' | 'outline'> = {
      agreed: 'default',
      declined: 'destructive',
      not_eligible: 'outline',
      no_match: 'secondary',
      dropped: 'destructive',
    }
    return <Badge variant={variants[outcome] || 'outline'}>{outcome.replace(/_/g, ' ')}</Badge>
  }

  const getSentimentBadge = (sentiment?: string | null) => {
    if (!sentiment) return <Badge variant="outline">—</Badge>
    const variants: Record<string, 'default' | 'secondary' | 'destructive' | 'outline'> = {
      positive: 'default',
      neutral: 'secondary',
      negative: 'destructive',
    }
    return <Badge variant={variants[sentiment] || 'outline'}>{sentiment}</Badge>
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Calls</h1>
          <p className="text-sm text-muted-foreground mt-1">All recorded inbound carrier sales calls</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Phone className="h-4 w-4" />
          {calls.length} total
        </div>
      </div>

      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search by MC, carrier, load..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex h-10 w-full rounded-lg border border-input bg-background pl-9 pr-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
        />
      </div>

      {filtered.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center text-muted-foreground">
            {search ? 'No calls match your search.' : 'No calls recorded yet. Make a test call to generate data.'}
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-2">
          {filtered.map((call) => (
            <Link key={call.id} to={`/calls/${call.run_id}`} className="block">
              <Card className="hover:bg-accent/40 transition-colors cursor-pointer group">
                <CardContent className="!p-4">
                  <div className="flex items-center gap-4">
                    <div className="flex-shrink-0">
                      <div className="h-10 w-10 rounded-xl bg-primary/10 flex items-center justify-center">
                        <Phone className="h-4 w-4 text-primary" />
                      </div>
                    </div>
                    <div className="flex-1 min-w-0 grid grid-cols-1 sm:grid-cols-5 gap-2 items-center">
                      <div className="sm:col-span-1">
                        <p className="text-sm font-semibold truncate">{call.run_id.slice(0, 12)}</p>
                        <p className="text-xs text-muted-foreground">
                          {call.duration_seconds
                            ? `${Math.floor(call.duration_seconds / 60)}m ${call.duration_seconds % 60}s`
                            : '—'}
                        </p>
                      </div>
                      <div className="sm:col-span-1">
                        <p className="text-sm font-medium">{call.mc_number || '—'}</p>
                        <p className="text-xs text-muted-foreground truncate">
                          {call.carrier_name || 'Unknown carrier'}
                        </p>
                      </div>
                      <div className="sm:col-span-1">
                        <p className="text-sm font-medium">{call.load_id || '—'}</p>
                        <p className="text-xs text-muted-foreground truncate">
                          {call.origin && call.destination
                            ? `${call.origin} → ${call.destination}`
                            : 'No lane data'}
                        </p>
                      </div>
                      <div className="sm:col-span-1 flex items-center gap-2 flex-wrap">
                        {getOutcomeBadge(call.outcome)}
                        {getSentimentBadge(call.sentiment)}
                      </div>
                      <div className="sm:col-span-1 flex items-center justify-end gap-2">
                        <span className="text-xs text-muted-foreground">
                          {call.started_at ? new Date(call.started_at).toLocaleDateString() : '—'}
                        </span>
                        <ChevronRight className="h-4 w-4 text-muted-foreground group-hover:text-foreground transition-colors" />
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
