import React, { useState, useContext, useCallback } from 'react';
import {
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  Image,
  Modal,
  TextInput,
  SafeAreaView,
  ActivityIndicator,
  Alert
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native'; // Hook de recarregamento
import Header from '../components/Header';
import Skeleton from '../components/Skeleton';
import BreadcrumbCard from '../components/BreadcrumbCard';
import { Feather } from '@expo/vector-icons';
import { COLORS } from "../components/Cores"; 
import styles from '../styles/Projeto';

// Importação do Contexto de Tema e Acessibilidade
import { ThemeContext } from '../context/ThemeContext';

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

export default function ProjetosScreen({ route, navigation }) {
  // Puxando as variáveis globais
  const { theme, fontSizeScale } = useContext(ThemeContext);

  const { turmaId, codigoTurma } = route.params || { turmaId: null, codigoTurma: "Turma" };

  const [projetos, setProjetos] = useState([]); 
  const [carregando, setCarregando] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);

  // Transformando em useCallback para evitar renderizações infinitas
  const buscarProjetos = useCallback(async () => {
    try {
      setCarregando(true);
      const urlCompleta = `${URL_BASE}/projetos?turmaId=${turmaId}`;
      const resposta = await fetch(urlCompleta);
      const dados = await resposta.json();
      
      if (Array.isArray(dados)) {
        setProjetos(dados);
      } else {
        Alert.alert(
          "Erro no Banco de Dados", 
          `${dados.mensagem}\n\nDetalhe Técnico: ${dados.detalhe || 'Erro desconhecido.'}`
        );
      }
    } catch (error) {
      Alert.alert("Erro", "Não foi possível conectar ao servidor de projetos.");
    } finally {
      setCarregando(false);
    }
  }, [turmaId]);

  // Executa a busca toda vez que a tela ganha foco
  useFocusEffect(
    useCallback(() => {
      if (turmaId) {
        buscarProjetos();
      }
    }, [buscarProjetos, turmaId])
  );

  const irParaRepositorio = (projeto) => {
    navigation.navigate("Repositorio", { projetoId: projeto.idprojeto, projetoNome: projeto.nome_projeto });
  };

  return (
    // Fundo dinâmico da tela
    <SafeAreaView style={[styles.container, { backgroundColor: theme.background }]}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.dark} />
      
      <Header 
        foto={null} 
        escolherImagem={null} 
        nomeTela={"Projetos"} 
        temGoBack={true} 
        telaDestino={"Turmas"}
        carregando={carregando}
      />

      <BreadcrumbCard titulo="Projetos:" itemSub={`Turma: ${codigoTurma}`} />

      {carregando ? (
        <View style={{ flex: 1, padding: 20 }}>
          {[1, 2, 3].map((item) => (
            <Skeleton key={item} width="100%" height={100} borderRadius={18} style={{ marginBottom: 16 }} />
          ))}
        </View>
      ) : (
        <ScrollView contentContainerStyle={styles.scrollContent}>
          {projetos.length === 0 ? (
            <Text style={[styles.vazio, { color: theme.text, fontSize: 16 * fontSizeScale }]}>
              Nenhum projeto cadastrado para esta turma.
            </Text>
          ) : (
            projetos.map((projeto) => (
              <TouchableOpacity 
                key={projeto.idprojeto} 
                // Card adaptável ao modo escuro
                style={[styles.projetoCard, { backgroundColor: theme.card, borderColor: theme.border, borderWidth: 1 }]}
                activeOpacity={0.7}
                onPress={() => irParaRepositorio(projeto)}
              >
                <View style={styles.cardInfo}>
                  
                  {/* Imagem de Capa ou Pasta Placeholder adaptável */}
                  {projeto.imagem ? (
                    <Image source={{ uri: projeto.imagem }} style={styles.projetoImagemQuadrada} />
                  ) : (
                    <View style={[styles.projetoImagemQuadrada, styles.placeholderImagemContainer, { backgroundColor: theme.border }]}>
                      <Feather name="folder" size={22 * fontSizeScale} color={COLORS.primary} />
                    </View>
                  )}
                  
                  <View style={{ flex: 1 }}> 
                    <Text style={[styles.projetoNome, { color: theme.text, fontSize: 16 * fontSizeScale }]} numberOfLines={1}>
                      {projeto.nome_projeto}
                    </Text>
                    <Text style={[styles.projetoDesc, { color: theme.text, opacity: 0.7, fontSize: 14 * fontSizeScale }]} numberOfLines={2}>
                      {projeto.descricao || "Sem descrição disponível."}
                    </Text>
                  </View>
                </View>

                <View style={styles.setaContainer}>
                  <Feather name="chevron-right" size={22 * fontSizeScale} color={COLORS.primary} />
                </View>
              </TouchableOpacity>
            ))
          )}
        </ScrollView>
      )}

      {/* MODAL DE CADASTRO */}
      <Modal animationType="slide" transparent={true} visible={modalVisible}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: theme.card }]}>
            <View style={styles.modalHeader}>
              <Text style={[styles.modalTitle, { color: theme.text, fontSize: 20 * fontSizeScale }]}>Novo Projeto</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Feather name="x" size={24 * fontSizeScale} color={theme.text} />
              </TouchableOpacity>
            </View>

            <TextInput 
              style={[
                styles.input, 
                { backgroundColor: theme.background, color: theme.text, borderColor: theme.border, borderWidth: 1, fontSize: 14 * fontSizeScale }
              ]} 
              placeholder="Nome do projeto" 
              placeholderTextColor="#94A3B8" 
            />
            <TextInput 
              style={[
                styles.input, 
                { height: 100, textAlignVertical: 'top', backgroundColor: theme.background, color: theme.text, borderColor: theme.border, borderWidth: 1, fontSize: 14 * fontSizeScale }
              ]} 
              placeholder="Descrição curta..." 
              multiline 
              placeholderTextColor="#94A3B8"
            />
            
            <TouchableOpacity style={[styles.uploadBtn, { borderColor: COLORS.primary, borderWidth: 1, backgroundColor: theme.background }]}>
              <Feather name="image" size={20 * fontSizeScale} color={COLORS.primary} />
              <Text style={[styles.uploadText, { color: COLORS.primary, fontSize: 14 * fontSizeScale }]}>Upload de Capa</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.btnSave} onPress={() => setModalVisible(false)}>
              <Text style={[styles.btnSaveText, { fontSize: 16 * fontSizeScale }]}>Salvar Projeto</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}