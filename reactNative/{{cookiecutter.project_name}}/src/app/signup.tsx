import Ionicons from '@expo/vector-icons/Ionicons';
import * as Haptics from 'expo-haptics';
import { router } from 'expo-router';
import { useRef, useState } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import { Button } from '@/components/ui/button';
import { Screen } from '@/components/ui/screen';
import { Text } from '@/components/ui/text';
import { TextField, type TextFieldRef } from '@/components/ui/text-field';
import { HitSize, Radius, Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { validateEmail, validatePassword, validatePhone, validateRequired } from '@/lib/validation';
import { ApiError } from '@/services/api';
import { signup, type SignupInput } from '@/services/auth';

type Field = keyof SignupInput;
type Errors = Partial<Record<Field | 'form', string | null>>;

export default function SignupScreen() {
  const { colors } = useTheme();
  const prenomRef = useRef<TextFieldRef>(null);
  const emailRef = useRef<TextFieldRef>(null);
  const telRef = useRef<TextFieldRef>(null);
  const passwordRef = useRef<TextFieldRef>(null);
  const [form, setForm] = useState<SignupInput>({ nom: '', prenom: '', email: '', tel: '', password: '' });
  const [errors, setErrors] = useState<Errors>({});
  const [loading, setLoading] = useState(false);

  const set = (field: Field) => (value: string) => {
    setForm((f) => ({ ...f, [field]: value }));
    if (errors[field]) setErrors((e) => ({ ...e, [field]: null }));
  };

  async function onSubmit() {
    const next: Errors = {
      nom: validateRequired(form.nom, 'Nom'),
      prenom: validateRequired(form.prenom, 'Prénom'),
      email: validateEmail(form.email),
      tel: validatePhone(form.tel ?? ''),
      password: validatePassword(form.password),
    };
    setErrors(next);
    if (Object.values(next).some(Boolean)) return void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);

    setLoading(true);
    try {
      await signup(form);
      void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      router.replace({ pathname: '/login', params: { email: form.email.trim(), created: '1' } });
    } catch (error) {
      setErrors({ form: error instanceof ApiError ? error.message : 'Inscription impossible' });
      void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Screen>
      <Pressable accessibilityRole="button" accessibilityLabel="Retour" hitSlop={12} onPress={() => router.back()} style={styles.back}>
        <Ionicons name="chevron-back" size={26} color={colors.text} />
      </Pressable>

      <View style={styles.header}>
        <Text variant="title" accessibilityRole="header">
          Créer un compte
        </Text>
        <Text color="textSecondary">Quelques informations pour commencer.</Text>
      </View>

      <View style={styles.form}>
        <View style={styles.row}>
          <View style={styles.flex}>
            <TextField label="Nom" value={form.nom} onChangeText={set('nom')} error={errors.nom} autoComplete="family-name" textContentType="familyName" returnKeyType="next" onSubmitEditing={() => prenomRef.current?.focus()} />
          </View>
          <View style={styles.flex}>
            <TextField ref={prenomRef} label="Prénom" value={form.prenom} onChangeText={set('prenom')} error={errors.prenom} autoComplete="given-name" textContentType="givenName" returnKeyType="next" onSubmitEditing={() => emailRef.current?.focus()} />
          </View>
        </View>
        <TextField ref={emailRef} label="Email" icon="mail-outline" value={form.email} onChangeText={set('email')} error={errors.email} keyboardType="email-address" autoCapitalize="none" autoComplete="email" textContentType="emailAddress" returnKeyType="next" onSubmitEditing={() => telRef.current?.focus()} />
        <TextField ref={telRef} label="Téléphone (optionnel)" icon="call-outline" value={form.tel} onChangeText={set('tel')} error={errors.tel} keyboardType="phone-pad" autoComplete="tel" textContentType="telephoneNumber" returnKeyType="next" onSubmitEditing={() => passwordRef.current?.focus()} />
        <TextField
          ref={passwordRef}
          label="Mot de passe"
          icon="lock-closed-outline"
          password
          value={form.password}
          onChangeText={set('password')}
          error={errors.password}
          autoComplete="new-password"
          textContentType="newPassword"
          returnKeyType="go"
          onSubmitEditing={onSubmit}
        />
        <Text variant="caption" color="textMuted">
          8 caractères min. avec majuscule, minuscule, chiffre et caractère spécial.
        </Text>
        {errors.form ? (
          <View style={[styles.formError, { backgroundColor: colors.dangerSoft }]} accessibilityRole="alert">
            <Ionicons name="alert-circle" size={18} color={colors.danger} />
            <Text variant="label" color="danger" style={styles.flex}>
              {errors.form}
            </Text>
          </View>
        ) : null}
        <Button title="Créer mon compte" loading={loading} onPress={onSubmit} />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  back: { width: HitSize, height: HitSize, justifyContent: 'center', marginLeft: -Spacing.sm },
  header: { gap: Spacing.sm, marginBottom: Spacing.sm },
  form: { gap: Spacing.lg },
  row: { flexDirection: 'row', gap: Spacing.md },
  flex: { flex: 1 },
  formError: { flexDirection: 'row', alignItems: 'center', gap: Spacing.sm, padding: Spacing.md, borderRadius: Radius.md },
});
