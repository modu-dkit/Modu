import { useEffect } from 'react';
import { Image, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import { colors } from '../src/theme';

const SPLASH_DURATION_MS = 2000;

export default function Splash() {
  useEffect(() => {
    const timer = setTimeout(() => router.replace('/login'), SPLASH_DURATION_MS);
    return () => clearTimeout(timer);
  }, []);

  return (
    <View style={styles.container}>
      <Image source={require('../assets/images/splash.jpg')} style={styles.image} resizeMode="cover" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.surface },
  image: { width: '100%', height: '100%' },
});
