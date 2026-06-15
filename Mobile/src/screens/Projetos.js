import React, { useState, useEffect } from 'react';
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
import Header from '../components/Header';
import BreadcrumbCard from '../components/BreadcrumbCard';
import { Feather } from '@expo/vector-icons';
import { COLORS } from "../components/Cores"; 
import styles from '../styles/Projeto';

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

export default function ProjetosScreen({ route, navigation }) {
  const { turmaId, codigoTurma } = route.params || { turmaId: null, codigoTurma: "Turma" };

  const [projetos, setProjetos] = useState([]); 
  const [carregando, setCarregando] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);

  useEffect(() => {
    if (turmaId) {
      buscarProjetos();
    }
  }, [turmaId]);

  const buscarProjetos = async () => {
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
  };

  const irParaRepositorio = (projeto) => {
    navigation.navigate("Repositorio", { projetoId: projeto.idprojeto, projetoNome: projeto.nome_projeto });
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.dark} />
      
      <Header 
        foto={null} 
        escolherImagem={null} 
        nomeTela={"Projetos"} 
        temGoBack={true} 
        telaDestino={"Turmas"} 
      />

      <BreadcrumbCard titulo="Projetos:" itemSub={`Turma: ${codigoTurma}`} />

      {carregando ? (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <ActivityIndicator size="large" color={COLORS.primary} />
          <Text style={{ marginTop: 10, color: COLORS.primary }}>Carregando projetos...</Text>
        </View>
      ) : (
        <ScrollView contentContainerStyle={styles.scrollContent}>
          {projetos.length === 0 ? (
            <Text style={styles.vazio}>Nenhum projeto cadastrado para esta turma.</Text>
          ) : (
            projetos.map((projeto) => (
              <TouchableOpacity 
                key={projeto.idprojeto} 
                style={styles.projetoCard}
                activeOpacity={0.7}
                onPress={() => irParaRepositorio(projeto)}
              >
                <View style={styles.cardInfo}>
                  
                  {/* Imagem de Capa ou Pasta Placeholder */}
                  {projeto.imagem ? (
                    <Image source={{ uri: projeto.imagem }} style={styles.projetoImagemQuadrada} />
                  ) : (
                    <View style={[styles.projetoImagemQuadrada, styles.placeholderImagemContainer]}>
                      <Feather name="folder" size={22} color={COLORS.primary} />
                    </View>
                  )}
                  
                  <View style={{ flex: 1 }}> 
                    <Text style={styles.projetoNome} numberOfLines={1}>
                      {projeto.nome_projeto}
                    </Text>
                    <Text style={styles.projetoDesc} numberOfLines={2}>
                      {projeto.descricao || "Sem descrição disponível."}
                    </Text>
                  </View>
                </View>

                <View style={styles.setaContainer}>
                  <Feather name="chevron-right" size={22} color={COLORS.primary} />
                </View>
              </TouchableOpacity>
            ))
          )}
        </ScrollView>
      )}

      {/* MODAL DE CADASTRO */}
      <Modal animationType="slide" transparent={true} visible={modalVisible}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Novo Projeto</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Feather name="x" size={24} color={COLORS.textSecondary} />
              </TouchableOpacity>
            </View>

            <TextInput style={styles.input} placeholder="Nome do projeto" placeholderTextColor="#94A3B8" />
            <TextInput 
              style={[styles.input, { height: 100, textAlignVertical: 'top' }]} 
              placeholder="Descrição curta..." 
              multiline 
              placeholderTextColor="#94A3B8"
            />
            <TouchableOpacity style={styles.uploadBtn}>
              <Feather name="image" size={20} color={COLORS.primary} />
              <Text style={styles.uploadText}>Upload de Capa</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.btnSave} onPress={() => setModalVisible(false)}>
              <Text style={styles.btnSaveText}>Salvar Projeto</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}