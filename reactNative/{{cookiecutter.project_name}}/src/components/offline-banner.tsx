import Ionicons from '@expo/vector-icons/Ionicons';
import { StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Spacing } from '@/constants/theme';
import { useOnline } from '@/hooks/use-online';
import { useTheme } from '@/hooks/use-theme';
import { Text } from './ui/text';

/** Non-blocking banner: the app stays usable offline (cached screens), the user is just informed. */
export function OfflineBanner() {
  const online = useOnline();
  const { colors } = useTheme();
  const { top } = useSafeAreaInsets();
  if (online !== false) return null;

  return (
    <View accessibilityRole="alert" style={[styles.banner, { paddingTop: top + Spacing.xs, backgroundColor: colors.danger }]}>
      <Ionicons name="cloud-offline-outline" size={16} color="#fff" />
      <Text variant="caption" style={styles.text}>
        Pas de connexion internet
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  banner: { position: 'absolute', top: 0, left: 0, right: 0, zIndex: 10, flexDirection: 'row', justifyContent: 'center', alignItems: 'center', gap: Spacing.xs, paddingBottom: Spacing.xs },
  text: { color: '#fff', fontWeight: '600' },
});
