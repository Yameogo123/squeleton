import Ionicons from '@expo/vector-icons/Ionicons';
import * as Haptics from 'expo-haptics';
import { Link, useLocalSearchParams } from 'expo-router';
import { useRef, useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { Button } from '@/components/ui/button';
import { Screen } from '@/components/ui/screen';
import { Text } from '@/components/ui/text';
import { TextField, type TextFieldRef } from '@/components/ui/text-field';
import { Radius, Spacing } from '@/constants/theme';
import { useSession } from '@/context/session';
import { useTheme } from '@/hooks/use-theme';
import { validateEmail, validateRequired } from '@/lib/validation';
import { ApiError } from '@/services/api';
import { login } from '@/services/auth';

/** Login screen (first screen for anonymous users). */
export default function LoginScreen() {
  const { signIn } = useSession();
  const { colors } = useTheme();
  const passwordRef = useRef<TextFieldRef>(null);
  // coming back from sign-up: email pre-filled + confirmation banner
  const params = useLocalSearchParams<{ email?: string; created?: string }>();
  const [email, setEmail] = useState(params.email ?? '');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string | null; password?: string | null; form?: string }>({});
  const [loading, setLoading] = useState(false);

  async function onSubmit() {
    const next = { email: validateEmail(email), password: validateRequired(password, 'Mot de passe') };
    setErrors(next);
    if (next.email || next.password) return void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);

    setLoading(true);
    try {
      await signIn(await login(email, password));
      void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    } catch (error) {
      setErrors({ form: error instanceof ApiError ? error.message : 'Connexion impossible' });
      void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Screen>
      <View style={styles.header}>
        <View style={[styles.logo, { backgroundColor: colors.primarySoft }]}>
          <Ionicons name="sparkles" size={32} color={colors.primaryText} />
        </View>
        <Text variant="title" accessibilityRole="header">
          Bon retour 👋
        </Text>
        <Text color="textSecondary">Connectez-vous pour continuer.</Text>
      </View>

      <View style={styles.form}>
        {params.created ? (
          <View style={[styles.banner, { backgroundColor: colors.primarySoft }]} accessibilityRole="alert">
            <Ionicons name="checkmark-circle" size={18} color={colors.primaryText} />
            <Text variant="label" style={styles.flex}>
              Compte créé ! Connectez-vous.
            </Text>
          </View>
        ) : null}
        <TextField
          label="Email"
          icon="mail-outline"
          placeholder="vous@exemple.com"
          value={email}
          onChangeText={setEmail}
          error={errors.email}
          keyboardType="email-address"
          autoCapitalize="none"
          autoComplete="email"
          textContentType="emailAddress"
          returnKeyType="next"
          autoFocus={!params.email}
          onSubmitEditing={() => passwordRef.current?.focus()}
        />
        <TextField
          ref={passwordRef}
          label="Mot de passe"
          icon="lock-closed-outline"
          password
          placeholder="••••••••"
          value={password}
          onChangeText={setPassword}
          error={errors.password}
          autoComplete="current-password"
          textContentType="password"
          autoFocus={!!params.email}
          returnKeyType="go"
          onSubmitEditing={onSubmit}
        />
        {errors.form ? (
          <View style={[styles.formError, { backgroundColor: colors.dangerSoft }]} accessibilityRole="alert">
            <Ionicons name="alert-circle" size={18} color={colors.danger} />
            <Text variant="label" color="danger" style={styles.flex}>
              {errors.form}
            </Text>
          </View>
        ) : null}
        <Button title="Se connecter" loading={loading} onPress={onSubmit} />
      </View>

      <View style={styles.footer}>
        <Text color="textSecondary">Pas encore de compte ?</Text>
        <Link href="/signup" asChild>
          <Button title="Créer un compte" variant="ghost" />
        </Link>
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  header: { gap: Spacing.sm, marginTop: Spacing.xxl, marginBottom: Spacing.lg },
  logo: { width: 64, height: 64, borderRadius: Radius.lg, alignItems: 'center', justifyContent: 'center', marginBottom: Spacing.md },
  form: { gap: Spacing.lg },
  banner: { flexDirection: 'row', alignItems: 'center', gap: Spacing.sm, padding: Spacing.md, borderRadius: Radius.md },
  formError: { flexDirection: 'row', alignItems: 'center', gap: Spacing.sm, padding: Spacing.md, borderRadius: Radius.md },
  footer: { marginTop: 'auto', alignItems: 'center' },
  flex: { flex: 1 },
});
