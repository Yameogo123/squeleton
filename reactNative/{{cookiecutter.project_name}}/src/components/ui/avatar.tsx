import { StyleSheet, View } from 'react-native';
import { useTheme } from '@/hooks/use-theme';
import { Text } from './text';

export function Avatar({ name, size = 44 }: { name: string; size?: number }) {
  const { colors } = useTheme();
  const initials = name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('');

  return (
    <View
      accessible={false}
      style={[styles.avatar, { width: size, height: size, borderRadius: size / 2, backgroundColor: colors.primarySoft }]}>
      <Text variant="bodyStrong" style={{ color: colors.primaryText, fontSize: size * 0.38 }}>
        {initials || '?'}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({ avatar: { alignItems: 'center', justifyContent: 'center' } });
