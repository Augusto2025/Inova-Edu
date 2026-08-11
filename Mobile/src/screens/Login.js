import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Alert, Image, TouchableOpacity, useWindowDimensions } from 'react-native';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view';
import { Ionicons } from '@expo/vector-icons';
import CustomButton from '../components/CustomButton';
import CustomInput from '../components/CustomInput';
import SplashScreen from './SplashScreen';
import { API_ENDPOINTS } from '../services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

const URL_BACKEND = API_ENDPOINTS.login;
const URL_RECUPERAR_SENHA = `${URL_BACKEND.replace(/\/$/, '')}/recuperar-senha`;

export default function LoginScreen({ navigation }) {
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const [carregandoTransicao, setCarregandoTransicao] = useState(false);
    const [tipoSelecionado, setTipoSelecionado] = useState(null);
    const [lembrarDeMim, setLembrarDeMim] = useState(false);

    const { width, height } = useWindowDimensions();
    const logoSize = Math.min(140, Math.max(90, width * 0.32));
    const headerTopPadding = Math.max(36, Math.min(88, height * 0.12));
    const containerPaddingHorizontal = Math.max(16, Math.min(32, width * 0.08));

    const Logo = require('../../assets/LOGOBRANCO.png');

    useEffect(() => {
        carregarCredenciaisSalvas();
    }, []);

    const carregarCredenciaisSalvas = async () => {
        try {
            const emailSalvo = await AsyncStorage.getItem('lembrar_email');
            const senhaSalva = await AsyncStorage.getItem('lembrar_senha');
            const tipoSalvo = await AsyncStorage.getItem('lembrar_tipo');
            const estaLembrado = await AsyncStorage.getItem('lembrar_ativo');

            if (estaLembrado === 'true') {
                if (emailSalvo) setEmail(emailSalvo);
                if (senhaSalva) setSenha(senhaSalva);
                if (tipoSalvo) setTipoSelecionado(tipoSalvo);
                setLembrarDeMim(true);
            }
        } catch (error) {
            console.error('Erro ao carregar dados salvos:', error);
        }
    };

    const handleLogin = async () => {
        if (email === '' || senha === '') {
            Alert.alert('Erro', 'Por favor, preencha todos os campos.');
            return;
        }

        if (!email.includes('@') || !email.includes('.')) {
            Alert.alert('Erro', 'Por favor, insira um email válido.');
            return;
        }

        if (!tipoSelecionado) {
            Alert.alert('Erro', 'Selecione se você é Aluno ou Professor.');
            return;
        }

        try {
            if (lembrarDeMim) {
                await AsyncStorage.setItem('lembrar_email', email);
                await AsyncStorage.setItem('lembrar_senha', senha);
                await AsyncStorage.setItem('lembrar_tipo', tipoSelecionado);
                await AsyncStorage.setItem('lembrar_ativo', 'true');
            } else {
                await AsyncStorage.multiRemove([
                    'lembrar_email', 
                    'lembrar_senha', 
                    'lembrar_tipo', 
                    'lembrar_ativo'
                ]);
            }

            const resposta = await fetch(URL_BACKEND, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email.trim(),
                    senha: senha,
                    tipo: tipoSelecionado,
                }),
            });

            const dados = await resposta.json();

            if (dados.sucesso) {
                await AsyncStorage.setItem('idUsuario', dados.usuario.id.toString());
                await AsyncStorage.setItem('tipo', dados.usuario.tipo);
                
                setCarregandoTransicao(true);

                setTimeout(() => {
                    navigation.replace('Main', { usuario: dados.usuario });
                }, 1200); 
            } else {
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

    const handleForgotPassword = () => {
        Alert.prompt(
            'Recuperar senha',
            'Informe o e-mail cadastrado para receber as instruções.',
            [
                { text: 'Cancelar', style: 'cancel' },
                {
                    text: 'Enviar',
                    onPress: async (emailRecuperacao) => {
                        const emailLimpo = (emailRecuperacao || '').trim();
                        if (!emailLimpo) {
                            Alert.alert('Erro', 'Informe um e-mail válido.');
                            return;
                        }

                        try {
                            const resposta = await fetch(URL_RECUPERAR_SENHA, {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ email: emailLimpo })
                            });

                            const dados = await resposta.json();
                            Alert.alert(dados.sucesso ? 'Sucesso' : 'Erro', dados.mensagem || 'Não foi possível recuperar a senha.');
                        } catch (error) {
                            console.error('Erro ao recuperar senha:', error);
                            Alert.alert('Erro', 'Não foi possível enviar a recuperação no momento.');
                        }
                    }
                }
            ],
            'plain-text'
        );
    };

    return (
        <View style={{ flex: 1 }}>
            <KeyboardAwareScrollView
                style={styles.tela}
                contentContainerStyle={styles.scrollContent}
                enableOnAndroid={true}
                extraScrollHeight={80}
                keyboardOpeningTime={0}
                keyboardShouldPersistTaps="handled"
            >
                <View style={styles.containerTotal}>
                    <View style={[styles.header, { paddingTop: headerTopPadding, paddingBottom: headerTopPadding }]}> 
                        <Image source={Logo} style={[styles.Logo, { width: logoSize, height: logoSize }]} />
                        <Text style={[styles.headerText, { fontSize: Math.max(18, Math.min(24, width * 0.055)) }]}>Bem-Vindo ao Inova Edu</Text>
                    </View>
                    
                    <View style={[styles.containerCenter, { paddingTop: Math.max(18, height * 0.08), paddingHorizontal: containerPaddingHorizontal }]}> 
                        <Text style={styles.titulo}>Login</Text>

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
                            autoCapitalize="none"
                            keyboardType="email-address"
                            placeholderTextColor="#64748B"
                        />
                        
                        <CustomInput
                            placeholder="Senha"
                            value={senha}
                            onChangeText={setSenha}
                            secureTextEntry
                            placeholderTextColor="#64748B"
                        />

                        <TouchableOpacity 
                            style={styles.lembrarContainer} 
                            activeOpacity={0.8}
                            onPress={() => setLembrarDeMim(!lembrarDeMim)}
                        >
                            <Ionicons 
                                name={lembrarDeMim ? "checkbox" : "square-outline"} 
                                size={22} 
                                color={lembrarDeMim ? "#1459b3" : "#64748B"} 
                            />
                            <Text style={styles.lembrarText}>Lembrar de mim</Text>
                        </TouchableOpacity>

                        <TouchableOpacity activeOpacity={0.8} onPress={handleForgotPassword}>
                            <Text style={styles.forgotPasswordText}>Esqueci minha senha</Text>
                        </TouchableOpacity>

                        <CustomButton title="Entrar" onPress={handleLogin} style={styles.loginButton} />
                    </View>
                </View>
            </KeyboardAwareScrollView>

            {carregandoTransicao && <SplashScreen />}
        </View>
    );
}

