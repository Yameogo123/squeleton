/**
 * Auth session: token + user, persisted in the secure store, expired automatically,
 * cleared on any 401. Routes read it through `useSession()`.
 */
import { createContext, use, useCallback, useEffect, useMemo, useState, type PropsWithChildren } from 'react';
import { configureApi } from '@/services/api';
import type { Session } from '@/services/auth';
import { getSecure, setSecure } from '@/lib/storage';

const KEY = 'session';

// token kept outside React so the API client always sees the latest value synchronously
let currentToken: string | null = null;
let onUnauthorized: () => void = () => {};
configureApi({ getToken: () => currentToken, onUnauthorized: () => onUnauthorized() });

type SessionContextValue = {
  session: Session | null;
  isLoading: boolean;
  signIn: (session: Session) => Promise<void>;
  signOut: () => Promise<void>;
};

const SessionContext = createContext<SessionContextValue | null>(null);

export function useSession(): SessionContextValue {
  const value = use(SessionContext);
  if (!value) throw new Error('useSession must be used inside <SessionProvider>');
  return value;
}

function parse(raw: string | null): Session | null {
  if (!raw) return null;
  try {
    const session = JSON.parse(raw) as Session;
    return session.token && session.expiresAt > Date.now() ? session : null;
  } catch {
    return null;
  }
}

export function SessionProvider({ children }: PropsWithChildren) {
  const [session, setSession] = useState<Session | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const signOut = useCallback(async () => {
    currentToken = null;
    setSession(null);
    await setSecure(KEY, null);
  }, []);

  const signIn = useCallback(async (next: Session) => {
    currentToken = next.token;
    setSession(next);
    await setSecure(KEY, JSON.stringify(next));
  }, []);

  // restore on launch
  useEffect(() => {
    getSecure(KEY)
      .then((raw) => {
        const restored = parse(raw);
        currentToken = restored?.token ?? null;
        setSession(restored);
      })
      .finally(() => setIsLoading(false));
  }, []);

  // any 401 from the API logs the user out
  useEffect(() => {
    onUnauthorized = () => void signOut();
  }, [signOut]);

  // logout exactly when the token expires
  useEffect(() => {
    if (!session) return;
    const timer = setTimeout(() => void signOut(), Math.min(session.expiresAt - Date.now(), 2 ** 31 - 1));
    return () => clearTimeout(timer);
  }, [session, signOut]);

  const value = useMemo(() => ({ session, isLoading, signIn, signOut }), [session, isLoading, signIn, signOut]);
  return <SessionContext value={value}>{children}</SessionContext>;
}
