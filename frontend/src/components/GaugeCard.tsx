// src/components/GaugeCard.tsx

type Props = {
  title?: string
  value: number            // 0..1
  subtitle?: string
  size?: number            // px, outer square size (default 160)
  stroke?: number          // stroke width of ring (default 12)
}

export default function GaugeCard({
  title = 'Gevaarscore',
  value,
  subtitle,
  size = 160,
  stroke = 12,
}: Props) {
  // Clamp and derive numbers
  const v = Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0))
  const pct = Math.round(v * 100)

  // Color ramp
  const color = getRiskColor(v)

  // SVG measurements
  const radius = (size - stroke) / 2
  const circumference = 2 * Math.PI * radius
  const dash = Math.max(0, Math.min(circumference, circumference * v))
  const gap = circumference - dash

  const center = size / 2

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 backdrop-blur p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-zinc-100">{title}</h3>
          {subtitle && <p className="text-xs text-zinc-400 mt-1">{subtitle}</p>}
        </div>
        <div className="text-lg font-semibold text-zinc-100">{v.toFixed(2)}</div>
      </div>

      <div className="mt-4 flex items-center justify-center">
        <svg
          width={size}
          height={size}
          viewBox={`0 0 ${size} ${size}`}
          role="img"
          aria-label={`Gevaarscore ${pct} procent`}
        >
          {/* Background track */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke="rgba(255,255,255,0.08)"
            strokeWidth={stroke}
          />
          {/* Progress arc (rotate so 0 starts at top) */}
          <g transform={`rotate(-90 ${center} ${center})`}>
            <circle
              cx={center}
              cy={center}
              r={radius}
              fill="none"
              stroke={color}
              strokeWidth={stroke}
              strokeLinecap="round"
              strokeDasharray={`${dash} ${gap}`}
              style={{ transition: 'stroke-dasharray 400ms ease, stroke 200ms ease' }}
            />
          </g>

          {/* Center labels */}
          <g>
            <text
              x="50%"
              y="48%"
              textAnchor="middle"
              className="fill-zinc-100"
              style={{ fontSize: size * 0.22, fontWeight: 700 }}
            >
              {pct}%
            </text>
            <text
              x="50%"
              y="64%"
              textAnchor="middle"
              className="fill-zinc-400"
              style={{ fontSize: size * 0.11, fontWeight: 500 }}
            >
              {v.toFixed(2)}
            </text>
          </g>
        </svg>
      </div>

      <div className="mt-2 text-xs text-zinc-400 text-center">
        0 = Laag risico &nbsp;•&nbsp; 1 = Hoog risico
      </div>
    </div>
  )
}

/** Green → Yellow → Orange → Red as risk increases */
function getRiskColor(v: number): string {
  if (v < 0.25) return '#22c55e'   // green-500
  if (v < 0.5)  return '#eab308'   // yellow-500
  if (v < 0.75) return '#f97316'   // orange-500
  return '#ef4444'                 // red-500
}
