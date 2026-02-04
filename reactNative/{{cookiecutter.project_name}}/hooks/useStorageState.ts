import  { useEffect, useCallback, useReducer, useState } from 'react';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

type UseStateHook<T> = [[boolean, T | null], (value: T | null) => void];

function useAsyncState<T>(
  initialValue: [boolean, T | null] = [true, null],
): UseStateHook<T> {
  return useReducer(
    (state: [boolean, T | null], action: T | null = null): [boolean, T | null] => [false, action],
    initialValue
  ) as UseStateHook<T>;
}

export async function setStorageItemAsync(key: string, value: string | null) {
    if (Platform.OS === 'web') {
        try {
            if (value === null) {
                localStorage.removeItem(key);
            } else {
                localStorage.setItem(key, value);
            }
        } catch (e) {
            console.error('Local storage is unavailable:', e);
        }
    } else {
        if (value == null) {
            await SecureStore.deleteItemAsync(key);
        } else {
            await SecureStore.setItemAsync(key, value);
        }
    }
}


export async function getStorageItemAsync(key: string) {
    if (Platform.OS === 'web') {
        try {
            return localStorage.getItem(key);
        } catch (e) {
            console.error('Local storage is unavailable:', e);
            return ''
        }
    } else {
        return await SecureStore.getItemAsync(key);
    }
}


export function getStorageItem(key: string) {
    if (Platform.OS === 'web') {
        try {
            return localStorage.getItem(key);
        } catch (e) {
            console.error('Local storage is unavailable:', e);
            return ''
        }
    } else {
        return SecureStore.getItem(key);
    }
}

export function useStorageState(key: string): UseStateHook<string> {
    // Public
    const [state, setState] = useAsyncState<string>();

    // Get
    useEffect(() => {
        if (Platform.OS === 'web') {
            try {
                if (typeof localStorage !== 'undefined') {
                    setState(localStorage.getItem(key));
                }
            } catch (e) {
                console.error('Local storage is unavailable:', e);
            }
        } else {
            SecureStore.getItemAsync(key).then(value => {
                setState(value);
            });
        }
    }, [key]);

    // Set
    const setValue = useCallback(
        (value: string | null) => {
            setState(value);
            setStorageItemAsync(key, value);
        },
        [key]
    );

    return [state, setValue];
}


export function getSessionInfo(){
    const [state, setState] = useState({});

    // Get
    useEffect(() => {
        if (Platform.OS === 'web') {
            try {
                if (typeof localStorage !== 'undefined') {
                    const sessionData = localStorage.getItem("session");
                    setState(sessionData ? JSON.parse(sessionData) : {});
                }
            } catch (e) {
                //console.error('Local storage is unavailable:', e);
            }
        } else {
            SecureStore.getItemAsync("session").then(value => {
                setState(value ? JSON.parse(value) : {});
            });
        }
    }, []);

    return state;

}


export const BiometricStorage = {
    // Store phone number securely
    setStoredTel: async (tel: string) => {
        await SecureStore.setItemAsync('biometric_tel', tel);
    },

    getStoredTel: async (): Promise<string | null> => {
        return await SecureStore.getItemAsync('biometric_tel');
    },

    // Store password securely
    setStoredPwd: async (pwd: string) => {
        await SecureStore.setItemAsync('biometric_pwd', pwd);
    },

    getStoredPwd: async (): Promise<string | null> => {
        return await SecureStore.getItemAsync('biometric_pwd');
    },

    // Enable/disable biometric login
    setBiometricEnabled: async (enabled: boolean) => {
        await SecureStore.setItemAsync('biometric_enabled', JSON.stringify(enabled));
    },

    getBiometricEnabled: async (): Promise<boolean> => {
        const value = await SecureStore.getItemAsync('biometric_enabled');
        return value ? JSON.parse(value) : false;
    },

    // Clear all biometric data (for logout)
    clearBiometricData: async () => {
        await SecureStore.deleteItemAsync('biometric_tel');
        await SecureStore.deleteItemAsync('biometric_pwd');
        await SecureStore.deleteItemAsync('biometric_enabled');
    },
};