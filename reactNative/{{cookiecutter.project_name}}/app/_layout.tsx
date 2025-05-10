import React, { useEffect, useRef, useState } from "react";
import { SessionProvider } from '@/hooks/ctx';
import { Slot } from 'expo-router';
import Toast from 'react-native-toast-message';
import NetInfo from "@react-native-community/netinfo";
import NoInternet from "@/pages/security/noInternet";
import { StatusBar } from 'react-native';
import { useNotification } from "@/hooks/useNotification";

export default function Root() {
  // Set up the auth context and render our layout inside of it.

  const [connected, setConnected] = useState<boolean | null>(true);

  const notif = useNotification();

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setConnected(state.isConnected);
    });
  
    return () => {
      unsubscribe(); // cleanup
    };
  }, []);

  return (
    <SessionProvider>
      {connected ? <Slot /> : <NoInternet />}
      <StatusBar barStyle="dark-content" translucent />
      <Toast />
    </SessionProvider>
  );
}
