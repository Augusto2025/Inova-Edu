import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from "../components/Cores";

// telas
import HomeScreen from '../screens/HomeScreen';
import CalendarScreen from '../screens/Eventos';
import ForumScreen from '../screens/Forum';
import SettingsScreen from '../screens/SettingsScreen';
import CursosScreen from '../screens/Cursos';
import TurmasScreen from '../screens/Turmas';
import ProjetosScreen from '../screens/Projetos';
import RepositorioScreen from '../screens/Repositorio';
import TituloScreen from '../screens/Topico';
import ConversaScreen from '../screens/Conversa';
import NotificationScreen from "../screens/NotificationScreen";
import ProfileScreen from '../screens/Perfil';


const Tab = createBottomTabNavigator();

export default function TabRoutes() {
  return (
    <Tab.Navigator
      // 🆕 Garante que, ao entrar no "Main" (logo após o login), a tela inicial seja a Home,
      // independente da ordem em que as abas aparecem na barra abaixo.
      initialRouteName="Home"
      backBehavior="history"
      screenOptions={({ route }) => ({
        headerShown: false,

        tabBarIcon: ({ color, size, focused }) => {
          let iconName = 'home';

          if (route.name === 'Home') iconName = 'home';
          else if (route.name === 'Eventos') iconName = 'calendar';
          else if (route.name === 'Fórum') iconName = 'chatbubble';
          else if (route.name === 'Repositório') iconName = 'folder';
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
          backgroundColor: COLORS.primary,
          height: 95,
        },

        tabBarLabelStyle: {
          fontSize: 12,
          marginTop: 5,
        },
      })}
    >
      {/* Visíveis */}
      <Tab.Screen name="Eventos" component={CalendarScreen} />
      <Tab.Screen name="Fórum" component={ForumScreen} />
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Repositório" component={CursosScreen} />
      <Tab.Screen name="Config" component={SettingsScreen} />

      {/* Ocultas */}
      <Tab.Screen 
        name="Perfil" 
        component={ProfileScreen}
        options={{
            tabBarItemStyle: {
              display: 'none',
            },
          }}
      />
      <Tab.Screen
        name="Turmas"
        component={TurmasScreen}
        options={{
          tabBarItemStyle: {
            display: 'none',
          },
        }}
      />
      
      <Tab.Screen
        name="Notifications"
        component={NotificationScreen}
        options={{
          tabBarItemStyle: {
            display: 'none',
          },
        }}
      />


      <Tab.Screen
        name="Projetos"
        component={ProjetosScreen}
        options={{
          tabBarItemStyle: {
            display: 'none',
          },
        }}
      />

      <Tab.Screen
        name="Repositorio"
        component={RepositorioScreen}
        options={{
          tabBarItemStyle: {
            display: 'none',
          },
        }}
      />

      <Tab.Screen
        name="Titulo"
        component={TituloScreen}
        options={{
          tabBarItemStyle: {
            display: 'none',
          },
        }}
      />

      <Tab.Screen
        name="Conversa"
        component={ConversaScreen}
        options={{
          tabBarItemStyle: {
            display: 'none',
          },
        }}
      />
    </Tab.Navigator>
  );
}
