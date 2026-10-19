/**
 * Secrets (auth token) go to the OS keychain/keystore via expo-secure-store.
 * Web has no secure store: falls back to sessionStorage (cleared when the tab closes).
 * Never use AsyncStorage for tokens: it is unencrypted.
 */
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

const options: SecureStore.SecureStoreOptions = {
  keychainAccessible: SecureStore.WHEN_UNLOCKED_THIS_DEVICE_ONLY, // not restored from backups
};

export async function getSecure(key: string): Promise<string | null> {
  if (Platform.OS === 'web') return globalThis.sessionStorage?.getItem(key) ?? null;
  return SecureStore.getItemAsync(key, options);
}

export async function setSecure(key: string, value: string | null): Promise<void> {
  if (Platform.OS === 'web') {
    if (value === null) globalThis.sessionStorage?.removeItem(key);
    else globalThis.sessionStorage?.setItem(key, value);
    return;
  }
  if (value === null) await SecureStore.deleteItemAsync(key, options);
  else await SecureStore.setItemAsync(key, value, options);
}
