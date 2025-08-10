import { RadialBarChart, RadialBar, PolarAngleAxis } from 'recharts'

export default function Gauge({score}:{score:number}) {
  const pct = Math.max(0, Math.min(1, score))
  const data = [{ name: 'score', value: pct*100, fill: gaugeColor(pct) }]

  return (
    <div className="flex flex-col items-center">
      <RadialBarChart width={240} height={240} cx={120} cy={120} innerRadius={80} outerRadius={110} barSize={18} data={data} startAngle={180} endAngle={0}>
        <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false}/>
        <RadialBar dataKey="value" cornerRadius={10} background />
      </RadialBarChart>
      <div className="mt-2 text-xl font-semibold">{(pct).toFixed(2)}  <span className="text-sm text-zinc-500"> (0=laag, 1=hoog)</span></div>
    </div>
  )
}

function gaugeColor(p:number){
  // smooth gradient green→yellow→red
  if (p < 0.33) return '#22c55e'
  if (p < 0.66) return '#eab308'
  return '#ef4444'
}
