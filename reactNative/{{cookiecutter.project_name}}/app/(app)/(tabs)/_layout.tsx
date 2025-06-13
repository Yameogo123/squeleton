import { Tabs } from 'expo-router';
import React from 'react';
import { Platform } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import { StatusBar } from 'react-native';
import { app_color } from '@/assets/constantes/constante';

export default function TabLayout() {

  const screenOptions = {
    tabBarActiveTintColor: app_color,
    headerShown: false, //tabBarButton: HapticTab,
    //tabBarBackground: TabBarBackground,
    tabBarStyle: Platform.select({ ios: { position: 'absolute' }, default: {} }),
  };

  const options = {
    title: 'home', tabBarIcon: ({ color }) => <Ionicons size={30} name="home" color={color} />,
  }

  return (
    <>
      <Tabs
        screenOptions={screenOptions}>
        <Tabs.Screen name="(home)"
          options={
            {
              title: 'home',
              tabBarIcon: ({ color }: { color: string }) => <Ionicons size={25} name="home" color={color} />,
            }
          }
        />
      </Tabs>
      <StatusBar barStyle="dark-content" translucent  />
    </>
  );
}
