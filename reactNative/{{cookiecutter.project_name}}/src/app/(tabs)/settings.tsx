import Constants from 'expo-constants';
import { useState } from 'react';
import { Platform, StyleSheet, Switch, View } from 'react-native';
import { Avatar } from '@/components/ui/avatar';
import { Card } from '@/components/ui/card';
import { ListItem } from '@/components/ui/list-item';
import { Screen } from '@/components/ui/screen';
import { Text } from '@/components/ui/text';
import { Spacing } from '@/constants/theme';
import { useSession } from '@/context/session';
import { confirm } from '@/lib/dialog';
import { useTheme } from '@/hooks/use-theme';

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <View style={styles.section}>
      <Text variant="label" color="textSecondary" style={styles.sectionTitle}>
        {title.toUpperCase()}
      </Text>
      <Card style={styles.sectionCard}>{children}</Card>
    </View>
  );
}

export default function SettingsScreen() {
  const { session, signOut } = useSession();
  const { colors } = useTheme();
  const [notifications, setNotifications] = useState(true);
  const user = session?.user;

  async function confirmSignOut() {
    if (await confirm('Se déconnecter ?', 'Vous devrez vous reconnecter pour accéder à votre compte.', 'Se déconnecter', true)) {
      await signOut();
    }
  }

  return (
    <Screen edges={['top', 'left', 'right']}>
      <Text variant="title" accessibilityRole="header">
        Réglages
      </Text>

      <Card style={styles.profile}>
        <Avatar name={`${user?.prenom ?? ''} ${user?.nom ?? ''}`} size={56} />
        <View style={styles.flex}>
          <Text variant="heading" numberOfLines={1}>
            {user?.prenom} {user?.nom}
          </Text>
          <Text color="textSecondary" numberOfLines={1}>
            {user?.email}
          </Text>
        </View>
      </Card>

      <Section title="Compte">
        <ListItem icon="person-outline" title="Informations personnelles" onPress={() => {}} />
        <ListItem icon="lock-closed-outline" title="Mot de passe" onPress={() => {}} />
      </Section>

      <Section title="Préférences">
        <ListItem
          icon="notifications-outline"
          title="Notifications"
          right={
            <Switch
              accessibilityLabel="Notifications"
              value={notifications}
              onValueChange={setNotifications}
              trackColor={{ true: colors.primary, false: colors.border }}
              thumbColor="#FFFFFF"
              // react-native-web uses its own prop for the "on" thumb
              {...(Platform.OS === 'web' && { activeThumbColor: '#FFFFFF' })}
              ios_backgroundColor={colors.border}
            />
          }
        />
        <ListItem icon="moon-outline" title="Apparence" subtitle="Suit le réglage du système" />
      </Section>

      <Section title="Aide">
        <ListItem icon="help-circle-outline" title="Support" onPress={() => {}} />
        <ListItem icon="document-text-outline" title="Confidentialité" onPress={() => {}} />
      </Section>

      <Card style={styles.sectionCard}>
        <ListItem icon="log-out-outline" title="Se déconnecter" destructive onPress={confirmSignOut} />
      </Card>

      <Text variant="caption" color="textMuted" style={styles.version}>
        Version {Constants.expoConfig?.version}
      </Text>
    </Screen>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  profile: { flexDirection: 'row', alignItems: 'center', gap: Spacing.lg },
  section: { gap: Spacing.sm },
  sectionTitle: { marginLeft: Spacing.sm },
  sectionCard: { padding: 0, overflow: 'hidden', gap: 0 },
  version: { textAlign: 'center' },
});
