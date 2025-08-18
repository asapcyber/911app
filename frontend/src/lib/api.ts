// src/lib/api.ts
export async function postJSON<T>(path: string, body: unknown, base?: string) {
  const API_BASE = (import.meta as any).env?.VITE_API_BASE ?? ''
  const url = `${base ?? API_BASE}${path}`
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `HTTP ${res.status}`)
  }
  return (await res.json()) as T
}

