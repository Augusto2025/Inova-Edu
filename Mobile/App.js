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
<<<<<<< HEAD
import CalendarScreen from './src/screens/Calendario';
import forumScreen from './src/screens/forum';
// import HeaderForum from './src/components/HeaderForum';
// import FooterForum from './src/components/FooterForum';
import ConversaScreen from "./src/screens/Conversa";
import TituloScreen from "./src/screens/TituloForum";
=======
import CalendarScreen from './src/screens/Eventos';
import forumScreen from './src/screens/forumScreen';
import HeaderForum from './src/components/HeaderForum';
import FooterForum from './src/components/FooterForum';
import ProfilePage from './src/screens/Perfil';
import CursosScreen from './src/screens/Cursos';
import TurmasScreen from './src/screens/Turmas';
import ProjetosScreen from './src/screens/Projetos';
import RepositorioScreen from './src/screens/Repositorio';
>>>>>>> Deploys

// criando o stack de navegação (pilha de telas)
const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>

      {/* stack navigator, usando screenOptions para ocultar o cabeçalho */}
      <Stack.Navigator screenOptions={{ headerShown: false }}>
<<<<<<< HEAD
        <Stack.Screen name="Titulo" component={TituloScreen} />
        <Stack.Screen name="Forum" component={forumScreen}/>
        <Stack.Screen name="Conversa" component={ConversaScreen} />


=======
        <Stack.Screen name="Repositorio" component={RepositorioScreen}/>
        <Stack.Screen name="Projetos" component={ProjetosScreen}/>
        <Stack.Screen name="Turmas" component={TurmasScreen}/>
        <Stack.Screen name="Cursos" component={CursosScreen}/>
        <Stack.Screen name="Profile" component={ProfilePage}/>
>>>>>>> Deploys
        <Stack.Screen name="Calendar" component={CalendarScreen}/>
        {/* <Stack.Screen name="footerforum" component={FooterForum}/>   */}
        {/* <Stack.Screen name="headerforum" component={HeaderForum}/> */}
        <Stack.Screen name="Splash" component={SplashScreen}/>
        <Stack.Screen name="Login" component={LoginScreen}/>
<<<<<<< HEAD
        {/* <Stack.Screen name="Home" component={HomeScreen}/> */}

=======
        <Stack.Screen name="Forum" component={forumScreen}/>
>>>>>>> Deploys
      </Stack.Navigator>
    
    </NavigationContainer>
  );
}