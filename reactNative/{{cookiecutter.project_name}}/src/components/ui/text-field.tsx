import Ionicons from '@expo/vector-icons/Ionicons';
import { useState, type ComponentRef, type Ref } from 'react';
import { Platform, Pressable, StyleSheet, TextInput, View, type TextInputProps, type TextStyle } from 'react-native';
import { HitSize, Radius, Spacing, Typography } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { Text } from './text';

export type TextFieldRef = ComponentRef<typeof TextInput>;

type Props = Omit<TextInputProps, 'ref'> & {
  ref?: Ref<TextFieldRef>;
  label: string;
  error?: string | null;
  icon?: keyof typeof Ionicons.glyphMap;
  /** shows an eye toggle */
  password?: boolean;
};

/** Labelled input with icon, inline error and password visibility toggle. */
export function TextField({ ref, label, error, icon, password = false, style, onFocus, onBlur, ...rest }: Props) {
  const { colors } = useTheme();
  const [focused, setFocused] = useState(false);
  const [hidden, setHidden] = useState(password);
  const borderColor = error ? colors.danger : focused ? colors.primary : colors.border;

  return (
    <View style={styles.wrapper}>
      <Text variant="label" color="textSecondary">
        {label}
      </Text>
      <View style={[styles.field, { backgroundColor: colors.surface, borderColor }]}>
        {icon && <Ionicons name={icon} size={20} color={focused ? colors.primaryText : colors.textMuted} />}
        <TextInput
          ref={ref}
          accessibilityLabel={label}
          placeholderTextColor={colors.textMuted}
          selectionColor={colors.primary}
          secureTextEntry={hidden}
          autoCorrect={!password}
          onFocus={(e) => {
            setFocused(true);
            onFocus?.(e);
          }}
          onBlur={(e) => {
            setFocused(false);
            onBlur?.(e);
          }}
          style={[styles.input, { color: colors.text }, style]}
          {...rest}
        />
        {password && (
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={hidden ? 'Afficher le mot de passe' : 'Masquer le mot de passe'}
            hitSlop={12}
            onPress={() => setHidden((h) => !h)}>
            <Ionicons name={hidden ? 'eye-outline' : 'eye-off-outline'} size={20} color={colors.textMuted} />
          </Pressable>
        )}
      </View>
      {error ? (
        <Text variant="caption" color="danger" accessibilityLiveRegion="polite">
          {error}
        </Text>
      ) : null}
    </View>
  );
}

// 'none' is valid CSS for react-native-web but missing from RN's TextStyle type
const webNoOutline = { outlineStyle: 'none' } as unknown as TextStyle;

const styles = StyleSheet.create({
  wrapper: { gap: Spacing.xs },
  field: {
    minHeight: HitSize + 8,
    borderWidth: 1.5,
    borderRadius: Radius.md,
    paddingHorizontal: Spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.sm,
  },
  // web: the field border already shows focus, drop the browser outline
  input: { flex: 1, ...Typography.body, paddingVertical: Spacing.md, backgroundColor: 'transparent', ...(Platform.OS === 'web' && webNoOutline) },
});
