/**
 * Design tokens: the ONLY place for colors, spacing, radius and type scale.
 * Screens/components must read them through `useTheme()` — no hard-coded hex values.
 * Contrast: text/background pairs meet WCAG AA (4.5:1) in both schemes — check new pairs before adding them
 * (onPrimary on primary, primaryText/textMuted on background & surface).
 */
import { Platform } from 'react-native';

const brand = '#6A52ED';

export const Colors = {
  light: {
    primary: brand,
    /** accent used as TEXT (links, ghost buttons, active tab): AA on background */
    primaryText: brand,
    onPrimary: '#FFFFFF',
    primarySoft: '#EEEBFD',
    background: '#F7F7FA',
    surface: '#FFFFFF',
    surfaceMuted: '#F0F0F4',
    border: '#E3E3EA',
    text: '#14141A',
    textSecondary: '#5E5E6E',
    textMuted: '#6E6E7D',
    danger: '#D93636',
    dangerSoft: '#FDECEC',
    success: '#1F9D55',
    tabInactive: '#6E6E7D',
  },
  dark: {
    primary: '#6E5AF0',
    primaryText: '#9C8CF5',
    onPrimary: '#FFFFFF',
    primarySoft: '#26213F',
    background: '#0B0B10',
    surface: '#16161D',
    surfaceMuted: '#1F1F28',
    border: '#2A2A35',
    text: '#F4F4F7',
    textSecondary: '#B4B4C2',
    textMuted: '#80808F',
    danger: '#FF6B6B',
    dangerSoft: '#3A1D1F',
    success: '#4ADE80',
    tabInactive: '#80808F',
  },
} as const;

export type ThemeColors = { [K in keyof typeof Colors.light]: string };

/** 4pt grid */
export const Spacing = { xs: 4, sm: 8, md: 12, lg: 16, xl: 24, xxl: 32, xxxl: 48 } as const;

export const Radius = { sm: 8, md: 12, lg: 16, xl: 24, pill: 999 } as const;

export const Typography = {
  title: { fontSize: 28, lineHeight: 34, fontWeight: '700' },
  heading: { fontSize: 20, lineHeight: 26, fontWeight: '600' },
  body: { fontSize: 16, lineHeight: 24, fontWeight: '400' },
  bodyStrong: { fontSize: 16, lineHeight: 24, fontWeight: '600' },
  caption: { fontSize: 13, lineHeight: 18, fontWeight: '400' },
  label: { fontSize: 14, lineHeight: 20, fontWeight: '500' },
} as const;

/** Minimum touch target (Apple HIG 44pt / Material 48dp) */
export const HitSize = Platform.select({ android: 48, default: 44 });

export const MaxContentWidth = 560;
