import { Text as RNText, type TextProps } from 'react-native';
import { Typography, type ThemeColors } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

type Props = TextProps & {
  variant?: keyof typeof Typography;
  color?: keyof ThemeColors;
};

/** Themed text: always use it instead of <Text> so dark mode and the type scale stay consistent. */
export function Text({ variant = 'body', color = 'text', style, ...rest }: Props) {
  const { colors } = useTheme();
  return <RNText maxFontSizeMultiplier={1.6} style={[Typography[variant], { color: colors[color] }, style]} {...rest} />;
}
