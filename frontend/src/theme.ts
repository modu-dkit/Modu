export const colors = {
  bg: '#F3F3F3',
  surface: '#FFFFFF',
  black: '#000000',

  textPrimary: '#1C1C1E',
  textSecondary: '#8E8E93',
  textTertiary: '#C7C7CC',
  textOnDark: '#FFFFFF',

  fillPrimary: '#2C2C2E',
  fillSecondary: '#E9E9EB',
  fillDisabled: '#9A9A9A',
  track: '#E5E5EA',
  separator: '#EDEDED',

  success: '#34C759',
  error: '#FF3B30',
  overlay: 'rgba(0, 0, 0, 0.35)',
} as const;

export const fonts = {
  regular: 'Inter_400Regular',
  semiBold: 'Inter_600SemiBold',
  bold: 'Inter_700Bold',
} as const;

export const text = {
  headingLarge: { fontFamily: fonts.bold, fontSize: 28 },
  headingSection: { fontFamily: fonts.semiBold, fontSize: 18 },
  body: { fontFamily: fonts.regular, fontSize: 14 },
  bodySemiBold: { fontFamily: fonts.semiBold, fontSize: 14 },
  caption: { fontFamily: fonts.regular, fontSize: 12 },
  productBrand: { fontFamily: fonts.semiBold, fontSize: 12 },
  productName: { fontFamily: fonts.regular, fontSize: 12 },
  productPrice: { fontFamily: fonts.semiBold, fontSize: 15 },
  tabLabel: { fontFamily: fonts.regular, fontSize: 8 },
} as const;

export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  xxl: 32,
} as const;

export const radius = {
  button: 8,
  row: 14,
  card: 16,
  sheet: 28,
  pill: 999,
} as const;

export const theme = { colors, fonts, text, spacing, radius };
export default theme;
