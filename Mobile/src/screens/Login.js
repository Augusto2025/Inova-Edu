import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Alert, Image, TouchableOpacity } from 'react-native';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view';
import { Ionicons } from '@expo/vector-icons';
import CustomButton from '../components/CustomButton';
import CustomInput from '../components/CustomInput';
import SplashScreen from './SplashScreen';
import { API_ENDPOINTS } from '../services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

const URL_BACKEND = API_ENDPOINTS.login;

export default function LoginScreen({ navigation }) {
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const [carregandoTransicao, setCarregandoTransicao] = useState(false);
    const [tipoSelecionado, setTipoSelecionado] = useState(null);
    const [lembrarDeMim, setLembrarDeMim] = useState(false); // 🆕 Estado para o Checkbox

    const Logo = require('../../assets/LOGOBRANCO.png');

    // ==========================================
    // 1. CARREGAR DADOS SALVOS AO ABRIR A TELA
    // ==========================================
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

    // ==========================================
    // 2. EXECUTAR LOGIN E TRATAR SALVAMENTO
    // ==========================================
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
            // --- Lógica de Salvar / Limpar "Lembrar de Mim" ---
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

            // Envia os dados para o seu servidor
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

                        {/* Seletor Aluno / Professor */}
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
                            secureTextEntry
                        />

                        {/* 🆕 Opção "Lembrar de mim" */}
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

                        <CustomButton title="Entrar" onPress={handleLogin}/>
                    </View>
                </View>
            </KeyboardAwareScrollView>

            {carregandoTransicao && <SplashScreen />}
        </View>
    );
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
    header: {
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
        paddingTop: '12%',
        paddingHorizontal: '8%', // Usamos horizontal para dar margem igual dos dois lados
        alignItems: 'stretch',   // 🌟 Força todos os elementos a esticarem na mesma largura
    },
    titulo: {
        color: '#1459b3',
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
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
        width: '100%', // 🌟 Mesma largura dos inputs
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
        marginBottom: 18,
        alignSelf: 'flex-start', // Alinha a caixinha à esquerda no limite do campo
    },
    lembrarText: {
        marginLeft: 8,
        color: '#64748B',
        fontSize: 14,
        fontWeight: '600',
    },
});