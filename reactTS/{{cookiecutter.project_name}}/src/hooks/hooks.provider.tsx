import type { ReactNode } from 'react'
import { Provider } from 'react-redux'
import { store } from './hooks.store'

export default function Provide({ children }: { children: ReactNode }) {
  return <Provider store={store}>{children}</Provider>
}
