type Tab = { id: string; label: string }
export default function Tabs({tabs, value, onChange}:{tabs:Tab[]; value:string; onChange:(v:string)=>void}) {
  return (
    <div className="flex gap-2 border-b border-zinc-200 dark:border-zinc-800">
      {tabs.map(t => (
        <button
          key={t.id}
          onClick={()=>onChange(t.id)}
          className={[
            "px-3 py-2 text-sm",
            value===t.id ? "border-b-2 border-blue-500 text-blue-600 dark:text-blue-400" : "text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200"
          ].join(' ')}
        >
          {t.label}
        </button>
      ))}
    </div>
  )
}
