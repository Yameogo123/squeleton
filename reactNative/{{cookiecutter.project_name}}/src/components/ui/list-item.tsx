import Ionicons from '@expo/vector-icons/Ionicons';
import type { ReactNode } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import { HitSize, Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { Text } from './text';

type Props = {
  title: string;
  subtitle?: string;
  icon?: keyof typeof Ionicons.glyphMap;
  left?: ReactNode;
  right?: ReactNode;
  destructive?: boolean;
  onPress?: () => void;
};

/** Row for settings / lists. Shows a chevron when pressable and no custom `right`. */
export function ListItem({ title, subtitle, icon, left, right, destructive, onPress }: Props) {
  const { colors } = useTheme();
  const tint = destructive ? colors.danger : colors.text;

  const content = (
    <>
      {left ?? (icon && <Ionicons name={icon} size={22} color={destructive ? colors.danger : colors.primaryText} />)}
      <View style={styles.body}>
        <Text variant="body" style={{ color: tint }} numberOfLines={1}>
          {title}
        </Text>
        {subtitle ? (
          <Text variant="caption" color="textSecondary" numberOfLines={1}>
            {subtitle}
          </Text>
        ) : null}
      </View>
      {right ?? (onPress && !destructive && <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />)}
    </>
  );

  // static row (e.g. holds a Switch): a plain View, so its children stay interactive for assistive tech
  if (!onPress) return <View style={styles.row}>{content}</View>;

  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={subtitle ? `${title}, ${subtitle}` : title}
      onPress={onPress}
      style={({ pressed }) => [styles.row, { backgroundColor: pressed ? colors.surfaceMuted : 'transparent' }]}>
      {content}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  row: { minHeight: HitSize + 12, flexDirection: 'row', alignItems: 'center', gap: Spacing.md, paddingHorizontal: Spacing.lg, paddingVertical: Spacing.sm },
  body: { flex: 1, gap: 2 },
});
