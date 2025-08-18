import { create } from 'zustand'
import { v4 as uuidv4 } from 'uuid'
export type ChatMsg = { role: 'user' | 'assistant'; text: string }

interface AppState {
  transcript: string
  setTranscript: (t: string) => void

  sessionId: string
  resetSession: () => void

  chat: ChatMsg[]
  addChat: (m: ChatMsg) => void
  clearChat: () => void
}

export const useAppStore = create<AppState>((set) => ({
  transcript: '',
  setTranscript: (t) => set({ transcript: t }),

  sessionId: uuidv4(),
  resetSession: () => set({ sessionId: uuidv4(), chat: [] }),

  chat: [],
  addChat: (m) => set((s) => ({ chat: [...s.chat, m] })),
  clearChat: () => set({ chat: [] }),
}))
