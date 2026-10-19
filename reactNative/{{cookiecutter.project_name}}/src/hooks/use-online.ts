import NetInfo from '@react-native-community/netinfo';
import { useEffect, useState } from 'react';

/** true / false once known, null while unknown (avoid flashing "offline" at startup). */
export function useOnline(): boolean | null {
  const [online, setOnline] = useState<boolean | null>(null);

  useEffect(
    () =>
      NetInfo.addEventListener((state) => {
        setOnline(state.isConnected === false ? false : state.isInternetReachable !== false);
      }),
    [],
  );

  return online;
}
