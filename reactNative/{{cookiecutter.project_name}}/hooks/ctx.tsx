import { useContext, createContext, type PropsWithChildren, useEffect, useState, ReactNode, useCallback } from 'react';
import { getSessionInfo, useStorageState } from './useStorageState';
import { getAnInformationSync } from './useInformations';
import { sessionType } from '@/assets/constantes/types';
import { LoadingOverlay } from '@/pages/components/loading_page';

const AuthContext = createContext<{
    signIn: (user:string) => void;
    signOut: () => void;
    updateSession: (key:string, value?: string)=> void;
    session?: string | null;
    isLoading: boolean;
}>({
    signIn: (user:string) => null,
    signOut: () => null,
    updateSession: (key:string, value?: string)=> null,
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

    return (
        <AuthContext.Provider
            value={{
                signIn: (user) => {
                    // Perform sign-in logic here
                    setSession(user);
                },
                signOut: () => {
                    setSession(null);
                },
                updateSession: (key:string, value?:string) => {
                    if (session) {
                        const sess = JSON.parse(session);
                        sess[key] = value;
                        setSession(JSON.stringify(sess));
                    }
                },
                session,
                isLoading,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}





/// theme context



interface ThemeColors {
    bgcol: string;
    app_color: string;
    text_color: string;
}

interface ThemeContextType extends ThemeColors {
    refreshTheme: () => Promise<void>;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
    const session  = getSessionInfo() as sessionType;
    const sessionId = session?.userId; 
    
    const [theme, setTheme] = useState<ThemeColors>({
        bgcol: "white",
        app_color: "#6A52ED",
        text_color: "#14315A",
    });

    const refreshTheme = useCallback(async () => {
        const bgcol = getAnInformationSync("bgcol");
        const app_color = getAnInformationSync("app_color") ;
        const text_color = getAnInformationSync("text_color");

        setTheme({
            bgcol,
            app_color,
            text_color,
        });
    }, []);

    useEffect(() => {
        refreshTheme();
    }, [sessionId]);

    return (
        <ThemeContext.Provider value={{ ...theme, refreshTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

export function useTheme() {
    const context = useContext(ThemeContext);
    if (context === undefined) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
}







// loading context



interface LoadingContextType {
    showLoading: (message?: string) => void;
    hideLoading: () => void;
    withLoading: <T>(fn: () => Promise<T>, message?: string) => Promise<T>;
}

const LoadingContext = createContext<LoadingContextType | undefined>(undefined);

export function LoadingProvider({ children }: { children: ReactNode }) {
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState('Chargement...');
    const {app_color} = useTheme();

    const showLoading = (msg: string = 'Chargement...') => {
        setMessage(msg);
        setIsLoading(true);
    };

    const hideLoading = () => {
        setIsLoading(false);
    };

    const withLoading = async <T,>(
        fn: () => Promise<T>, 
        msg: string = 'Chargement...'
    ): Promise<T> => {
        try {
            showLoading(msg);
            const result = await fn();
            return result;
        } catch (error) {
            throw error;
        } finally {
            hideLoading();
        }
    };

    return (
        <LoadingContext.Provider value={{ showLoading, hideLoading, withLoading }}>
            {children}
            <LoadingOverlay app_color={app_color} visible={isLoading} message={message} />
        </LoadingContext.Provider>
    );
}

export function useGlobalLoading() {
    const context = useContext(LoadingContext);
    if (!context) {
        throw new Error('useGlobalLoading must be used within LoadingProvider');
    }
    return context;
}