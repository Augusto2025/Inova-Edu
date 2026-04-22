import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

// telas
import HomeScreen from '../screens/HomeScreen';
import CalendarScreen from '../screens/Eventos';
import ForumScreen from '../screens/Forum';
import SettingsScreen from '../screens/SettingsScreen';
import CursosScreen from '../screens/Cursos';

const Tab = createBottomTabNavigator();

export default function TabRoutes() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,

        tabBarIcon: ({ color, size, focused }) => {
          let iconName = 'home';

          if (route.name === 'Home') iconName = 'home';
          else if (route.name === 'Calendario') iconName = 'calendar';
          else if (route.name === 'Forum') iconName = 'chatbubble';
          else if (route.name === 'Repositorio') iconName = 'folder';
          else if (route.name === 'Config') iconName = 'settings';

          return (
            <Ionicons
              name={iconName}
              size={focused ? 30 : 24}
              color={color}
            />
          );
        },

        tabBarActiveTintColor: '#ffffff',
        tabBarInactiveTintColor: '#dcdcdc',

        tabBarStyle: {
          backgroundColor: '#1459b3',
          height: 85,
          borderTopLeftRadius: 20,
          borderTopRightRadius: 20,
          elevation: 10,
        },

        tabBarLabelStyle: {
          fontSize: 13,
          marginBottom: 8,
        },
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Calendario" component={CalendarScreen} />
      <Tab.Screen name="Forum" component={ForumScreen} />
      <Tab.Screen name="Repositorio" component={CursosScreen} />
      <Tab.Screen name="Config" component={SettingsScreen} />
    </Tab.Navigator>
  );
}