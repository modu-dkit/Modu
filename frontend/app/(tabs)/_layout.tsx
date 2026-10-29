import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, text } from '../../src/theme';

type IconName = keyof typeof Ionicons.glyphMap;

const tabs: { name: string; title: string; icon: IconName; activeIcon: IconName }[] = [
  { name: 'home', title: 'Home', icon: 'home-outline', activeIcon: 'home' },
  { name: 'search', title: 'Search', icon: 'search-outline', activeIcon: 'search' },
  { name: 'dressing-room', title: 'Dressing Room', icon: 'shirt-outline', activeIcon: 'shirt' },
  { name: 'profile', title: 'Profile', icon: 'person-outline', activeIcon: 'person' },
];

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: colors.textPrimary,
        tabBarInactiveTintColor: colors.textSecondary,
        tabBarLabelStyle: { ...text.tabLabel, fontSize: 10 },
        tabBarStyle: { backgroundColor: colors.surface, borderTopColor: colors.separator },
        sceneStyle: { backgroundColor: colors.bg },
      }}
    >
      {tabs.map(tab => (
        <Tabs.Screen
          key={tab.name}
          name={tab.name}
          options={{
            title: tab.title,
            tabBarIcon: ({ color, size, focused }) => (
              <Ionicons name={focused ? tab.activeIcon : tab.icon} color={color as string} size={size} />
            ),
          }}
        />
      ))}
    </Tabs>
  );
}
