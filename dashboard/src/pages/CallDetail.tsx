import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Phone, Clock, MapPin, Truck, DollarSign, MessageSquare, AlertTriangle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, Badge, Skeleton } from '../components/ui'
import api from '../services/api'
import type { CallDetail as CallDetailType } from '../types'

export default function CallDetail() {
  const { callId } = useParams<{ callId: string }>()
  const navigate = useNavigate()
  const [detail, setDetail] = useState<CallDetailType | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!callId) return

    async function load() {
      try {
        setLoading(true)
        const res = await api.get(`/api/dashboard/calls/${callId}`)
        setDetail(res.data)
      } catch (err: any) {
        if (err?.response?.status === 401) {
          localStorage.removeItem('dashboard_auth')
          window.location.reload()
        }
        setError(err?.response?.data?.detail || err.message || 'Failed to load call')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [callId])

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-48" />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <Skeleton className="h-72" />
          <Skeleton className="h-72 lg:col-span-2" />
        </div>
      </div>
    )
  }

  if (error || !detail) {
    return (
      <Card className="border-destructive">
        <CardHeader>
          <CardTitle className="text-destructive flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            Error
          </CardTitle>
          <CardDescription>{error || 'Call not found'}</CardDescription>
        </CardHeader>
      </Card>
    )
  }

  const { call, offer, summary } = detail

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
      <button
        onClick={() => navigate('/calls')}
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to calls
      </button>

      <div>
        <h1 className="text-2xl font-bold tracking-tight">Call Details</h1>
        <p className="text-sm text-muted-foreground mt-1">Run ID: {callId}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Call Info */}
        <div className="space-y-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Phone className="h-4 w-4 text-muted-foreground" />
                Call Information
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 pt-0">
              {call && (
                <>
                  <div className="flex items-start gap-3">
                    <Clock className="h-4 w-4 text-muted-foreground mt-0.5" />
                    <div>
                      <p className="text-xs text-muted-foreground">Duration</p>
                      <p className="text-sm font-medium">
                        {call.duration_seconds
                          ? `${Math.floor(call.duration_seconds / 60)}m ${call.duration_seconds % 60}s`
                          : '—'}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <MessageSquare className="h-4 w-4 text-muted-foreground mt-0.5" />
                    <div>
                      <p className="text-xs text-muted-foreground">Status</p>
                      <p className="text-sm font-medium capitalize">{call.status}</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <MapPin className="h-4 w-4 text-muted-foreground mt-0.5" />
                    <div>
                      <p className="text-xs text-muted-foreground">Run ID</p>
                      <p className="text-xs font-mono break-all text-muted-foreground">
                        {call.run_id || '—'}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Clock className="h-4 w-4 text-muted-foreground mt-0.5" />
                    <div>
                      <p className="text-xs text-muted-foreground">Started</p>
                      <p className="text-sm font-medium">
                        {call.started_at ? new Date(call.started_at).toLocaleString() : '—'}
                      </p>
                    </div>
                  </div>
                </>
              )}
            </CardContent>
          </Card>

          {offer && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-base flex items-center gap-2">
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                  Offer Details
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 pt-0">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-muted-foreground">MC Number</p>
                    <p className="text-sm font-medium">{offer.mc_number}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Carrier</p>
                    <p className="text-sm font-medium">{offer.carrier_name || '—'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Load ID</p>
                    <p className="text-sm font-medium">{offer.load_id}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Rate</p>
                    <p className="text-sm font-medium">
                      {offer.agreed_rate ? `$${offer.agreed_rate.toLocaleString()}` : '—'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Equipment</p>
                    <p className="text-sm font-medium">{offer.equipment_type || '—'}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 pt-2 border-t">
                  <Truck className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm text-muted-foreground">
                    {offer.origin || '—'} → {offer.destination || '—'}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  {getOutcomeBadge(offer.outcome)}
                  {getSentimentBadge(offer.sentiment)}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Summary */}
        <Card className="lg:col-span-2">
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <MessageSquare className="h-4 w-4 text-muted-foreground" />
              Call Summary
            </CardTitle>
            <CardDescription>
              AI-generated end-of-call summary
            </CardDescription>
          </CardHeader>
          <CardContent>
            {!summary ? (
              <div className="text-center py-12 text-muted-foreground">
                <MessageSquare className="h-8 w-8 mx-auto mb-3 opacity-40" />
                <p className="text-sm">Summary not available</p>
                <p className="text-xs mt-1 max-w-xs mx-auto">
                  This call did not include a generated summary.
                </p>
              </div>
            ) : (
              <div className="max-h-[600px] overflow-y-auto pr-2">
                <p className="text-sm leading-7 whitespace-pre-wrap">{summary}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
