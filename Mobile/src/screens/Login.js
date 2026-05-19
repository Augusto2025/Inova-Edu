import { useState } from 'react';
import { View, Text, TextInput, StyleSheet, Alert } from 'react-native';
import { Image } from 'react-native';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view';
import CustomButton from '../components/CustomButton';
import CustomInput from '../components/CustomInput';

// npm install react-native-keyboard-aware-scroll-view

export default function LoginScreen({ navigation }) {
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const Logo = require('../../assets/LOGOBRANCO.png');

    const handleLogin = () => {
        if (email === '' || senha === '') {
            Alert.alert('Erro', 'Por favor, preencha todos os campos.');
            return;
        }

        if (!email.includes('@') || !email.includes('.')) {
            Alert.alert('Erro', 'Por favor, insira um email válido.');
            return;
        }

        // o replace é usado para substituir a tela atual, impedindo que o usuário volte para a tela de login usando o botão de voltar do dispositivo
        navigation.replace('Main');
    };

    return (
        <KeyboardAwareScrollView style={styles.tela} enableOnAndroid={true} extraScrollHeight={40}>
            <View style={styles.containerTotal}>
                <View style={styles.header}>
                    <Image source={Logo} />
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
    )
}

const paddingHeader = 90;
const borderRadius = 40;

const styles = StyleSheet.create({
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
})