import { Component, type ErrorInfo, type ReactNode } from 'react'

interface State {
  hasError: boolean
}

/** Catches render errors so one broken component doesn't blank the whole app. */
export default class ErrorBoundary extends Component<{ children: ReactNode }, State> {
  state: State = { hasError: false }

  static getDerivedStateFromError(): State {
    return { hasError: true }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    // plug your error tracker (Sentry, ...) here
    console.error(error, info.componentStack)
  }

  render() {
    if (this.state.hasError) {
      return (
        <main className="flex min-h-screen flex-col items-center justify-center gap-4">
          <h1 className="text-xl font-semibold">Something went wrong.</h1>
          <button type="button" className="underline" onClick={() => window.location.assign('/')}>
            Reload
          </button>
        </main>
      )
    }
    return this.props.children
  }
}
