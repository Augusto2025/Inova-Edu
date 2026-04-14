import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

// TELAS
import LoginScreen from './src/screens/Login';
import SplashScreen from './src/screens/SplashScreen';

import ForumScreen from './src/screens/Forum'; 
import ConversaScreen from "./src/screens/Conversa";
import TituloScreen from "./src/screens/Titulo";

import ProfilePage from './src/screens/Perfil';
import CursosScreen from './src/screens/Cursos';
import TurmasScreen from './src/screens/Turmas';
import ProjetosScreen from './src/screens/Projetos';
import RepositorioScreen from './src/screens/Repositorio';

// STACK
const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Splash" component={SplashScreen}/>
        
        <Stack.Screen name="Titulo" component={TituloScreen} />
        <Stack.Screen name="Forum" component={ForumScreen}/>
        <Stack.Screen name="Conversa" component={ConversaScreen} />

        <Stack.Screen name="Repositorio" component={RepositorioScreen}/>
        <Stack.Screen name="Projetos" component={ProjetosScreen}/>
        <Stack.Screen name="Turmas" component={TurmasScreen}/>
        <Stack.Screen name="Cursos" component={CursosScreen}/>
        <Stack.Screen name="Profile" component={ProfilePage}/>
        <Stack.Screen name="Calendar" component={CalendarScreen}/>
        <Stack.Screen name="footerforum" component={FooterForum}/>  
        <Stack.Screen name="headerforum" component={HeaderForum}/>

        <Stack.Screen name="Splash" component={SplashScreen}/>
        <Stack.Screen name="Login" component={LoginScreen}/>

      </Stack.Navigator>
    </NavigationContainer>
  );
}