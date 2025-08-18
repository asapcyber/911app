// src/routes/McpAgentPage.tsx
import { useEffect, useMemo, useRef, useState } from 'react'
import { askMCP, resetMCP } from '../lib/mcp'
import { useAppStore } from '../state/appStore'
import clsx from 'clsx'

export default function McpAgentPage(){
  const transcript = useAppStore(s => s.transcript)
  const sessionId = useAppStore(s => s.sessionId)
  const addChat = useAppStore(s => s.addChat)
  const clearChat = useAppStore(s => s.clearChat)
  const resetSession = useAppStore(s => s.resetSession)
  const chat = useAppStore(s => s.chat)

  const [q, setQ] = useState('')
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState<string | null>(null)

  const scrollRef = useRef<HTMLDivElement>(null)
  useEffect(() => { scrollRef.current?.scrollTo(0, scrollRef.current.scrollHeight) }, [chat, loading])

  async function onAsk(){
    if (!q.trim()) return
    setErr(null); setLoading(true)
    const userMsg = q.trim()
    addChat({ role: 'user', text: userMsg })
    setQ('')

    try {
      const { response } = await askMCP(sessionId, userMsg, transcript || '')
      addChat({ role: 'assistant', text: response })
    } catch (e:any) {
      let msg = e.message ?? 'Onbekende fout'
      try {
        const parsed = JSON.parse(msg); if (parsed?.detail) msg = parsed.detail
      } catch {}
      setErr(msg)
    } finally {
      setLoading(false)
    }
  }

  async function onReset(){
    await resetMCP(sessionId)
    resetSession()
    clearChat()
    setErr(null)
  }

  const placeholder = useMemo(() =>
    transcript ? "Stel je vraag over dit incident…" :
    "Plak eerst een transcript in het Analyse-tabblad, of stel je vraag zonder context…",
    [transcript]
  )

  return (
    <div className="grid lg:grid-cols-2 gap-6">
      {/* Left: live chat */}
      <section className="rounded-xl border border-zinc-200 bg-white text-black shadow-sm flex flex-col">
        <div className="p-3 border-b border-zinc-200 flex items-center gap-3">
          <div className="font-semibold">MCP Agent</div>
          <div className="ml-auto flex items-center gap-2">
            <button onClick={onReset} className="text-sm px-3 py-1.5 rounded bg-zinc-100 hover:bg-zinc-200">
              Reset gesprek
            </button>
          </div>
        </div>

        <div ref={scrollRef} className="p-4 space-y-3 overflow-y-auto" style={{minHeight: 320, maxHeight: 520}}>
          {chat.length === 0 && (
            <p className="text-sm text-zinc-500">
              Geen berichten. {transcript ? "Je transcript is al als context toegevoegd." : "Voeg een transcript toe in het Analyse-tabblad voor betere context."}
            </p>
          )}
          {chat.map((m, i) => (
            <div key={i} className={clsx(
              "max-w-[85%] px-3 py-2 rounded-lg shadow-sm whitespace-pre-wrap",
              m.role === 'user'
                ? "bg-blue-600 text-white ml-auto"
                : "bg-zinc-100 text-zinc-900 mr-auto"
            )}>
              {m.text}
            </div>
          ))}
          {loading && <div className="text-sm text-zinc-500">Denken…</div>}
          {err && <div className="text-sm text-red-500">{err}</div>}
        </div>

        <div className="p-3 border-t border-zinc-200 flex items-center gap-2">
          <input
            value={q}
            onChange={e=>setQ(e.target.value)}
            onKeyDown={e => { if (e.key==='Enter' && !e.shiftKey) onAsk() }}
            placeholder={placeholder}
            className="flex-1 rounded-lg border border-zinc-300 bg-white text-black p-2 focus:ring-2 focus:ring-blue-500 outline-none"
          />
          <button
            onClick={onAsk}
            disabled={!q.trim() || loading}
            className="px-4 py-2 rounded-lg bg-blue-600 text-white disabled:opacity-50 shadow hover:bg-blue-500"
          >
            Verstuur
          </button>
        </div>
      </section>

      {/* Right: auto-included context */}
      <section className="rounded-xl border border-zinc-200 p-4 bg-white text-black shadow-sm">
        <h3 className="font-semibold mb-2">Context (automatisch vanuit Analyse)</h3>
        <p className="text-xs text-zinc-500 mb-2">Dit wordt meegestuurd met elke vraag.</p>
        <div className="rounded-lg border border-zinc-200 p-3 bg-white text-black whitespace-pre-wrap min-h-[160px]">
          {transcript || <span className="text-zinc-500">Nog geen transcript beschikbaar.</span>}
        </div>
      </section>
    </div>
  )
}
