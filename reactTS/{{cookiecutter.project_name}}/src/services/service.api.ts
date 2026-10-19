/**
 * Typed fetch client for the FastAPI backend.
 * - base URL from VITE_API_URL (never hard-coded)
 * - Bearer token injected automatically, 401 -> logout
 * - timeout, JSON errors normalized into ApiError
 */

export const API_URL = import.meta.env.VITE_API_URL.replace(/\/+$/, '')
const TIMEOUT_MS = Number(import.meta.env.VITE_API_TIMEOUT_MS ?? 15000)

export class ApiError extends Error {
  readonly status: number
  readonly requestId?: string

  constructor(status: number, message: string, requestId?: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.requestId = requestId
  }
}

interface ApiHooks {
  getToken: () => string | null
  onUnauthorized: () => void
}

let hooks: ApiHooks = { getToken: () => null, onUnauthorized: () => {} }

/** Wired once in main.tsx (keeps this module free of any store import). */
export function configureApi(next: Partial<ApiHooks>) {
  hooks = { ...hooks, ...next }
}

type Method = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

function errorMessage(data: unknown, fallback: string): string {
  if (data && typeof data === 'object' && 'detail' in data) {
    const detail = (data as { detail: unknown }).detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) return detail.map((d) => d?.msg ?? '').filter(Boolean).join(', ') || fallback
    if (detail && typeof detail === 'object' && 'error' in detail) return String((detail as { error: unknown }).error)
  }
  return fallback
}

async function request<T>(method: Method, path: string, body?: unknown, signal?: AbortSignal): Promise<T> {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS)
  signal?.addEventListener('abort', () => controller.abort())

  const headers = new Headers({ Accept: 'application/json' })
  const token = hooks.getToken()
  if (token) headers.set('Authorization', `Bearer ${token}`)

  let payload: BodyInit | undefined
  if (body instanceof FormData) {
    payload = body // the browser sets the multipart boundary itself
  } else if (body !== undefined) {
    headers.set('Content-Type', 'application/json')
    payload = JSON.stringify(body)
  }

  try {
    const response = await fetch(`${API_URL}${path}`, {
      method,
      headers,
      body: payload,
      signal: controller.signal,
      credentials: 'omit', // bearer auth: no cookies sent cross-site
    })
    const data: unknown = response.status === 204 ? null : await response.json().catch(() => null)
    if (!response.ok) {
      if (response.status === 401 && token) hooks.onUnauthorized()
      const requestId = (data as { request_id?: string } | null)?.request_id
      throw new ApiError(response.status, errorMessage(data, response.statusText), requestId)
    }
    return data as T
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw new ApiError(0, 'Request timed out')
    if (error instanceof TypeError) throw new ApiError(0, 'Network error, is the API reachable?')
    throw error
  } finally {
    clearTimeout(timer)
  }
}

export const Get = <T>(path: string, signal?: AbortSignal) => request<T>('GET', path, undefined, signal)
export const Send = <T>(path: string, data?: unknown) => request<T>('POST', path, data)
export const Update = <T>(path: string, data?: unknown) => request<T>('PUT', path, data)
export const Remove = <T>(path: string) => request<T>('DELETE', path)
