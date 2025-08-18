//import React from 'react'

type Props = {
  term: string
  delta: number // negative = score goes DOWN when removed (important/risky term)
  maxAbs?: number // optional cap for scaling, default 1.0
}

function clamp01(x: number) {
  return Math.max(0, Math.min(1, x))
}

export default function SensitivityBar({ term, delta, maxAbs = 1 }: Props) {
  // map |delta| to a 0..1 width; assume typical deltas in [-1, 1]
  const widthPct = clamp01(Math.abs(delta) / maxAbs) * 100
  const isReducing = delta < 0 // removing term reduces danger => strong risk signal
  const barColor = isReducing ? 'bg-red-500/80' : 'bg-zinc-500/60'
  const borderColor = isReducing ? 'border-red-400/60' : 'border-zinc-500/40'
  const textColor = isReducing ? 'text-red-300' : 'text-zinc-300'
  const sign = delta > 0 ? '+' : ''

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-1">
        <span className={`text-xs ${textColor} truncate`} title={term}>
          {term}
        </span>
        <span className={`text-xs ${textColor}`}>
          {sign}{delta.toFixed(2)}
        </span>
      </div>
      <div className={`w-full h-2 rounded-full bg-zinc-800 border ${borderColor} overflow-hidden`}>
        <div
          className={`${barColor} h-full transition-all`}
          style={{ width: `${widthPct}%` }}
          aria-label={`Delta ${delta.toFixed(2)} voor ${term}`}
          title={`Δ ${delta.toFixed(2)}`}
        />
      </div>
      {isReducing && (
        <div className="mt-1 text-[10px] text-red-400/80">
          verwijderen → lagere score (risicorelevante term)
        </div>
      )}
    </div>
  )
}
