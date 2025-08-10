import { useEffect, useState } from 'react'
import TranscriptPage from './routes/TranscriptPage'
import McpAgentPage from './routes/McpAgentPage'
import Tabs from './components/Tabs'
import ThemeToggle from './components/ThemeToggle'
import { clsx } from 'clsx'

export default function App() {
  const [tab, setTab] = useState<'transcript'|'mcp'>('transcript')
  const [dark, setDark] = useState(false)

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
  }, [dark])

  return (
    <div className={clsx('min-h-screen', 'bg-zinc-50 text-zinc-900',
                         'dark:bg-zinc-900 dark:text-zinc-100')}>
      <header className="border-b border-zinc-200 dark:border-zinc-800">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-3">
          <span className="text-2xl">🚨 112 Gevaren Analyzer</span>
          <div className="ml-auto flex items-center gap-3">
            <ThemeToggle dark={dark} setDark={setDark}/>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6">
        <Tabs
          tabs={[
            { id: 'transcript', label: 'Transcript' },
            { id: 'mcp', label: 'MCP Agent (beta)' }
          ]}
          value={tab}
          onChange={(t)=>setTab(t as any)}
        />
        <div className="mt-6">
          {tab === 'transcript' ? <TranscriptPage/> : <McpAgentPage/>}
        </div>
      </main>
    </div>
  )
}
