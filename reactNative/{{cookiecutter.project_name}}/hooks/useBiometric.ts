import * as LocalAuthentication from 'expo-local-authentication';
import { Alert } from 'react-native';

export const useBiometricAuth = () => {
    // Check if device supports biometric authentication
    const checkBiometricSupport = async () => {
        const compatible = await LocalAuthentication.hasHardwareAsync();
        
        if (!compatible) {
            Alert.alert('Erreur', 'Votre appareil ne supporte pas l\'authentification biométrique');
            return false;
        }

        const enrolled = await LocalAuthentication.isEnrolledAsync();
        
        if (!enrolled) {
            Alert.alert(
                'Configuration requise',
                'Veuillez configurer Face ID ou Touch ID dans les paramètres de votre appareil'
            );
            return false;
        }

        return true;
    };

    // Get biometric type (Face ID, Touch ID, or other)
    const getBiometricType = async () => {
        const types = await LocalAuthentication.supportedAuthenticationTypesAsync();
        
        if (types.includes(LocalAuthentication.AuthenticationType.FACIAL_RECOGNITION)) {
            return 'Face ID';
        } else if (types.includes(LocalAuthentication.AuthenticationType.FINGERPRINT)) {
            return 'Touch ID';
        } else if (types.includes(LocalAuthentication.AuthenticationType.IRIS)) {
            return 'Iris';
        }
        return 'Biométrie';
    };

    // Authenticate user
    const authenticate = async (promptMessage?: string) => {
        const isSupported = await checkBiometricSupport();
        
        if (!isSupported) {
            return false;
        }

        try {
            const biometricType = await getBiometricType();
            
            const result = await LocalAuthentication.authenticateAsync({
                promptMessage: promptMessage || `Authentifiez-vous avec ${biometricType}`,
                fallbackLabel: 'Utiliser le code',
                cancelLabel: 'Annuler',
                disableDeviceFallback: true, // Allow PIN/password fallback
            });

            return result.success;
        } catch (error) {
            return false;
        }
    };

    return {
        checkBiometricSupport,
        getBiometricType,
        authenticate,
    };
};
