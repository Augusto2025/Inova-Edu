import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  Platform,
  StatusBar,
  ActivityIndicator,
  Image,
  Alert,
  Modal,
  TextInput,
  SafeAreaView
} from 'react-native';
import Header from '../components/Header';
import SplashScreen from '../screens/SplashScreen';

import { Feather } from '@expo/vector-icons';
import Card from '../components/Card';

// Definição de Cores Padrão
const COLORS = {
  primary: '#005eb8',    // Azul Senac
  darkBlue: '#003d7a',   // Azul Header
  accent: '#f7941d',     // Laranja Senac
  danger: '#EF4444',
  success: '#10B981',
  background: '#EBF2F7',
  card: '#FFFFFF',
  textMain: '#1E293B',
  textSecondary: '#64748B',
  border: '#CBD5E1'
};

// DADOS ESTÁTICOS (MOCK)
const PROJETOS_ESTATICOS = [
  {
    id: 1,
    nome: "Sistema de Gestão Hospitalar",
    descricao: "Desenvolvimento de uma interface para triagem rápida de pacientes em prontos-socorros.",
    imagem: "https://picsum.photos/seed/hosp/300/200",
    repo: "https://github.com/exemplo/hospital"
  },
  {
    id: 2,
    nome: "E-Commerce de Artesanato",
    descricao: "Plataforma para artesãos locais venderem produtos com foco em sustentabilidade.",
    imagem: "https://picsum.photos/seed/shop/300/200",
    repo: "https://github.com/exemplo/shop"
  },
  {
    id: 3,
    nome: "App de Monitoramento Ambiental",
    descricao: "Aplicação mobile que utiliza sensores IoT para medir a qualidade do ar em tempo real.",
    imagem: null, // Teste sem imagem
    repo: "https://github.com/exemplo/eco"
  }
];

export default function ProjetosScreen({ navigation }) {
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);

  const confirmarExclusao = (nome) => {
    Alert.alert(
      "🗑️ Excluir Projeto",
      `Deseja realmente apagar o projeto "${nome}"?`,
      [
        { text: "Cancelar", style: "cancel" },
        { text: "Excluir", style: "destructive", onPress: () => console.log("Excluído") }
      ]
    );
  };

  const irParaRepositorio = (repositorio) => {
    navigation.navigate("Repositorio", { url: repositorio });
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.darkBlue} />
      
      <Header foto={null} escolherImagem={null} nomeTela={"Projetos"} temGoBack={true} telaDestino={"Turmas"} />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        
        {/* ROTA / BREADCRUMB */}
        <View style={styles.breadcrumbCard}>
          <View style={styles.breadcrumbInfo}>
            <Text style={styles.itemSub}>Nome da Turma Selecionada:</Text>
            <Text style={styles.turmaBadge}>Turma: ADS-2026-1A</Text>
          </View>
        </View>

        {/* LISTAGEM DE PROJETOS */}
        {PROJETOS_ESTATICOS.map((projeto) => (
          <Card 
            key={projeto.id}
            titulo={projeto.nome}
            descricao={projeto.descricao}
            imagem={projeto.imagem}
            textoBotao="Repositório"
            iconeBotao="external-link"
            aoPressionar={() => irParaRepositorio(projeto.repo)}
          />
        ))}
      </ScrollView>

      {/* MODAL DE CADASTRO (ESTÁTICO) */}
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

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  center: { justifyContent: 'center', alignItems: 'center' },
  
  header: {
    height: 60,
    backgroundColor: COLORS.darkBlue,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
  },
  headerTitle: { color: 'white', fontSize: 18, fontWeight: 'bold', letterSpacing: 1 },
  
  scrollContent: { padding: 16 },

  // Breadcrumb
  breadcrumbCard: {
    borderRadius: 12,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
    borderLeftWidth: 5,
    backgroundColor: COLORS.card,
    borderLeftColor: COLORS.accent,
  },
  breadcrumbPath: { fontSize: 12, color: COLORS.textSecondary },
  turmaBadge: { fontSize: 14, fontWeight: 'bold', color: COLORS.darkBlue, marginTop: 2 },
  btnAdd: { backgroundColor: COLORS.primary, width: 40, height: 40, borderRadius: 20, justifyContent: 'center', alignItems: 'center' },

  itemSub: { fontSize: 11, color: COLORS.textSecondary },

  // Cards de Projeto
  card: {
    backgroundColor: COLORS.card,
    borderRadius: 15,
    marginBottom: 16,
    overflow: 'hidden',
    elevation: 3,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  cardImage: { width: '100%', height: 140, objectFit: 'cover' },
  noImage: { backgroundColor: '#F1F5F9', justifyContent: 'center', alignItems: 'center' },
  cardBody: { padding: 15 },
  projetoNome: { fontSize: 18, fontWeight: 'bold', color: COLORS.textMain },
  projetoDesc: { fontSize: 14, color: COLORS.textSecondary, marginTop: 5, lineHeight: 20 },
  
  cardActions: {
    justifyContent: 'right',
    alignItems: 'center',
    marginTop: 15,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
  },
  btnRepo: {
    backgroundColor: COLORS.primary,
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    paddingHorizontal: 50,
    borderRadius: 8,
    gap: 8,
  },
  btnRepoText: { color: 'white', fontWeight: 'bold', fontSize: 15 },
  
  // Modal
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'flex-end' },
  modalContent: { 
    backgroundColor: 'white', 
    borderTopLeftRadius: 25, 
    borderTopRightRadius: 25, 
    padding: 25,
    minHeight: 400
  },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  modalTitle: { fontSize: 20, fontWeight: 'bold', color: COLORS.darkBlue },
  input: {
    backgroundColor: '#F8FAFC',
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 10,
    padding: 12,
    marginBottom: 15,
    color: COLORS.textMain
  },
  uploadBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: COLORS.primary,
    borderStyle: 'dashed',
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
    gap: 10
  },
  uploadText: { color: COLORS.primary, fontWeight: 'bold' },
  btnSave: { backgroundColor: COLORS.accent, padding: 16, borderRadius: 12, alignItems: 'center' },
  btnSaveText: { color: 'white', fontWeight: 'bold', fontSize: 16 }
});