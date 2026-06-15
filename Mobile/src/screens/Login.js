import { useState } from 'react';
import { View, Text, TextInput, StyleSheet, Alert } from 'react-native';
import { Image } from 'react-native';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view';
import CustomButton from '../components/CustomButton';
import CustomInput from '../components/CustomInput';
import SplashScreen from './SplashScreen';

// npm install react-native-keyboard-aware-scroll-view

export default function LoginScreen({ navigation }) {
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const [carregandoTransicao, setCarregandoTransicao] = useState(false);
    const Logo = require('../../assets/LOGOBRANCO.png');

    // 🌟 Transformada em async para poder realizar a requisição HTTP
    const handleLogin = async () => {
        if (email === '' || senha === '') {
            Alert.alert('Erro', 'Por favor, preencha todos os campos.');
            return;
        }

        if (!email.includes('@') || !email.includes('.')) {
            Alert.alert('Erro', 'Por favor, insira um email válido.');
            return;
        }

        // Substitua pela URL gerada pelo seu deploy no Render quando ele estiver pronto!
        // Adeus IP local! Agora o seu app aponta para a internet real:
        const URL_BACKEND = process.env.URL_BACKEND;

        try {
            // Envia os dados para o seu servidor
            const resposta = await fetch(URL_BACKEND, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email.trim(), // Remove espaços em branco bobos
                    senha: senha,
                }),
            });

            const dados = await resposta.json();

            if (dados.sucesso) {
                // Se o banco validou, avança para a Main passando os dados obtidos (opcional)
                setCarregandoTransicao(true);

                // 2. Segura o usuário por 1.2 segundos para ele ver o "Carregando..."
                setTimeout(() => {
                    // 3. Só depois do tempo, joga ele para a tela principal
                    navigation.replace('Main', { usuario: dados.usuario });
                }, 1200); // 1200 milissegundos bate com o tempo da sua Splash!
            } else {
                // Alerta com a mensagem de erro vinda do seu banco de dados
                Alert.alert('Erro de Login', dados.mensagem);
            }

        } catch (error) {
            console.error('Erro na conexão:', error);
            Alert.alert(
                'Erro de Rede', 
                'Não foi possível se comunicar com o servidor. Verifique a conexão com a internet.'
            );
        }
    };

    return (
        <View style={{ flex: 1 }}>
            
            <KeyboardAwareScrollView style={styles.tela} enableOnAndroid={true} extraScrollHeight={40}>
                <View style={styles.containerTotal}>
                    <View style={styles.header}>
                        <Image source={Logo} style={styles.Logo} />
                        <Text style={{ color: '#ffffff', fontSize: 20, fontWeight: 'bold' }}>Bem-Vindo ao Inova Edu</Text>
                    </View>
                    <View style={styles.containerCenter}>
                        <Text style={styles.titulo}>Login</Text>

                        <CustomInput
                            placeholder="Email"
                            value={email}
                            onChangeText={setEmail}
                            />
                        <CustomInput
                            placeholder="Senha"
                            value={senha}
                            onChangeText={setSenha}
                            // esconde o texto digitado, para proteger a senha do usuário
                            secureTextEntry
                            />

                        <CustomButton title="Entrar" onPress={handleLogin}/>
                    </View>
                </View>
            </KeyboardAwareScrollView>

            {carregandoTransicao && <SplashScreen />}
        </View>
    )
}

const paddingHeader = 90;
const borderRadius = 40;

const styles = StyleSheet.create({
    Logo: {
        width: 150,
        height: 150,
    },
    tela: {
        backgroundColor: '#1459b3',
    },
    header:{
        width: '100%',
        paddingBottom: paddingHeader,
        paddingTop: paddingHeader,
        justifyContent: 'center',
        alignItems: 'center',
    },
    containerCenter: {
        borderTopRightRadius: borderRadius,
        borderTopLeftRadius: borderRadius,
        backgroundColor: '#fafafa',
        height: '100%',
        width: '100%',
        alignItems: 'flex-start',
        paddingTop: '25%',
        paddingLeft: '10%',
    },
    titulo: {
        color: '#1459b3',
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
    },
});