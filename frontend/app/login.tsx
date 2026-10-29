import { Image, Pressable, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { colors, radius, spacing, text } from '../src/theme';

export default function Login() {
  const continueWithGoogle = () => {
    router.replace('/home');
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.logoArea}>
        <Image source={require('../assets/images/logo.png')} style={styles.logo} resizeMode="contain" />
      </View>

      <Text style={styles.tagline}>Your Style,{'\n'}Endless possibilities.</Text>

      <Pressable
        style={({ pressed }) => [styles.googleButton, pressed && styles.pressed]}
        onPress={continueWithGoogle}
        accessibilityRole="button"
      >
        <Image source={require('../assets/images/google.png')} style={styles.googleIcon} />
        <Text style={styles.googleLabel}>Continue with Google</Text>
      </Pressable>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.xxl * 3,
  },
  logoArea: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  logo: { width: 280, height: 280 },
  tagline: {
    ...text.headingLarge,
    color: colors.textPrimary,
    marginBottom: spacing.md,
  },
  googleButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    height: 48,
    borderRadius: radius.button,
    borderWidth: 1,
    borderColor: colors.textTertiary,
    backgroundColor: colors.surface,
  },
  pressed: { backgroundColor: colors.fillSecondary },
  googleIcon: { position: 'absolute', left: spacing.lg, width: 20, height: 20 },
  googleLabel: { ...text.body, color: colors.textPrimary },
});
