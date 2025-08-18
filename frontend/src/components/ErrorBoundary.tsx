import React from 'react'

type Props = { children: React.ReactNode }
type State = { hasError: boolean; error?: any }

export default class ErrorBoundary extends React.Component<Props, State> {
  state: State = { hasError: false }

  static getDerivedStateFromError(error: any) {
    return { hasError: true, error }
  }

  componentDidCatch(error: any, info: any) {
    // eslint-disable-next-line no-console
    console.error('UI crash:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="m-4 rounded-lg border border-red-500/40 bg-red-500/10 p-4 text-red-200">
          <div className="font-semibold mb-1">Er is een fout opgetreden in de UI</div>
          <pre className="text-xs whitespace-pre-wrap opacity-80">
            {String(this.state.error)}
          </pre>
        </div>
      )
    }
    return this.props.children
  }
}
