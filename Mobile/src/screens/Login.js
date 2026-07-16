import { useState } from 'react';
import { View, Text, TextInput, StyleSheet, Alert } from 'react-native';
import { Image } from 'react-native';
import { TouchableOpacity } from 'react-native';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view';
import CustomButton from '../components/CustomButton';
import CustomInput from '../components/CustomInput';
import SplashScreen from './SplashScreen';
import { API_ENDPOINTS } from '../services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

// npm install react-native-keyboard-aware-scroll-view

// Substitua pela URL gerada pelo seu deploy no Render quando ele estiver pronto!
// Adeus IP local! Agora o seu app aponta para a internet real:
const URL_BACKEND = API_ENDPOINTS.login;

export default function LoginScreen({ navigation }) {
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const [carregandoTransicao, setCarregandoTransicao] = useState(false);
    // 🆕 Tipo escolhido na tela: 'Aluno' ou 'Professor'
    const [tipoSelecionado, setTipoSelecionado] = useState(null);
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

        // 🆕 Exige que a pessoa escolha se é Aluno ou Professor antes de entrar
        if (!tipoSelecionado) {
            Alert.alert('Erro', 'Selecione se você é Aluno ou Professor.');
            return;
        }

    
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
                    tipo: tipoSelecionado, // 🆕 Envia o tipo escolhido pra validação no backend
                }),
            });

            const dados = await resposta.json();

            if (dados.sucesso) {
                // ATENÇÃO AQUI: Salva o ID real do usuário no celular 
                // Convertemos para String porque o AsyncStorage só aceita texto.
                await AsyncStorage.setItem('idUsuario', dados.usuario.id.toString());
                await AsyncStorage.setItem('tipo', dados.usuario.tipo);
                // Se o banco validou, avança para a Main passando os dados obtidos (opcional)
                setCarregandoTransicao(true);

                // 2. Segura o usuário por 1.2 segundos para ele ver o "Carregando..."
                setTimeout(() => {
                    // 3. Só depois do tempo, joga ele para a tela principal
                    navigation.replace('Main', { usuario: dados.usuario });
                }, 1200); 
            } else {
                // Alerta com a mensagem de erro vinda do seu banco de dados
                // (inclui o caso de tipo selecionado não bater com o cadastrado)
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

                        {/* 🆕 Seletor Aluno / Professor */}
                        <Text style={styles.labelTipo}>Você é:</Text>
                        <View style={styles.tipoContainer}>
                            <TouchableOpacity
                                style={[
                                    styles.tipoBtn,
                                    tipoSelecionado === 'Aluno' && styles.tipoBtnAtivo,
                                ]}
                                activeOpacity={0.8}
                                onPress={() => setTipoSelecionado('Aluno')}
                            >
                                <Text
                                    style={[
                                        styles.tipoBtnText,
                                        tipoSelecionado === 'Aluno' && styles.tipoBtnTextAtivo,
                                    ]}
                                >
                                    Aluno
                                </Text>
                            </TouchableOpacity>

                            <TouchableOpacity
                                style={[
                                    styles.tipoBtn,
                                    tipoSelecionado === 'Professor' && styles.tipoBtnAtivo,
                                ]}
                                activeOpacity={0.8}
                                onPress={() => setTipoSelecionado('Professor')}
                            >
                                <Text
                                    style={[
                                        styles.tipoBtnText,
                                        tipoSelecionado === 'Professor' && styles.tipoBtnTextAtivo,
                                    ]}
                                >
                                    Professor
                                </Text>
                            </TouchableOpacity>
                        </View>

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
    // 🆕 Estilos do seletor Aluno / Professor
    labelTipo: {
        color: '#64748B',
        fontSize: 13,
        fontWeight: '600',
        marginBottom: 8,
    },
    tipoContainer: {
        flexDirection: 'row',
        gap: 10,
        marginBottom: 18,
        paddingRight: '10%',
        width: '100%',
    },
    tipoBtn: {
        flex: 1,
        paddingVertical: 12,
        borderRadius: 14,
        borderWidth: 1.5,
        borderColor: '#CBD5E1',
        alignItems: 'center',
        backgroundColor: '#fff',
    },
    tipoBtnAtivo: {
        backgroundColor: '#1459b3',
        borderColor: '#1459b3',
    },
    tipoBtnText: {
        color: '#64748B',
        fontWeight: '700',
        fontSize: 14,
    },
    tipoBtnTextAtivo: {
        color: '#fff',
    },
});