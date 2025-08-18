import { Radar } from 'react-chartjs-2'
import {
  Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend
} from 'chart.js'
ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend)

type Props = {
  title?: string
  emotions: Record<string, number> // {"angst":0.4,...}
}

export default function RadarCard({ title="Emotie Radar", emotions }: Props){
  const labels = Object.keys(emotions)
  const data = {
    labels,
    datasets: [{
      label: 'Intensiteit',
      data: labels.map(k => emotions[k]),
      fill: true,
      borderWidth: 2,
      borderColor: 'rgba(59,130,246,0.9)',     // blue-500
      backgroundColor: 'rgba(59,130,246,0.15)', // fill
      pointBackgroundColor: 'rgba(59,130,246,1)',
      pointBorderColor: '#0a0a0a',
      pointRadius: 2.5,
    }]
  }

  const opts = {
    plugins: { legend: { display: false } },
    scales: {
      r: {
        beginAtZero: true, max: 1,
        angleLines: { color: 'rgba(255,255,255,0.08)' },
        grid: { color: 'rgba(255,255,255,0.08)' },
        pointLabels: { color: '#d4d4d8', font: { size: 11 } },
        ticks: { display: false },
      }
    }
  } as any

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-950/60 backdrop-blur p-4 shadow-sm">
      <h3 className="font-semibold mb-2 text-zinc-100">{title}</h3>
      <div className="h-[280px] flex items-center">
        <Radar data={data} options={opts}/>
      </div>
    </div>
  )
}
