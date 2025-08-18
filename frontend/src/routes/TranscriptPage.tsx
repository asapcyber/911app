// src/routes/TranscriptPage.tsx
import { useState } from 'react'
import { postJSON } from '../lib/api'
import { useAppStore } from '../state/appStore'
import GaugeCard from '../components/GaugeCard'
import SensitivityBar from '../components/SensitivityBar'
import RadarCard from '../components/RadarCard'
import MapCard from '../components/MapCard'
import RiskChips from '../components/RiskChips'

type SensItem = { term: string; delta: number }

export default function TranscriptPage() {
  const setTranscript = useAppStore(s => s.setTranscript)

  const [text, setText] = useState('')
  const [lat, setLat] = useState<string>('')
  const [lon, setLon] = useState<string>('')

  const [score, setScore] = useState<number | null>(null)
  const [sens, setSens] = useState<SensItem[]>([])
  const [emotions, setEmotions] = useState<Record<string, number>>({})
  const [actions, setActions] = useState<string[]>([])

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function analyze() {
    if (!text.trim()) return
    setLoading(true)
    setError(null)
    setScore(0)          // gauge always has a number
    setSens([])
    setEmotions({})
    setActions([])

    try {
      // 1) Combined analyze (fallback to split endpoints if needed)
      let s = 0
      let sensRes: Array<{ Term?: string; term?: string; delta: number }> = []
      try {
        const { score, results } = await postJSON<{ score: number; results: Array<{ Term?: string; term?: string; delta: number }> }>(
          '/api/analyze',
          { transcript: text, top_n: 12 }
        )
        s = Number(score) || 0
        sensRes = results || []
      } catch {
        const [{ score }, { results }] = await Promise.all([
          postJSON<{ score: number }>('/api/score', { transcript: text }),
          postJSON<{ results: Array<{ Term?: string; term?: string; delta: number }> }>('/api/sensitivity', {
            transcript: text,
            top_n: 12,
          }),
        ])
        s = Number(score) || 0
        sensRes = results || []
      }

      setScore(s)
      setSens(
        sensRes
          .map(r => ({ term: (r.Term ?? r.term ?? '').toString(), delta: Number(r.delta) || 0 }))
          .filter(x => !!x.term)
      )
      setTranscript(text)

      // 2) Sentiment (soft-fail)
      try {
        const { emotions } = await postJSON<{ emotions: Record<string, number> }>('/api/sentiment', { transcript: text })
        setEmotions(emotions || {})
      } catch (e: any) {
        console.warn('Sentiment mislukt:', e?.message)
      }

      // 3) Recommendations (soft-fail)
      try {
        const { actions } = await postJSON<{ actions: string[] }>('/api/recommend', { transcript: text, score: s })
        setActions(actions || [])
      } catch (e: any) {
        console.warn('Aanbevelingen mislukt:', e?.message)
      }
    } catch (e: any) {
      setError(e?.message ?? 'Er is een onbekende fout opgetreden.')
    } finally {
      setLoading(false)
    }
  }

  const sensHas = sens && sens.length > 0
  const topRisk = sens.filter(x => x.delta < 0).sort((a, b) => a.delta - b.delta).slice(0, 6)

  const latNum = lat.trim() ? Number(lat) : undefined
  const lonNum = lon.trim() ? Number(lon) : undefined
  const locOk = latNum != null && !Number.isNaN(latNum) && lonNum != null && !Number.isNaN(lonNum)

  return (
    <div className="space-y-6">
      {/* Input */}
      <section className="rounded-xl border border-zinc-800 bg-zinc-900/60 backdrop-blur shadow-sm">
        <div className="p-4 sm:p-5">
          <h2 className="text-lg font-semibold mb-2">Transcript invoer (112)</h2>
          <p className="text-sm text-zinc-400 mb-3">
            Plak hieronder het 112-gesprek. Voeg optioneel latitude/longitude toe voor kaartweergave. Klik daarna op <em>Analyseer</em>.
          </p>
          <textarea
            className="w-full rounded-lg border border-zinc-700 bg-zinc-900/60 text-zinc-100 p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[160px]"
            placeholder='Bijv: "Mijn vriendin snijdt zichzelf met een mes en bedreigt iedereen..."'
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <div className="mt-3 grid grid-cols-1 sm:grid-cols-3 gap-3">
            <input
              className="rounded-lg border border-zinc-700 bg-zinc-900/60 text-zinc-100 p-2"
              placeholder="Latitude (bijv. 52.3702)"
              value={lat}
              onChange={e => setLat(e.target.value)}
            />
            <input
              className="rounded-lg border border-zinc-700 bg-zinc-900/60 text-zinc-100 p-2"
              placeholder="Longitude (bijv. 4.8952)"
              value={lon}
              onChange={e => setLon(e.target.value)}
            />
            <button
              onClick={analyze}
              disabled={!text.trim() || loading}
              className="px-4 py-2 rounded-lg bg-blue-600 text-white disabled:opacity-50 shadow hover:bg-blue-500"
            >
              {loading ? 'Analyseren…' : 'Analyseer'}
            </button>
          </div>
          {error && <div className="mt-2 text-sm text-red-400">{error}</div>}
        </div>
      </section>

      {/* Top row: gauge + map */}
      <section className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <GaugeCard title="Gevaarscore" value={score ?? 0} subtitle="0 = Laag, 1 = Hoog" />
        </div>
        <div className="lg:col-span-2">
          <MapCard lat={locOk ? latNum : undefined} lon={locOk ? lonNum : undefined} label="Meldingslocatie" />
        </div>
      </section>

      {/* Sensitivity + Radar + Risk chips */}
      <section className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 rounded-xl border border-zinc-800 bg-zinc-900/40 backdrop-blur p-4">
          <h3 className="text-base font-semibold mb-1 text-zinc-100">Gevoeligheidsanalyse</h3>
          <p className="text-sm text-zinc-400 mb-4">Impact van het <em>verwijderen</em> van termen (negatief = score daalt).</p>

          {!loading && score !== null && sensHas ? (
            <div className="space-y-2">
              {sens.map((s, i) => (
                <SensitivityBar key={i} term={s.term} delta={s.delta} />
              ))}
            </div>
          ) : !loading && score !== null ? (
            <div className="text-sm text-zinc-500">Geen gevoelige termen geïdentificeerd.</div>
          ) : (
            <div className="text-sm text-zinc-500">Resultaten worden berekend…</div>
          )}
        </div>

        {/* Center the RadarCard nicely inside its column */}
        <div className="flex items-center justify-center">
          <div className="w-full">
            <RadarCard title="Emotie Radar" emotions={emotions} />
          </div>
        </div>
      </section>

      {/* Top risk terms + actions */}
      <section className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 rounded-xl border border-zinc-800 bg-zinc-900/40 backdrop-blur p-4">
          <h3 className="font-semibold mb-2 text-zinc-100">Top risicotermen</h3>
          {topRisk.length ? (
            <RiskChips items={topRisk} />
          ) : (
            <p className="text-sm text-zinc-500">Nog geen risicotermen.</p>
          )}
        </div>

        <div className="lg:col-span-2 rounded-xl border border-zinc-800 bg-zinc-900/40 backdrop-blur p-4">
          <h3 className="font-semibold mb-2 text-zinc-100">Aanbevolen Next-Best Actions</h3>
          {actions.length ? (
            <ul className="list-disc pl-5 space-y-1 text-zinc-200">
              {actions.map((a, i) => (
                <li key={i}>{a}</li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-zinc-500">Nog geen aanbevelingen.</p>
          )}
        </div>
      </section>
    </div>
  )
}
