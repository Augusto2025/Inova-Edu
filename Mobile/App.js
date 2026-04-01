// importe de navegação
// instalação do react navigation: npm install @react-navigation/native
// instalação do stack navigator: npm install @react-navigation/native-stack
// instalação de dependências: npm install react-native-screens react-native-safe-area-context
// instalação via Expo: npx expo install react-native-screens react-native-safe-area-context
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

// importando telas
import LoginScreen from './src/screens/Login';
// import HomeScreen from './src/screens/Home';
import SplashScreen from './src/screens/SplashScreen';

// criando o stack de navegação (pilha de telas)
const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>

      {/* stack navigator, usando screenOptions para ocultar o cabeçalho */}
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Splash" component={SplashScreen}/>
        <Stack.Screen name="Login" component={LoginScreen}/>
        {/* <Stack.Screen name="Home" component={HomeScreen}/> */}

      </Stack.Navigator>
    
    </NavigationContainer>
  );
}