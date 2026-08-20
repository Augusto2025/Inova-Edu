import React, { useState, useContext, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Switch,
  TouchableOpacity,
  Image,
  Alert,
  Modal,
  TextInput,
  TouchableWithoutFeedback,
  Keyboard,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";
import Header from "../components/Header";
import { COLORS } from "../components/Cores"; 
import { ThemeContext } from "../context/ThemeContext";
import { useUser } from "../context/UserContext";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { URL_BASE } from '../config/backend';

// Importando o motor de voz do Expo
import * as Speech from 'expo-speech';

export default function ConfiguracoesScreen({ navigation }) {
  // Puxando os novos estados do controle de fonte global
  const { isDarkMode, toggleDarkMode, fontSizeScale, alterarTamanhoFonte, obterNomeTamanhoFonte } = useContext(ThemeContext);
  const { user } = useUser();
  const [avatarLoadFailed, setAvatarLoadFailed] = useState(false);
  const defaultAvatar = require('../../assets/default.png');

  const [push, setPush] = useState(false);

  const irParaPerfil = () => {
    navigation.navigate("Perfil");
  };

  const handleLogout = () => {
    Alert.alert(
      'Sair',
      'Deseja realmente sair do aplicativo?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Sair',
          style: 'destructive',
          onPress: () => doLogout()
        }
      ]
    );
  };

  const doLogout = async () => {
    try {
      console.log('Iniciando logout: limpando AsyncStorage');
      // tenta limpar chaves específicas e como fallback limpa tudo
      try {
        await AsyncStorage.multiRemove(['idUsuario', 'tipo']);
      } catch (e) {
        console.warn('multiRemove falhou, tentando clear():', e);
        await AsyncStorage.clear();
      }

      console.log('Logout: navegação para Login');
      navigation.reset({ index: 0, routes: [{ name: 'Login' }] });
      Alert.alert('Desconectado', 'Você saiu do aplicativo.');
    } catch (err) {
      console.error('Erro durante logout:', err);
      Alert.alert('Erro', 'Não foi possível sair. Tente novamente.');
    }
  };

  // --- Conta (modal) ---
  const [accountModalVisible, setAccountModalVisible] = useState(false);

  useEffect(() => {
    // Não precisa fazer fetch, pois o user já está no contexto
    // que é atualizado globalmente
  }, [user]);

  // Função que lê o resumo da tela em voz alta
  const executarTextoEmVozAlta = () => {
    const textoDoStatus = `Você está na tela de configurações. O seu Modo Escuro está ${isDarkMode ? 'Ativado' : 'Desativado'}. O tamanho atual da sua fonte é ${obterNomeTamanhoFonte()}.`;
    
    // Cancela qualquer voz ativa antes de falar para não encavalar o áudio
    Speech.stop(); 
    Speech.speak(textoDoStatus, { language: 'pt-BR', rate: 1.0 });
  };

  const CoresTema = {
    fundo: isDarkMode ? "#121212" : COLORS.backgroundCard,
    card: isDarkMode ? "#1E1E1E" : "#fff",
    textoPrincipal: isDarkMode ? "#E2E8F0" : "#333",
    textoSecundario: isDarkMode ? "#94A3B8" : "#777",
    borda: isDarkMode ? "#2D3748" : "#EEE",
  };

  const ItemSwitch = ({ icon, titulo, valor, funcao }) => (
    <View style={[styles.item, { borderBottomColor: CoresTema.borda }]}>
      <View style={styles.left}>
        <Ionicons name={icon} size={22} color={isDarkMode ? "#94A3B8" : "#444"} />
        {/* MULTIPLICADOR DE FONTE APLICADO AQUI */}
        <Text style={[styles.itemText, { color: CoresTema.textoPrincipal, fontSize: 16 * fontSizeScale }]}>
          {titulo}
        </Text>
      </View>
      <Switch
        value={valor}
        onValueChange={funcao}
        trackColor={{ false: '#CBD5E1', true: COLORS.primary }}
        thumbColor={'#FFFFFF'}
      />
    </View>
  );

  const ItemBotao = ({ icon, titulo, subInfo, onPress }) => (
    <TouchableOpacity style={[styles.item, { borderBottomColor: CoresTema.borda }]} onPress={onPress}>
      <View style={styles.left}>
        <Ionicons name={icon} size={22} color={isDarkMode ? "#94A3B8" : "#444"} />
        {/* MULTIPLICADOR DE FONTE APLICADO AQUI */}
        <Text style={[styles.itemText, { color: CoresTema.textoPrincipal, fontSize: 16 * fontSizeScale }]}>
          {titulo} {subInfo && <Text style={{color: COLORS.primary, fontWeight: 'bold'}}>({subInfo})</Text>}
        </Text>
      </View>
      <Ionicons name="chevron-forward" size={20} color={CoresTema.textoSecundario} />
    </TouchableOpacity>
  );

  return (
    <View style={[styles.container, { backgroundColor: CoresTema.fundo }]}>
      <Header nomeTela={"Configurações"} temGoBack={true} />

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 120 }}>
        <View style={styles.perfil}>
          <View style={[styles.avatarWrapper, { borderColor: COLORS.primary }]}>
            {user && user.imagem && user.imagem !== 'null' && user.imagem.trim() !== '' && !avatarLoadFailed ? (
              <Image source={{ uri: user.imagem }} style={styles.avatar} onError={() => setAvatarLoadFailed(true)} />
            ) : (
              <Image source={defaultAvatar} style={styles.avatar} />
            )}
          </View>
          <Text style={[styles.nome, { fontSize: 24 * fontSizeScale }]}>{user ? `${user.nome} ${user.sobrenome}`.trim() : 'Usuário'}</Text>
          <Text style={[styles.email, { color: CoresTema.textoSecundario, fontSize: 14 * fontSizeScale }]}>{user ? user.turma || user.descricao || '' : ''}</Text>

          <TouchableOpacity style={styles.perfilBtn} onPress={irParaPerfil}>
            <Text style={[styles.perfilBtnText, { fontSize: 14 * fontSizeScale }]}>Visualizar Perfil</Text>
          </TouchableOpacity>

          {/* Conta moved to the settings card below */}
        </View>

        {/* Notificações */}

        {/* Aparência e Acessibilidade */}
        <View style={[styles.card, { backgroundColor: CoresTema.card }]}>
          <ItemSwitch icon="notifications" titulo="Notificações Push" valor={push} funcao={setPush} />
          <ItemSwitch icon="moon" titulo="Modo Escuro" valor={isDarkMode} funcao={toggleDarkMode} />
          <ItemBotao 
            icon="text" 
            titulo="Tamanho da fonte" 
            subInfo={obterNomeTamanhoFonte()} 
            onPress={alterarTamanhoFonte} 
          />
          <ItemBotao
            icon="person"
            titulo="Conta"
            onPress={() => navigation.navigate('Conta')}
          />
        </View>

        {/* Versão */}
        <Text style={[styles.titulo, { fontSize: 20 * fontSizeScale }]}>Versão</Text>
        <View style={[styles.card, { backgroundColor: CoresTema.card }]}>
          <Text style={{ color: CoresTema.textoSecundario, fontSize: 14 * fontSizeScale }}>
            Versão Brasileira: Herbert Richers 1.0.0
          </Text>
        </View>

        <TouchableOpacity style={styles.logout} onPress={handleLogout}>
          <Ionicons name="log-out" size={24} color="#fff" />
          <Text style={[styles.logoutText, { fontSize: 18 * fontSizeScale }]}>Sair do app</Text>
        </TouchableOpacity>
      </ScrollView>

      {/* Modal: Conta */}
      <Modal visible={accountModalVisible} transparent animationType="fade" onRequestClose={() => setAccountModalVisible(false)}>
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
          <View style={styles.modalOverlay}>
            <View style={[styles.modalBox, { backgroundColor: CoresTema.card, borderColor: CoresTema.borda }]}> 
              <Text style={[styles.modalTitleSmall, { color: CoresTema.text }]}>Conta</Text>

              <View style={styles.accountField}>
                <Text style={[styles.accountLabel, { color: CoresTema.text }]}>Email</Text>
                <Text style={[styles.accountValue, { color: CoresTema.text }]}>{user?.email || user?.nome || ''}</Text>
              </View>

              <View style={styles.accountField}>
                <Text style={[styles.accountLabel, { color: CoresTema.text }]}>Senha</Text>
                <Text style={[styles.accountValue, { color: CoresTema.text }]}>********</Text>
              </View>

              <View style={{ flexDirection: 'row', justifyContent: 'flex-end', gap: 8 }}>
                <TouchableOpacity style={[styles.secondaryBtn, { marginRight: 8 }]} onPress={() => setAccountModalVisible(false)}>
                  <Text style={styles.secondaryBtnText}>Fechar</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.primaryBtn} onPress={async () => {
                  try {
                    const response = await fetch(`${URL_BASE}/pedir_email/`, {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                      body: `nome=${encodeURIComponent(user?.nome || '')}&sobrenome=${encodeURIComponent(user?.sobrenome || '')}`
                    });
                    const text = await response.text();
                    if (!response.ok) throw new Error(text || 'Erro ao solicitar redefinição');
                    Alert.alert('Enviado', 'Um email para redefinição de senha foi enviado.');
                    setAccountModalVisible(false);
                  } catch (err) {
                    Alert.alert('Erro', err.message || String(err));
                  }
                }}>
                  <Text style={styles.primaryBtnText}>Redefinir senha por email</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        </TouchableWithoutFeedback>
      </Modal>
      
    </View>
  );
}