const borderRadius = 40;

const styles = StyleSheet.create({
    Logo: {
        resizeMode: 'contain',
    },
    headerText: {
        color: '#ffffff',
        fontWeight: 'bold',
        textAlign: 'center',
        marginTop: 12,
    },
    tela: {
        backgroundColor: '#1459b3',
    },
    scrollContent: {
        flexGrow: 1,
    },
    containerTotal: {
        minHeight: '100%',
    },
    header: {
        width: '100%',
        justifyContent: 'center',
        alignItems: 'center',
    },
    containerCenter: {
        borderTopRightRadius: borderRadius,
        borderTopLeftRadius: borderRadius,
        backgroundColor: '#fafafa',
        width: '100%',
        flexGrow: 1,
        alignItems: 'center',
    },
    titulo: {
        color: '#1459b3',
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
        textAlign: 'center',
    },
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
    lembrarContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginTop: 6,
        marginBottom: 10,
        alignSelf: 'flex-start',
    },
    lembrarText: {
        marginLeft: 8,
        color: '#64748B',
        fontSize: 14,
        fontWeight: '600',
    },
    forgotPasswordText: {
        color: '#1459b3',
        fontSize: 14,
        fontWeight: '700',
        marginBottom: 16,
        alignSelf: 'center',
    },
    loginButton: {
        width: '100%',
        maxWidth: 420,
    },
});