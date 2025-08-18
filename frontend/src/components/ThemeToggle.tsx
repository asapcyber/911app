import { useEffect } from 'react'

export default function ThemeToggle({ dark, setDark }:{ dark:boolean; setDark:(v:boolean)=>void }) {
  useEffect(() => {
    localStorage.setItem('theme', dark ? 'dark' : 'light')
    document.documentElement.classList.toggle('dark', dark)
  }, [dark])

  return (
    <button
      onClick={() => setDark(!dark)}
      className="text-sm px-3 py-1.5 rounded border border-zinc-300 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800"
      aria-label="Thema wisselen"
      title="Thema wisselen"
    >
      {dark ? '🌙 Donker' : '☀️ Licht'}
    </button>
  )
}
