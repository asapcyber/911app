import { useState } from 'react'
import Gauge from '../components/Gauge'
import SensitivityBar, { SensRow } from '../components/SensitivityBar'
import { postJSON } from '../lib/api'

export default function TranscriptPage() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [score, setScore] = useState<number | null>(null)
  const [sens, setSens] = useState<SensRow[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  const analyze = async () => {
    setLoading(true); setError(null)
    try {
      const [{ score }, { results }] = await Promise.all([
        postJSON<{score:number}>('/api/score', { transcript: text }),
        postJSON<{results:{Term:string;["Δ Change"]:number}[]}>('/api/sensitivity', { transcript: text })
      ])
      setScore(score)
      setSens(results.map(r => ({ term: r.Term, delta: r["Δ Change"] })))
    } catch (e:any) {
      setError(e.message ?? 'Onbekende fout')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid md:grid-cols-2 gap-6">
      <section className="space-y-3">
        <label className="block text-sm font-medium">Transcript (Nederlands)</label>
        <textarea
          value={text}
          onChange={e=>setText(e.target.value)}
          rows={10}
          className="w-full rounded border border-zinc-300 dark:border-zinc-700 bg-white/70 dark:bg-zinc-900/50 p-3"
          placeholder="Bijv: Mijn vriendin snijdt zichzelf met een mes en bedreigt iedereen; ik moest vluchten."
        />
        <div className="flex gap-3">
          <button
            onClick={analyze}
            disabled={!text.trim() || loading}
            className="px-4 py-2 rounded bg-blue-600 text-white disabled:opacity-50"
          >
            {loading ? 'Analyseren…' : 'Analyseer'}
          </button>
          {error && <span className="text-red-500 text-sm">{error}</span>}
        </div>
      </section>

      <section className="space-y-6">
        <div className="rounded border border-zinc-200 dark:border-zinc-800 p-4">
          <h3 className="font-semibold mb-2">Gevaarscore</h3>
          {score !== null ? <Gauge score={score}/> : <p className="text-sm text-zinc-500">Nog geen score.</p>}
        </div>

        <div className="rounded border border-zinc-200 dark:border-zinc-800 p-4">
          <h3 className="font-semibold mb-2">Gevoeligheidsanalyse</h3>
          {sens?.length ? <SensitivityBar rows={sens}/> : <p className="text-sm text-zinc-500">Nog geen resultaten.</p>}
        </div>
      </section>
    </div>
  )
}
