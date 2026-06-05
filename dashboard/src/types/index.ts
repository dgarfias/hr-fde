export interface MetricsResponse {
  total_calls: number
  total_offers: number
  avg_duration_seconds: number
  avg_duration_minutes: number
  outcomes: Record<string, number>
  sentiments: Record<string, number>
  booking_rate: number
  unverified_carriers: number
  loads_not_found: number
  calls_last_7_days: { date: string; count: number }[]
}

export interface CallRecord {
  id: string
  run_id: string
  mc_number: string | null
  carrier_name: string | null
  load_id: string | null
  origin: string | null
  destination: string | null
  equipment_type: string | null
  agreed_rate: number | null
  initial_rate: number | null
  outcome: string | null
  sentiment: string | null
  duration_seconds: number | null
  started_at: string | null
  ended_at: string | null
  summary: string | null
  loads_found: boolean
  call_dropped: boolean
  created_at: string
}

export interface CallDetail {
  call: {
    id: string
    run_id: string
    duration_seconds: number | null
    status: string
    started_at: string | null
    ended_at: string | null
  } | null
  offer: {
    id: string
    mc_number: string
    carrier_name: string | null
    load_id: string
    agreed_rate: number | null
    initial_rate: number | null
    outcome: string
    sentiment: string | null
    origin: string | null
    destination: string | null
    equipment_type: string | null
    created_at: string
  } | null
  summary: string | null
}
