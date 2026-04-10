import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

// telas
import HomeScreen from '../screens/HomeScreen';
import CalendarScreen from '../screens/Calendario';
import ForumScreen from '../screens/ForumScreen';
import SettingsScreen from '../screens/SettingsScreen';
import RepositorioScreen from '../screens/RepositorioScreen';

const Tab = createBottomTabNavigator();

export default function TabRoutes() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,

        // ícones
        tabBarIcon: ({ color, size, focused }) => {
            let iconName;

            if (route.name === 'Home') iconName = 'home';
            else if (route.name === 'Calendario') iconName = 'calendar';
            else if (route.name === 'Forum') iconName = 'chatbubble';
            else if (route.name === 'Repositorio') iconName = 'folder';
            else if (route.name === 'Config') iconName = 'settings';

            return (
                <Ionicons
                name={iconName}
                size={focused ? 30 : 24} // 👈 aumenta quando ativo
                color={color}
                />
            );
        },

        // cores
        tabBarActiveTintColor: '#ffffff',   // ícone ativo (branco)
        tabBarInactiveTintColor: '#dcdcdc', // ícone inativo (cinza claro)

        // estilo do menu
        tabBarStyle: {
          backgroundColor: '#1459b3', // azul 🔵
          height: 85,
          borderTopLeftRadius: 20,
          borderTopRightRadius: 20,
        //   position: 'absolute',

          // sombra Android
          elevation: 10,

          // sombra iOS
          shadowColor: '#000',
          shadowOpacity: 0.2,
          shadowRadius: 5,
        },

        tabBarLabelStyle: {
          fontSize: 13,
          marginBottom: 8,
          borderRadius: 15,
            margin: 5,
        },
        // tabBarActiveTintColor: '#ffffff',
        // tabBarInactiveTintColor: '#dcdcdc',
        // tabBarActiveBackgroundColor: '#0d47a1', // 👈 destaque do botão ativo
        
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Calendario" component={CalendarScreen} />
      <Tab.Screen name="Forum" component={ForumScreen} />
      <Tab.Screen name="Repositorio" component={RepositorioScreen} />
      <Tab.Screen name="Config" component={SettingsScreen} />
    </Tab.Navigator>
  );
}