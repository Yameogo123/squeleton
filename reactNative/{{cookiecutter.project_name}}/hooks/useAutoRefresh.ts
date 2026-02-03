import { useEffect, useRef, useState } from 'react';
import { AppState } from 'react-native';
import { useRouter } from 'expo-router';
import moment from 'moment';

const TIMEOUT = 5 * 60 * 1000; // 5 minutes

export function useAutoRefresh(refresh: boolean, setRefresh: any) {
    const router = useRouter();
    const [appState, setAppState] = useState(AppState.currentState);
    const appStateRef = useRef(appState);
    const backgroundTime = useRef<moment.Moment | null>(null);

    const navigateToHome = async () => {
        try {
            setRefresh(true);
            //console.log('🔄 Navigating to home after 5 minutes of inactivity...');
            
            await new Promise((resolve) => setTimeout(resolve, 1500));
            
            router.replace('/');
            
            setRefresh(false);
        } catch (error) {
            //console.error('Error during navigation:', error);
            setRefresh(false);
        }
    };

    useEffect(() => {
        appStateRef.current = appState;
    }, [appState]);

    useEffect(() => {
        const sub = AppState.addEventListener("change", async (nextState) => {
            if (appStateRef.current === "active" && nextState.match(/inactive|background/)) {
                backgroundTime.current = moment();
                setRefresh(true);
                //console.log('📱 App went to background at:', backgroundTime.current.format());
            }

            if (appStateRef.current.match(/background|inactive/) && nextState === "active") {
                if (backgroundTime.current) {
                    const now = moment();
                    const diff = now.diff(backgroundTime.current, "milliseconds");
                    //console.log(`📱 App came to foreground. Was inactive for: ${diff}ms`);
                    
                    if (diff >= TIMEOUT) {
                        await navigateToHome();
                    } else {
                        setRefresh(false);
                    }
                } else {
                    setRefresh(false);
                }
            }

            setAppState(nextState);
        });

        return () => sub.remove();
    }, []);

    return { refresh };
}
