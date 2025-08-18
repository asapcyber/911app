type Item = { term:string; delta:number }
export default function RiskChips({ items=[] as Item[] }){
  return (
    <div className="flex flex-wrap gap-2">
      {items.map((t,i)=>(
        <span key={i}
          className={`px-2 py-1 text-xs rounded-full border ${
            t.delta < 0 ? 'border-red-400 text-red-400 bg-red-400/10' : 'border-zinc-400 text-zinc-400'
          }`}>
          {t.term} {t.delta<0 ? `(${t.delta.toFixed(2)})` : ''}
        </span>
      ))}
    </div>
  )
}
