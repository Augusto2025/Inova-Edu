// importe de navegação
// instalação do react navigation: npm install @react-navigation/native
// instalação do stack navigator: npm install @react-navigation/native-stack
// instalação de dependências: npm install react-native-screens react-native-safe-area-context
// instalação via Expo: npx expo install react-native-screens react-native-safe-area-context
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator, Header } from '@react-navigation/stack';

// importando telas
import LoginScreen from './src/screens/Login';
import SplashScreen from './src/screens/SplashScreen';
import CalendarScreen from './src/screens/Eventos';
import forumScreen from './src/screens/forumScreen';
import HeaderForum from './src/components/HeaderForum';
import FooterForum from './src/components/FooterForum';
import ProfilePage from './src/screens/Perfil';
import CursosScreen from './src/screens/Cursos';

// criando o stack de navegação (pilha de telas)
const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>

      {/* stack navigator, usando screenOptions para ocultar o cabeçalho */}
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Cursos" component={CursosScreen}/>
        <Stack.Screen name="Profile" component={ProfilePage}/>
        <Stack.Screen name="Calendar" component={CalendarScreen}/>
        <Stack.Screen name="footerforum" component={FooterForum}/>  
        <Stack.Screen name="headerforum" component={HeaderForum}/>
        <Stack.Screen name="Splash" component={SplashScreen}/>
        <Stack.Screen name="Login" component={LoginScreen}/>
        <Stack.Screen name="Forum" component={forumScreen}/>
      </Stack.Navigator>
    
    </NavigationContainer>
  );
}