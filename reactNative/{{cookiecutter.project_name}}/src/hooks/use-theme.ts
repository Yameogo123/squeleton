import { useColorScheme } from 'react-native';
import { Colors, type ThemeColors } from '@/constants/theme';

export function useTheme(): { colors: ThemeColors; dark: boolean } {
  const dark = useColorScheme() === 'dark';
  return { colors: dark ? Colors.dark : Colors.light, dark };
}
