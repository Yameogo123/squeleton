import { useEffect, useState, useRef } from 'react';
import { AppState, AppStateStatus } from 'react-native';
//import { useBiometricAuth } from './useBiometric';

export const usePrivacyScreen = () => {
    const [showPrivacyScreen, setShowPrivacyScreen] = useState(false);
    const [isLocked, setIsLocked] = useState(false);
    const appState = useRef(AppState.currentState);
    //const { authenticate } = useBiometricAuth();

    useEffect(() => {
        const subscription = AppState.addEventListener('change', async (nextAppState: AppStateStatus) => {
            // App going to background
            if (
                appState.current === 'active' &&
                nextAppState.match(/inactive|background/)
            ) {
                //console.log('🔒 App going to background');
                setShowPrivacyScreen(true);
                setIsLocked(true);
            }

            // App coming to foreground - require authentication
            if (
                appState.current.match(/inactive|background/) &&
                nextAppState === 'active' &&
                isLocked
            ) {

                setShowPrivacyScreen(false);
                //console.log('🔓 App coming to foreground - requesting authentication');
                
                //const success = await authenticate('Authentifiez-vous pour continuer');
                
                // if (success) {
                //     setShowPrivacyScreen(false);
                //     setIsLocked(false);
                // } else {
                //     // Keep privacy screen if auth fails
                //     setShowPrivacyScreen(true);
                // }
            }

            appState.current = nextAppState;
        });

        return () => {
            subscription.remove();
        };
    }, [isLocked]);

    return { showPrivacyScreen, isLocked };
};