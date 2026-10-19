import Ionicons from '@expo/vector-icons/Ionicons';
import { router } from 'expo-router';
import { Pressable, StyleSheet, View } from 'react-native';
import { Avatar } from '@/components/ui/avatar';
import { Card } from '@/components/ui/card';
import { Screen } from '@/components/ui/screen';
import { Text } from '@/components/ui/text';
import { Radius, Spacing } from '@/constants/theme';
import { useSession } from '@/context/session';
import { useTheme } from '@/hooks/use-theme';

const shortcuts = [
  { icon: 'chatbubbles', label: 'Messages', href: '/messages' },
  { icon: 'settings', label: 'Réglages', href: '/settings' },
] as const;

function greeting() {
  const hour = new Date().getHours();
  return hour < 18 ? 'Bonjour' : 'Bonsoir';
}

export default function HomeScreen() {
  const { session } = useSession();
  const { colors } = useTheme();
  const user = session?.user;

  return (
    <Screen edges={['top', 'left', 'right']}>
      <View style={styles.header}>
        <View style={styles.flex}>
          <Text color="textSecondary">{greeting()},</Text>
          <Text variant="title" accessibilityRole="header" numberOfLines={1}>
            {user?.prenom ?? 'Bienvenue'}
          </Text>
        </View>
        <Avatar name={`${user?.prenom ?? ''} ${user?.nom ?? ''}`} size={48} />
      </View>

      <Card style={{ backgroundColor: colors.primary, borderColor: colors.primary }}>
        <Text variant="heading" style={{ color: colors.onPrimary }}>
          Votre espace est prêt ✨
        </Text>
        <Text style={{ color: colors.onPrimary, opacity: 0.9 }}>Commencez à construire vos écrans dans src/app.</Text>
      </Card>

      <Text variant="heading">Raccourcis</Text>
      <View style={styles.grid}>
        {shortcuts.map((s) => (
          <Pressable
            key={s.href}
            accessibilityRole="button"
            accessibilityLabel={s.label}
            onPress={() => router.navigate(s.href)}
            style={({ pressed }) => [styles.tile, { backgroundColor: colors.surface, borderColor: colors.border, opacity: pressed ? 0.8 : 1 }]}>
            <View style={[styles.tileIcon, { backgroundColor: colors.primarySoft }]}>
              <Ionicons name={s.icon} size={22} color={colors.primaryText} />
            </View>
            <Text variant="bodyStrong">{s.label}</Text>
          </Pressable>
        ))}
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  header: { flexDirection: 'row', alignItems: 'center', gap: Spacing.md },
  flex: { flex: 1 },
  grid: { flexDirection: 'row', gap: Spacing.md },
  tile: { flex: 1, padding: Spacing.lg, borderRadius: Radius.lg, borderWidth: StyleSheet.hairlineWidth, gap: Spacing.md },
  tileIcon: { width: 44, height: 44, borderRadius: Radius.md, alignItems: 'center', justifyContent: 'center' },
});
