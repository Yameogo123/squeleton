import { configureStore } from '@reduxjs/toolkit'
import { useDispatch, useSelector } from 'react-redux'
import authReducer from './hooks.authSlice'
import { loadAuth, saveAuth } from './hooks.storage'

export function makeStore(preloadedAuth = loadAuth()) {
  return configureStore({
    reducer: { auth: authReducer },
    preloadedState: preloadedAuth ? { auth: preloadedAuth } : undefined,
  })
}

export const store = makeStore()

// persist only when the auth slice actually changes
let previousAuth = store.getState().auth
store.subscribe(() => {
  const { auth } = store.getState()
  if (auth !== previousAuth) {
    previousAuth = auth
    saveAuth(auth)
  }
})

export type AppStore = ReturnType<typeof makeStore>
export type RootState = ReturnType<AppStore['getState']>
export type AppDispatch = AppStore['dispatch']

export const useAppDispatch = useDispatch.withTypes<AppDispatch>()
export const useAppSelector = useSelector.withTypes<RootState>()
