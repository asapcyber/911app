type Tab = { id: string; label: string }

export default function Tabs({
  tabs, value, onChange
}: { tabs: Tab[]; value: string; onChange: (v: string) => void }) {
  return (
    <div className="flex gap-1 border-b border-zinc-200 dark:border-zinc-800">
      {tabs.map(t => {
        const active = value === t.id
        return (
          <button
            key={t.id}
            onClick={() => onChange(t.id)}
            className={[
              "relative px-3 py-2 text-sm rounded-t",
              active
                ? "text-blue-600 dark:text-blue-400"
                : "text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200"
            ].join(' ')}
          >
            {t.label}
            <span className={[
              "absolute left-0 right-0 -bottom-[1px] h-[2px]",
              active ? "bg-blue-500" : "bg-transparent"
            ].join(' ')} />
          </button>
        )
      })}
    </div>
  )
}

