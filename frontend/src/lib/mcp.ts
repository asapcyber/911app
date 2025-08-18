export async function askMCP(session_id: string, query: string, context: string) {
  const res = await fetch('/mcp/query', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ session_id, query, context }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json() as Promise<{ response: string }>
}

export async function resetMCP(session_id: string) {
  const res = await fetch('/mcp/reset', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ session_id }),
  })
  return res.ok
}

