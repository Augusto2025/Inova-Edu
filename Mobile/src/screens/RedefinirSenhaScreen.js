import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import Header from '../components/Header';
import { useTheme } from '../context/ThemeContext';
import { useUser } from '../context/UserContext';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { URL_BASE } from '../config/backend';

export default function RedefinirSenhaScreen({ navigation }) {
  const { theme, fontSizeScale } = useTheme();
  const { user } = useUser();
  const [email, setEmail] = useState('');
  const [novaSenha, setNovaSenha] = useState('');
  const [confirmarSenha, setConfirmarSenha] = useState('');
  const [mostrarNovaSenha, setMostrarNovaSenha] = useState(false);
  const [mostrarConfirmacao, setMostrarConfirmacao] = useState(false);

  useEffect(() => {
    const carregarEmail = async () => {
      try {
        const emailSalvo = await AsyncStorage.getItem('lembrar_email');
        setEmail(emailSalvo || user?.email || '');
      } catch (error) {
        console.warn('Erro ao carregar email para redefinição:', error);
      }
    };

    carregarEmail();
  }, [user?.email]);

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
      const response = await fetch(`${URL_BASE}/recuperar-senha`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.trim() })
      });

      const dados = await response.json();
      if (!response.ok || !dados.sucesso) {
        throw new Error(dados.mensagem || 'Não foi possível redefinir a senha.');
      }

      const senhaGerada = dados.mensagem?.match(/: (.+)$/)?.[1] || novaSenha;
      await AsyncStorage.setItem('lembrar_senha', senhaGerada);

      Alert.alert('Sucesso', `Sua senha foi redefinida. Nova senha: ${senhaGerada}`);
      navigation.goBack();
    } catch (error) {
      Alert.alert('Erro', error.message || 'Não foi possível alterar a senha.');
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: theme.background }]}> 
      <Header nomeTela={"Redefinir senha"} temGoBack={true} />

      <View style={styles.content}>
        <View style={[styles.card, { backgroundColor: theme.card, borderColor: theme.border }] }>
          <Text style={[styles.label, { fontSize: 14 * fontSizeScale, color: theme.text }]}>Email</Text>
          <TextInput
            value={email}
            editable={false}
            style={[styles.input, { color: theme.text, borderColor: theme.border, backgroundColor: theme.background, fontSize: 16 * fontSizeScale }]}
          />

          <Text style={[styles.label, { fontSize: 14 * fontSizeScale, color: theme.text, marginTop: 12 }]}>Nova senha</Text>
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
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { padding: 16 },
  card: { borderRadius: 12, padding: 16, borderWidth: 1 },
  label: { opacity: 0.8 },
  input: {
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    marginTop: 6,
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
  actionText: { color: '#fff', fontWeight: '700' }
});
