import axios from 'axios'

const api = axios.create({
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

export default api

export async function fetchMetrics() {
  const res = await api.get('/api/dashboard/metrics')
  return res.data
}

export async function fetchCalls() {
  const res = await api.get('/api/dashboard/calls')
  return res.data
}

export async function fetchCallDetail(runId: string) {
  const res = await api.get(`/api/dashboard/calls/${runId}`)
  return res.data
}

export async function login(password: string) {
  const res = await api.post('/api/auth/login', { password })
  return res.data
}

export async function logout() {
  const res = await api.post('/api/auth/logout')
  return res.data
}

export async function checkAuth() {
  const res = await api.get('/api/auth/me')
  return res.data
}
