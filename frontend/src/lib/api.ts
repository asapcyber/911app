type ScoreResp = { score: number }
type SensResp  = { results: { Term: string; delta?: number; ["Δ Change"]?: number }[] }

const MOCK = import.meta.env.VITE_MOCK === '1';

export async function postJSON<T>(url: string, body: unknown, init?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body),
    ...init,
  })

  // Try to parse JSON; if it fails, read text for a clearer error
  let text = ''
  try {
    text = await res.text()
    const json = text ? JSON.parse(text) : {}
    if (!res.ok) {
      const detail = (json && (json.detail || json.message)) || text || res.statusText
      throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail))
    }
    return json as T
  } catch (e: any) {
    // If JSON.parse failed, throw raw text
    if (text && (e.name === 'SyntaxError' || e.message?.includes('Unexpected'))) {
      throw new Error(`Server gaf geen geldige JSON terug: ${text.slice(0, 400)}`)
    }
    throw e
  }
}
