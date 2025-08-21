// src/App.tsx
import { NavLink, Route, Routes, Navigate } from 'react-router-dom'
import TranscriptPage from './routes/TranscriptPage'
import McpAgentPage from './routes/McpAgentPage'

//function NavItem({ to, label }: { to: string; label: string }) {
//  return (
//    <NavLink
//      to={to}
//      className={({ isActive }) =>
//        [
//          "px-3 py-2 rounded-lg text-sm font-medium transition-colors",
//          "text-zinc-300 hover:text-white",
//          isActive ? "bg-zinc-800/70 text-white border border-zinc-700" : "hover:bg-zinc-800/40"
//        ].join(' ')
//      }
//    >
//      {label}
//    </NavLink>
// )
//}

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-950 via-zinc-900 to-black text-zinc-100">
      {/* Header */}
<header className="sticky top-0 z-40 bg-white text-black border-b border-zinc-200">
  <div className="container mx-auto px-4 py-3 flex items-center gap-3">
    <img
      src="/logo.svg"
      alt="112 Analyzer"
      className="h-10 w-30"
    />
    <div className="text-2xl text-[#154273] font-bold tracking-wide">
      112 Analyzer
    </div>
    <nav className="ml-auto flex items-center gap-2">
      <NavLink
        to="/transcript"
        className={({ isActive }) =>
          [
            "px-3 py-2 rounded-lg text-sm font-medium transition-colors",
            "text-zinc-700 hover:text-black",
            isActive ? "bg-zinc-100 text-black border border-zinc-200" : "hover:bg-zinc-100"
          ].join(' ')
        }
      >
        Analyse
      </NavLink>
      <NavLink
        to="/agent"
        className={({ isActive }) =>
          [
            "px-3 py-2 rounded-lg text-sm font-medium transition-colors",
            "text-zinc-700 hover:text-black",
            isActive ? "bg-zinc-100 text-black border border-zinc-200" : "hover:bg-zinc-100"
          ].join(' ')
        }
      >
        MCP Agent
      </NavLink>
    </nav>
  </div>
</header>

      {/* Main */}
      <main className="container mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<Navigate to="/transcript" replace />} />
          <Route path="/transcript" element={<TranscriptPage />} />
          <Route path="/agent" element={<McpAgentPage />} />
          <Route path="*" element={
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 backdrop-blur p-6">
              <h2 className="text-xl font-semibold mb-2">Pagina niet gevonden</h2>
              <p className="text-zinc-400">
                De opgevraagde pagina bestaat niet. Ga terug naar&nbsp;
                <NavLink className="text-blue-400 hover:underline" to="/transcript">Analyse</NavLink>.
              </p>
            </div>
          } />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-200 bg-white text-black">
  <div className="container mx-auto px-4 py-4 text-xs flex flex-col sm:flex-row gap-2 sm:gap-4 items-center justify-between">
    <div>© {new Date().getFullYear()} 112 Analyzer</div>
    <div className="flex items-center gap-3">
      <a
        className="text-zinc-700 hover:text-black transition-colors"
        href="https://www.asapcyber.com/"
        target="_blank" rel="noreferrer"
      >
        © Asapcyber
      </a>
      <span className="text-zinc-400 hidden sm:inline">•</span>
      <span className="text-zinc-500">
        Donker content, witte chrome
      </span>
    </div>
  </div>
</footer>
    </div>
  )
}
