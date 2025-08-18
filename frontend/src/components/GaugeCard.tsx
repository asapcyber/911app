import React from 'react'

type Props = {
  title?: string
  subtitle?: string
  value: number // expected 0..1
}

function clamp01(x: number) {
  if (Number.isNaN(x)) return 0
  return Math.max(0, Math.min(1, x))
}

function severityColor(v: number) {
  // 0 -> green, 0.5 -> yellow/orange, 1 -> red
  if (v < 0.33) return '#10b981' // emerald-500
  if (v < 0.66) return '#f59e0b' // amber-500
  return '#ef4444'               // red-500
}

export default function GaugeCard({ title = 'Gevaarscore', subtitle, value }: Props) {
  const v = clamp01(value)
  const size = 170
  const stroke = 14
  const r = (size - stroke) / 2
  const cx = size / 2
  const cy = size / 2
  const circumference = 2 * Math.PI * r
  const progress = circumference * v

  const trackColor = '#27272a' // zinc-800
  const barColor = severityColor(v)

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 backdrop-blur p-4 shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-semibold text-zinc-100">{title}</h3>
        <span className="text-xs text-zinc-500">{(v * 100).toFixed(0)}%</span>
      </div>

      <div className="flex items-center justify-center py-2">
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} role="img" aria-label={`Gevaarscore ${Math.round(v*100)}%`}>
          {/* Track */}
          <circle
            cx={cx}
            cy={cy}
            r={r}
            fill="none"
            stroke={trackColor}
            strokeWidth={stroke}
          />
          {/* Progress */}
          <circle
            cx={cx}
            cy={cy}
            r={r}
            fill="none"
            stroke={barColor}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={`${progress} ${circumference}`}
            transform={`rotate(-90 ${cx} ${cy})`}
          />
          {/* Center text */}
          <g aria-hidden="true">
            <text
              x="50%"
              y="50%"
              textAnchor="middle"
              dominantBaseline="middle"
              className="fill-zinc-100"
              fontSize="28"
              fontWeight={700}
            >
              {v.toFixed(2)}
            </text>
            <text
              x="50%"
              y="62%"
              textAnchor="middle"
              dominantBaseline="middle"
              className="fill-zinc-400"
              fontSize="11"
            >
              laag
            </text>
            <text
              x="50%"
              y="74%"
              textAnchor="middle"
              dominantBaseline="middle"
              className="fill-zinc-400"
              fontSize="11"
            >
              hoog
            </text>
          </g>
        </svg>
      </div>

      {subtitle && <p className="text-xs text-zinc-500 text-center mt-1">{subtitle}</p>}

      <div className="mt-3 grid grid-cols-3 gap-2 text-[10px] text-zinc-400">
        <span className="text-left">0</span>
        <span className="text-center">0.5</span>
        <span className="text-right">1.0</span>
      </div>
    </div>
  )
}