// Nota: Os estilos base foram mantidos idênticos aos seus originais
const styles = StyleSheet.create({
  container: { flex: 1 },
  perfil: { alignItems: "center", marginBottom: 20, marginTop: 10 },
  avatarWrapper: { width: 130, height: 130, borderRadius: 65, borderWidth: 3, borderColor: COLORS.primary, justifyContent: 'center', alignItems: 'center' },
  avatar: { width: 120, height: 120, borderRadius: 60 },
  avatarPlaceholder: { width: 120, height: 120, borderRadius: 60, borderWidth: 3, borderColor: COLORS.primary, justifyContent: 'center', alignItems: 'center' },
  nome: { fontWeight: "bold", color: COLORS.primary, marginTop: 10 },
  email: { marginBottom: 5 },
  perfilBtn: { backgroundColor: COLORS.primary, paddingHorizontal: 20, paddingVertical: 10, borderRadius: 12, marginTop: 15 },
  perfilBtnText: { color: "#fff", fontWeight: 'bold' },
  titulo: { fontWeight: "bold", marginLeft: 15, marginBottom: 10, color: COLORS.primary },
  card: {
    marginHorizontal: 15, marginBottom: 20, borderRadius: 20, padding: 15, elevation: 4,
    shadowColor: "#000", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4,
  },
  item: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", paddingVertical: 15, borderBottomWidth: 1 },
  left: { flexDirection: "row", alignItems: "center" },
  itemText: { marginLeft: 10 },
  logout: { margin: 20, padding: 15, backgroundColor: "#ff5757", borderRadius: 15, flexDirection: "row", justifyContent: "center", alignItems: "center" },
  logoutText: { color: "#fff", fontWeight: "bold", marginLeft: 10 }
  ,
  modalBox: { width: '90%', borderRadius: 14, padding: 16, borderWidth: 1 },
  modalTitleSmall: { fontSize: 18, fontWeight: '700', marginBottom: 12 },
  accountField: { marginBottom: 12 },
  accountLabel: { fontSize: 12, opacity: 0.8, marginBottom: 6 },
  accountValue: { fontSize: 16, fontWeight: '600' },
  input: { borderWidth: 1, borderColor: '#E6E6E6', padding: 10, borderRadius: 10, marginBottom: 10 },
  primaryBtn: { backgroundColor: COLORS.primary, paddingVertical: 10, paddingHorizontal: 14, borderRadius: 10 },
  primaryBtnText: { color: '#fff', fontWeight: '700' },
  secondaryBtn: { backgroundColor: 'transparent', paddingVertical: 10, paddingHorizontal: 14, borderRadius: 10 },
  secondaryBtnText: { color: '#666', fontWeight: '700' }
});