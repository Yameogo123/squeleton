import { DarkTheme, DefaultTheme, Stack, ThemeProvider } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { OfflineBanner } from '@/components/offline-banner';
import { SessionProvider, useSession } from '@/context/session';
import { useTheme } from '@/hooks/use-theme';

void SplashScreen.preventAutoHideAsync();

function RootNavigator() {
  const { session, isLoading } = useSession();
  const { colors, dark } = useTheme();

  // keep the native splash until we know whether the user is logged in (no auth screen flash)
  useEffect(() => {
    if (!isLoading) void SplashScreen.hideAsync();
  }, [isLoading]);

  if (isLoading) return null;

  const base = dark ? DarkTheme : DefaultTheme;
  const navigationTheme = {
    ...base,
    colors: { ...base.colors, primary: colors.primary, background: colors.background, card: colors.surface, text: colors.text, border: colors.border },
  };

  return (
    <ThemeProvider value={navigationTheme}>
      <Stack screenOptions={{ headerShown: false, animation: 'fade' }}>
        {/* routes are only reachable when the guard is true: no manual redirects needed */}
        <Stack.Protected guard={!!session}>
          <Stack.Screen name="(tabs)" />
        </Stack.Protected>
        {/* first screen = where logged-out users land */}
        <Stack.Protected guard={!session}>
          <Stack.Screen name="login" />
          <Stack.Screen name="signup" options={{ animation: 'slide_from_right' }} />
        </Stack.Protected>
      </Stack>
      <OfflineBanner />
      <StatusBar style={dark ? 'light' : 'dark'} />
    </ThemeProvider>
  );
}

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <SessionProvider>
        <RootNavigator />
      </SessionProvider>
    </SafeAreaProvider>
  );
}
