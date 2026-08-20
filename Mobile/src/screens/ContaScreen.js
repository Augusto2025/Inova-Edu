import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, TextInput } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';
import Header from '../components/Header';
import { useTheme } from '../context/ThemeContext';
import { useUser } from '../context/UserContext';
import { URL_BASE } from '../config/backend';

export default function ContaScreen({ navigation }) {
  const { theme, fontSizeScale } = useTheme();
  const { user } = useUser();
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [novaSenha, setNovaSenha] = useState('');
  const [confirmarSenha, setConfirmarSenha] = useState('');
  const [mostrarNovaSenha, setMostrarNovaSenha] = useState(false);
  const [mostrarConfirmacao, setMostrarConfirmacao] = useState(false);

  useEffect(() => {
    const carregarDados = async () => {
      try {
        const emailSalvo = await AsyncStorage.getItem('lembrar_email');
        const senhaSalva = await AsyncStorage.getItem('lembrar_senha');

        if (emailSalvo) {
          setEmail(emailSalvo);
        } else if (user?.email) {
          setEmail(user.email);
        }

        if (senhaSalva) {
          setSenha(senhaSalva);
        } else if (user?.senha) {
          setSenha(user.senha);
        }
      } catch (error) {
        console.warn('Erro ao carregar dados da conta:', error);
      }
    };

    carregarDados();
  }, [user?.email, user?.senha]);

  const salvarNovaSenha = async () => {
    if (!email.trim()) {
      Alert.alert('Erro', 'E-mail não encontrado.');
      return;
    }

    if (!novaSenha.trim() || !confirmarSenha.trim()) {
      Alert.alert('Erro', 'Preencha a nova senha e a confirmação.');
      return;
    }

    if (novaSenha !== confirmarSenha) {
      Alert.alert('Erro', 'As senhas não conferem.');
      return;
    }

    try {
      const response = await fetch(`${URL_BASE}/login/recuperar-senha`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email.trim(),
          novaSenha: novaSenha.trim()
        })
      });

      const dados = await response.json();
      if (!response.ok || !dados.sucesso) {
        throw new Error(dados.mensagem || 'Não foi possível redefinir a senha.');
      }

      const senhaGerada = dados.mensagem?.match(/: (.+)$/)?.[1] || novaSenha.trim();
      setSenha(senhaGerada);
      await AsyncStorage.setItem('lembrar_senha', senhaGerada);
      setMostrarFormulario(false);
      setNovaSenha('');
      setConfirmarSenha('');

      Alert.alert('Sucesso', `Sua senha foi redefinida. Nova senha: ${senhaGerada}`);
    } catch (error) {
      Alert.alert('Erro', error.message || 'Não foi possível alterar a senha.');
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: theme.background }]}> 
      <Header nomeTela={"Conta"} temGoBack={true} />

      <View style={styles.content}>
        <View style={[styles.card, { backgroundColor: theme.card, borderColor: theme.border }] }>
          <Text style={[styles.label, { fontSize: 14 * fontSizeScale, color: theme.text }]}>Email</Text>
          <Text style={[styles.valueText, { color: theme.text, fontSize: 16 * fontSizeScale }]}>{email || user?.email || '—'}</Text>

          <Text style={[styles.label, { fontSize: 14 * fontSizeScale, color: theme.text, marginTop: 12 }]}>Senha</Text>
          <View style={styles.passwordWrap}>
            <Text style={[styles.valueText, { color: theme.text, fontSize: 16 * fontSizeScale, flex: 1 }]}
            >{mostrarSenha ? (senha || '********') : '********'}</Text>
            <TouchableOpacity onPress={() => setMostrarSenha(!mostrarSenha)} style={styles.eyeButton}>
              <Ionicons name={mostrarSenha ? 'eye-off' : 'eye'} size={20} color={theme.text} />
            </TouchableOpacity>
          </View>

          {!mostrarFormulario && (
            <TouchableOpacity style={styles.actionBtn} onPress={() => setMostrarFormulario(true)}>
              <Text style={styles.actionText}>Definir nova senha</Text>
            </TouchableOpacity>
          )}

          {mostrarFormulario && (
            <View style={styles.formContainer}>
              <Text style={[styles.label, { fontSize: 14 * fontSizeScale, color: theme.text, marginTop: 8 }]}>Nova senha</Text>
              <View style={[styles.inputWrap, { borderColor: theme.border, backgroundColor: theme.background }]}> 
                <TextInput
                  value={novaSenha}
                  onChangeText={setNovaSenha}
                  secureTextEntry={!mostrarNovaSenha}
                  placeholder="Digite a nova senha"
                  placeholderTextColor={theme.text + '80'}
                  style={[styles.inputText, { color: theme.text, fontSize: 16 * fontSizeScale, flex: 1 }]}
                />
                <TouchableOpacity onPress={() => setMostrarNovaSenha(!mostrarNovaSenha)} style={styles.eyeButton}>
                  <Ionicons name={mostrarNovaSenha ? 'eye-off' : 'eye'} size={20} color={theme.text} />
                </TouchableOpacity>
              </View>

              <Text style={[styles.label, { fontSize: 14 * fontSizeScale, color: theme.text, marginTop: 12 }]}>Confirmar senha</Text>
              <View style={[styles.inputWrap, { borderColor: theme.border, backgroundColor: theme.background }]}> 
                <TextInput
                  value={confirmarSenha}
                  onChangeText={setConfirmarSenha}
                  secureTextEntry={!mostrarConfirmacao}
                  placeholder="Confirme a nova senha"
                  placeholderTextColor={theme.text + '80'}
                  style={[styles.inputText, { color: theme.text, fontSize: 16 * fontSizeScale, flex: 1 }]}
                />
                <TouchableOpacity onPress={() => setMostrarConfirmacao(!mostrarConfirmacao)} style={styles.eyeButton}>
                  <Ionicons name={mostrarConfirmacao ? 'eye-off' : 'eye'} size={20} color={theme.text} />
                </TouchableOpacity>
              </View>

              <TouchableOpacity style={styles.actionBtn} onPress={salvarNovaSenha}>
                <Text style={styles.actionText}>Salvar nova senha</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { padding: 16 },
  card: { borderRadius: 12, padding: 16, borderWidth: 1 },
  label: { opacity: 0.8 },
  passwordWrap: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 6,
  },
  valueText: {
    marginTop: 6,
    fontWeight: '500',
    paddingVertical: 10,
    paddingHorizontal: 12,
    borderWidth: 1,
    borderColor: '#D9D9D9',
    borderRadius: 10,
    backgroundColor: '#F5F5F5'
  },
  inputWrap: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 10,
    borderWidth: 1,
    marginTop: 6,
    paddingRight: 8,
  },
  inputText: {
    paddingHorizontal: 12,
    paddingVertical: 10,
  },
  eyeButton: {
    paddingHorizontal: 10,
    paddingVertical: 8,
  },
  actionBtn: { marginTop: 18, backgroundColor: '#0e68d6', paddingVertical: 10, borderRadius: 10, alignItems: 'center' },
  actionText: { color: '#fff', fontWeight: '700' },
  formContainer: { marginTop: 8 }
});
