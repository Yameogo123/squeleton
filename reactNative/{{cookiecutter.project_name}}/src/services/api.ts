/**
 * Typed fetch client for the FastAPI backend.
 * Base URL: EXPO_PUBLIC_API_URL > app.json extra.apiUrl > (dev only) Metro host + apiPort.
 */
import Constants from 'expo-constants';

const extra = (Constants.expoConfig?.extra ?? {}) as { apiUrl?: string; apiPort?: string };

/** null when not configured (prod build without EXPO_PUBLIC_API_URL): requests then fail cleanly. */
export function resolveApiUrl(): string | null {
  const explicit = process.env.EXPO_PUBLIC_API_URL || extra.apiUrl;
  if (explicit) return explicit.replace(/\/+$/, '');
  // dev: the machine running Metro also runs the API -> works on simulators AND real devices
  const host = Constants.expoConfig?.hostUri?.split(':')[0];
  if (__DEV__) return `http://${host ?? 'localhost'}:${extra.apiPort ?? '3000'}`;
  return null;
}
const TIMEOUT_MS = 15_000;

export class ApiError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

type Hooks = { getToken: () => string | null; onUnauthorized: () => void };
let hooks: Hooks = { getToken: () => null, onUnauthorized: () => {} };

/** Wired by the SessionProvider (keeps this module free of React). */
export function configureApi(next: Partial<Hooks>) {
  hooks = { ...hooks, ...next };
}

function messageFrom(data: unknown, fallback: string): string {
  const detail = (data as { detail?: unknown } | null)?.detail;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) return detail.map((d) => d?.msg).filter(Boolean).join(', ') || fallback;
  if (detail && typeof detail === 'object' && 'error' in detail) return String((detail as { error: unknown }).error);
  return fallback;
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const baseUrl = resolveApiUrl();
  if (!baseUrl) throw new ApiError(0, 'API non configurée (EXPO_PUBLIC_API_URL)');
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  const token = hooks.getToken();
  const headers: Record<string, string> = { Accept: 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body !== undefined && !(body instanceof FormData)) headers['Content-Type'] = 'application/json';

  try {
    const response = await fetch(`${baseUrl}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : body instanceof FormData ? body : JSON.stringify(body),
      signal: controller.signal,
    });
    const data: unknown = response.status === 204 ? null : await response.json().catch(() => null);
    if (!response.ok) {
      if (response.status === 401 && token) hooks.onUnauthorized();
      throw new ApiError(response.status, messageFrom(data, `Erreur ${response.status}`));
    }
    return data as T;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    if ((error as Error)?.name === 'AbortError') throw new ApiError(0, 'Le serveur ne répond pas');
    throw new ApiError(0, 'Connexion impossible au serveur');
  } finally {
    clearTimeout(timer);
  }
}

export const api = {
  get: <T>(path: string) => request<T>('GET', path),
  post: <T>(path: string, body?: unknown) => request<T>('POST', path, body),
  put: <T>(path: string, body?: unknown) => request<T>('PUT', path, body),
  delete: <T>(path: string) => request<T>('DELETE', path),
};
