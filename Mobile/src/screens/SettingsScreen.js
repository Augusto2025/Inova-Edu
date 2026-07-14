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
} from "react-native";

import { Ionicons } from "@expo/vector-icons";
import Header from "../components/Header";
import { COLORS } from "../components/Cores"; 
import { ThemeContext } from "../context/ThemeContext";
import AsyncStorage from '@react-native-async-storage/async-storage';

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

// Importando o motor de voz do Expo
import * as Speech from 'expo-speech';

export default function ConfiguracoesScreen({ navigation }) {
  // Puxando os novos estados do controle de fonte global
  const { isDarkMode, toggleDarkMode, fontSizeScale, alterarTamanhoFonte, obterNomeTamanhoFonte } = useContext(ThemeContext);

  const [push, setPush] = useState(false);
  const [email, setEmail] = useState(false);
  const [mensagens, setMensagens] = useState(false);
  const [eventos, setEventos] = useState(false);
  const [usuario, setUsuario] = useState(null);

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

  useEffect(() => {
    const carregarUsuario = async () => {
      try {
        const idSalvo = await AsyncStorage.getItem('idUsuario');
        if (!idSalvo) return;
        const resp = await fetch(`${URL_BASE}/perfil/${idSalvo}`);
        if (!resp.ok) return;
        const texto = await resp.text();
        const dados = JSON.parse(texto);
        if (dados.sucesso && dados.usuario) {
          // Normaliza URL da imagem como em Perfil.js
          let urlCompleta = dados.usuario.imagem;
          if (urlCompleta && !urlCompleta.startsWith('http')) {
            urlCompleta = `https://res.cloudinary.com/dw0pxfap3/${urlCompleta}`;
          }
          setUsuario({
            nome: dados.usuario.nome || '',
            sobrenome: dados.usuario.sobrenome || '',
            descricao: dados.usuario.descricao || '',
            imagem: urlCompleta || null,
            turma: dados.usuario.turma || ''
          });
        }
      } catch (err) {
        console.warn('Não foi possível carregar usuário:', err.message || err);
      }
    };

    carregarUsuario();
  }, []);

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
      <Header nomeTela={"Configurações"} />

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 120 }}>
        
        <View style={styles.perfil}>
          <Image
            source={usuario && usuario.imagem ? { uri: usuario.imagem } : require("../../assets/pascal.jpg")}
            style={styles.avatar}
          />
          <Text style={[styles.nome, { fontSize: 24 * fontSizeScale }]}>{usuario ? `${usuario.nome} ${usuario.sobrenome}`.trim() : 'Usuário'}</Text>
          <Text style={[styles.email, { color: CoresTema.textoSecundario, fontSize: 14 * fontSizeScale }]}>{usuario ? usuario.turma || usuario.descricao || '' : ''}</Text>

          <TouchableOpacity style={styles.perfilBtn} onPress={irParaPerfil}>
            <Text style={[styles.perfilBtnText, { fontSize: 14 * fontSizeScale }]}>Visualizar Perfil</Text>
          </TouchableOpacity>
        </View>

        {/* Notificações */}
        <Text style={[styles.titulo, { fontSize: 20 * fontSizeScale }]}>Notificações</Text>
        <View style={[styles.card, { backgroundColor: CoresTema.card }]}>
          <ItemSwitch icon="notifications" titulo="Notificações Push" valor={push} funcao={setPush} />
          <ItemSwitch icon="mail" titulo="Email" valor={email} funcao={setEmail} />
          <ItemSwitch icon="chatbox" titulo="Mensagens" valor={mensagens} funcao={setMensagens} />
          <ItemSwitch icon="calendar" titulo="Eventos" valor={eventos} funcao={setEventos} />
        </View>

        {/* Aparência e Acessibilidade */}
        <Text style={[styles.titulo, { fontSize: 20 * fontSizeScale }]}>Aparência e Acessibilidade</Text>
        <View style={[styles.card, { backgroundColor: CoresTema.card }]}>
          <ItemSwitch icon="moon" titulo="Modo Escuro" valor={isDarkMode} funcao={toggleDarkMode} />
          
          {/* AÇÃO REAL: Altera o tamanho da fonte do sistema */}
          <ItemBotao 
            icon="text" 
            titulo="Tamanho da fonte" 
            subInfo={obterNomeTamanhoFonte()} 
            onPress={alterarTamanhoFonte} 
          />
          
          {/* AÇÃO REAL: Executa o leitor de voz do Expo */}
          <ItemBotao 
            icon="volume-high" 
            titulo="Texto em voz alta" 
            onPress={executarTextoEmVozAlta} 
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
    </View>
  );
}

// Nota: Os estilos base foram mantidos idênticos aos seus originais
const styles = StyleSheet.create({
  container: { flex: 1 },
  perfil: { alignItems: "center", marginBottom: 20, marginTop: 10 },
  avatar: { width: 120, height: 120, borderRadius: 60, borderWidth: 3, borderColor: "#2d6cdf" },
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
});