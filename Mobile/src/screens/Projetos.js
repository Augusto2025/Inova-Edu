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

import { Feather } from '@expo/vector-icons';

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

export default function ProjetosScreen() {
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);

  // Simula um carregamento inicial
  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 800);
    return () => clearTimeout(timer);
  }, []);

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

  if (loading) {
    return (
      <View style={[styles.container, styles.center]}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.darkBlue} />
      
      {/* HEADER FIXO */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Repositórios</Text>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        
        {/* ROTA / BREADCRUMB */}
        <View style={styles.breadcrumbCard}>
          <View style={styles.breadcrumbInfo}>
            <Text style={styles.turmaBadge}>Turma: ADS-2026-1A</Text>
          </View>
          <TouchableOpacity 
            style={styles.btnAdd}
            onPress={() => setModalVisible(true)}
          >
            <Feather name="plus" size={20} color="white" />
          </TouchableOpacity>
        </View>

        {/* LISTAGEM DE PROJETOS */}
        {PROJETOS_ESTATICOS.map((projeto) => (
          <View key={projeto.id} style={styles.card}>
            
            {/* Imagem do Projeto */}
            {projeto.imagem ? (
              <Image source={{ uri: projeto.imagem }} style={styles.cardImage} />
            ) : (
              <View style={[styles.cardImage, styles.noImage]}>
                <Feather name="code" size={30} color={COLORS.textSecondary} />
              </View>
            )}

            <View style={styles.cardBody}>
              <Text style={styles.projetoNome}>{projeto.nome}</Text>
              <Text style={styles.projetoDesc} numberOfLines={2}>
                {projeto.descricao}
              </Text>

              <View style={styles.cardActions}>
                <TouchableOpacity style={styles.btnRepo}>
                  <Text style={styles.btnRepoText}>Repositório</Text>
                  <Feather name="external-link" size={14} color="white" />
                </TouchableOpacity>

                <View style={styles.adminTools}>
                  <TouchableOpacity style={styles.iconBtn} onPress={() => Alert.alert("Permissões", "Abrir lista de alunos...")}>
                    <Feather name="users" size={18} color={COLORS.primary} />
                  </TouchableOpacity>
                  
                  <TouchableOpacity style={styles.iconBtn}>
                    <Feather name="edit-3" size={18} color={COLORS.textMain} />
                  </TouchableOpacity>

                  <TouchableOpacity 
                    style={[styles.iconBtn, { backgroundColor: '#FEE2E2' }]} 
                    onPress={() => confirmarExclusao(projeto.nome)}
                  >
                    <Feather name="trash-2" size={18} color={COLORS.danger} />
                  </TouchableOpacity>
                </View>
              </View>
            </View>
          </View>
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
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 20,
    borderLeftWidth: 5,
    borderLeftColor: COLORS.accent,
  },
  breadcrumbPath: { fontSize: 12, color: COLORS.textSecondary },
  turmaBadge: { fontSize: 14, fontWeight: 'bold', color: COLORS.darkBlue, marginTop: 2 },
  btnAdd: { backgroundColor: COLORS.primary, width: 40, height: 40, borderRadius: 20, justifyContent: 'center', alignItems: 'center' },

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
    flexDirection: 'row',
    justifyContent: 'space-between',
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
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    gap: 8,
  },
  btnRepoText: { color: 'white', fontWeight: 'bold', fontSize: 12 },
  
  adminTools: { flexDirection: 'row', gap: 8 },
  iconBtn: {
    width: 36,
    height: 36,
    borderRadius: 8,
    backgroundColor: '#F1F5F9',
    justifyContent: 'center',
    alignItems: 'center',
  },

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