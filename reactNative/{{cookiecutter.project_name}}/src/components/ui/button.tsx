import * as Haptics from 'expo-haptics';
import { ActivityIndicator, Pressable, StyleSheet, View, type PressableProps } from 'react-native';
import { HitSize, Radius, Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { Text } from './text';

type Props = Omit<PressableProps, 'children'> & {
  title: string;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  loading?: boolean;
  icon?: React.ReactNode;
};

export function Button({ title, variant = 'primary', loading = false, disabled, icon, onPress, style, ...rest }: Props) {
  const { colors } = useTheme();
  const isDisabled = disabled || loading;

  const palette = {
    primary: { bg: colors.primary, fg: colors.onPrimary, border: colors.primary },
    secondary: { bg: colors.surface, fg: colors.text, border: colors.border },
    ghost: { bg: 'transparent', fg: colors.primaryText, border: 'transparent' },
    danger: { bg: colors.dangerSoft, fg: colors.danger, border: colors.dangerSoft },
  }[variant];

  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={title}
      accessibilityState={{ disabled: !!isDisabled, busy: loading }}
      disabled={isDisabled}
      onPress={(e) => {
        void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        onPress?.(e);
      }}
      style={(state) => [
        styles.base,
        { backgroundColor: palette.bg, borderColor: palette.border, opacity: isDisabled ? 0.5 : state.pressed ? 0.85 : 1 },
        state.pressed && styles.pressed,
        typeof style === 'function' ? style(state) : style,
      ]}
      {...rest}>
      <View style={styles.content}>
        {loading ? <ActivityIndicator color={palette.fg} /> : icon}
        <Text variant="bodyStrong" style={{ color: palette.fg }}>
          {title}
        </Text>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: {
    minHeight: HitSize + 8,
    borderRadius: Radius.md,
    borderWidth: 1,
    paddingHorizontal: Spacing.xl,
    justifyContent: 'center',
  },
  pressed: { transform: [{ scale: 0.98 }] },
  content: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: Spacing.sm },
});
