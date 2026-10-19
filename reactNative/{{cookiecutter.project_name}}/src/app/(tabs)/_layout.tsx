import Ionicons from '@expo/vector-icons/Ionicons';
import * as Haptics from 'expo-haptics';
import { Tabs } from 'expo-router';
import { Platform, type ColorValue } from 'react-native';
import { useTheme } from '@/hooks/use-theme';

type IconName = keyof typeof Ionicons.glyphMap;

type TabIconProps = { name: string; color: ColorValue; focused: boolean; size: number };

/** filled icon when focused, outline otherwise (clear active state, not color only) */
function TabIcon({ name, color, focused, size }: TabIconProps) {
  return <Ionicons name={(focused ? name : `${name}-outline`) as IconName} size={size} color={color as string} />;
}

export default function TabLayout() {
  const { colors } = useTheme();

  return (
    <Tabs
      screenListeners={{ tabPress: () => void Haptics.selectionAsync() }}
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: colors.primaryText,
        tabBarInactiveTintColor: colors.tabInactive,
        // web has no bottom safe-area inset: give labels room
        tabBarStyle: { backgroundColor: colors.surface, borderTopColor: colors.border, ...(Platform.OS === 'web' && { height: 64, paddingBottom: 8 }) },
        tabBarHideOnKeyboard: Platform.OS === 'android',
      }}>
      <Tabs.Screen name="index" options={{ title: 'Accueil', tabBarIcon: (p) => <TabIcon name="home" {...p} />, tabBarAccessibilityLabel: 'Accueil' }} />
      <Tabs.Screen
        name="messages"
        options={{ title: 'Messages', tabBarIcon: (p) => <TabIcon name="chatbubbles" {...p} />, tabBarBadge: 2, tabBarAccessibilityLabel: 'Messages, 2 non lus' }}
      />
      <Tabs.Screen name="settings" options={{ title: 'Réglages', tabBarIcon: (p) => <TabIcon name="settings" {...p} />, tabBarAccessibilityLabel: 'Réglages' }} />
    </Tabs>
  );
}
