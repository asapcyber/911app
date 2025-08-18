// src/components/GaugeCard.tsx
type Props = {
  title?: string
  value: number
  subtitle?: string
}

export default function GaugeCard({ title = 'Gevaarscore', value, subtitle }: Props) {
  const pct = Math.max(0, Math.min(100, Math.round(value * 100)))
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 backdrop-blur p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-zinc-100">{title}</h3>
          {subtitle && <p className="text-xs text-zinc-400 mt-1">{subtitle}</p>}
        </div>
        <div className="text-lg font-semibold text-zinc-100">{(value).toFixed(2)}</div>
      </div>
      <div className="mt-4 h-4 w-full bg-zinc-800 rounded">
        <div
          className="h-4 bg-blue-600 rounded"
          style={{ width: `${pct}%`, transition: 'width 300ms ease' }}
        />
      </div>
      <div className="mt-1 text-xs text-zinc-400">{pct}%</div>
    </div>
  )
}
