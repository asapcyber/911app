import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

export type SensRow = { term: string; delta: number }

export default function SensitivityBar({rows}:{rows:SensRow[]}) {
  const data = rows.map(r => ({ ...r, label: `‘${r.term}’` }))
  return (
    <div className="w-full h-64">
      <ResponsiveContainer>
        <BarChart data={data} layout="vertical" margin={{left: 40, right: 20, top: 10, bottom: 10}}>
          <XAxis type="number" />
          <YAxis type="category" dataKey="label" width={120}/>
          <Tooltip formatter={(v:any)=>Number(v).toFixed(3)} />
          <Bar dataKey="delta">
            {data.map((entry, idx) => (
              <Cell key={idx} fill={entry.delta < 0 ? '#ef4444' : '#22c55e'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
