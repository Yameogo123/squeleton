import { useContext, createContext, type PropsWithChildren } from 'react';
import { useStorageState } from './useStorageState';

const AuthContext = createContext<{
  signIn: (user:string) => void;
  signOut: () => void;
  updateSession: (key:string, value: string)=> void;
  session?: string | null;
  isLoading: boolean;
}>({
  signIn: (user:string) => null,
  signOut: () => null,
  updateSession: (key:string, value: string)=> null,
  session: null,
  isLoading: false,
});

// This hook can be used to access the user info.
export function useSession() {
    const value = useContext(AuthContext);
    if (process.env.NODE_ENV !== 'production') {
        if (!value) {
            throw new Error('useSession must be wrapped in a <SessionProvider />');
        }
    }

    return value;
}

export function SessionProvider({ children }: PropsWithChildren) {
    const [[isLoading, session], setSession] = useStorageState('session');

    const value = {
        signIn: (user:string) => {
            // Perform sign-in logic here
            setSession(user);
        },
        signOut: () => {
            setSession(null);
        },
        updateSession: (key:string, value:string) => {
            if (session) {
                const sess = JSON.parse(session);
                sess[key] = value;
                setSession(JSON.stringify(sess));
            }
        },
        session,
        isLoading,
    }

    return (
        <AuthContext.Provider
            value={value}
        >
            {children}
        </AuthContext.Provider>
    );
}
