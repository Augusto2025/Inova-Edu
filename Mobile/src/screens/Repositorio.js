import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator,
  Alert,
  Modal,
  TextInput,
  SafeAreaView
} from 'react-native';

import { Feather } from '@expo/vector-icons';

// Definição de Cores Padrão (Mantendo seu modelo)
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

// DADOS MOCK (PASTAS E ARQUIVOS)
const REPOSITORIO_MOCK = {
  projeto_nome: "Sistema de Gestão Hospitalar",
  pastas: [
    { id: 1, nome: "Documentação", itens: 3 },
    { id: 2, nome: "Imagens do Protótipo", itens: 8 },
    { id: 3, nome: "Scripts SQL", itens: 2 },
  ],
  arquivos: [
    { id: 1, nome: "index.html", tamanho: "12kb" },
    { id: 2, nome: "readme.md", tamanho: "5kb" },
    { id: 3, nome: "package.json", tamanho: "2kb" },
  ]
};

export default function RepositorioScreen() {
  const [loading, setLoading] = useState(true);
  const [modalPastaVisible, setModalPastaVisible] = useState(false);
  const [selecaoAtiva, setSelecaoAtiva] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 800);
    return () => clearTimeout(timer);
  }, []);

  const confirmarExclusao = (item) => {
    Alert.alert(
      "🗑️ Confirmar Exclusão",
      `Tem certeza que deseja excluir "${item}"?`,
      [
        { text: "Cancelar", style: "cancel" },
        { text: "Excluir", style: "destructive" }
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
        <TouchableOpacity style={styles.backButton}>
          <Feather name="chevron-left" size={24} color="white" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Repositório</Text>
        <TouchableOpacity style={styles.downloadHeader}>
          <Feather name="download" size={20} color="white" />
        </TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        
        {/* ROTA / BREADCRUMB */}
        <View style={styles.breadcrumbCard}>
          <View style={{ flex: 1 }}>
            <Text style={styles.itemSub}>Nome do Projeto:</Text>
            <Text style={styles.projetoBadge}>{REPOSITORIO_MOCK.projeto_nome}</Text>
          </View>
          <TouchableOpacity 
            style={[styles.btnActionMain, { backgroundColor: COLORS.accent }]}
            onPress={() => setModalPastaVisible(true)}
          >
            <Feather name="folder-plus" size={20} color="white" />
          </TouchableOpacity>
        </View>

        {/* SEÇÃO DE PASTAS */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Pastas</Text>
          <TouchableOpacity onPress={() => setSelecaoAtiva(!selecaoAtiva)}>
            <Text style={styles.btnToggleText}>{selecaoAtiva ? "Cancelar" : "Selecionar"}</Text>
          </TouchableOpacity>
        </View>

        {REPOSITORIO_MOCK.pastas.map((pasta) => (
          <TouchableOpacity key={pasta.id} style={[styles.itemCard, styles.folderBorder]}>
            <View style={styles.itemInfo}>
              {selecaoAtiva && <View style={styles.checkboxPlaceholder} />}
              <Feather name="folder" size={24} color={COLORS.primary} />
              <View style={{ marginLeft: 12 }}>
                <Text style={styles.itemName}>{pasta.nome}</Text>
                <Text style={styles.itemSub}>{pasta.itens} itens</Text>
              </View>
            </View>
            {!selecaoAtiva && (
              <View style={styles.itemActions}>
                <TouchableOpacity onPress={() => confirmarExclusao(pasta.nome)}>
                  <Feather name="trash-2" size={18} color={COLORS.danger} />
                </TouchableOpacity>
              </View>
            )}
          </TouchableOpacity>
        ))}

        {/* SEÇÃO DE ARQUIVOS */}
        <View style={[styles.sectionHeader, { marginTop: 20 }]}>
          <Text style={styles.sectionTitle}>Arquivos</Text>
          <TouchableOpacity style={styles.btnUploadSmall}>
            <Feather name="file-plus" size={16} color={COLORS.primary} />
            <Text style={styles.btnUploadSmallText}>Upload</Text>
          </TouchableOpacity>
        </View>

        {REPOSITORIO_MOCK.arquivos.map((arquivo) => (
          <View key={arquivo.id} style={[styles.itemCard, styles.fileBorder]}>
            <View style={styles.itemInfo}>
              <Feather name="file-text" size={24} color={COLORS.textSecondary} />
              <View style={{ marginLeft: 12 }}>
                <Text style={styles.itemName}>{arquivo.nome}</Text>
                <Text style={styles.itemSub}>{arquivo.tamanho}</Text>
              </View>
            </View>
            <TouchableOpacity onPress={() => confirmarExclusao(arquivo.nome)}>
              <Feather name="trash-2" size={18} color={COLORS.danger} />
            </TouchableOpacity>
          </View>
        ))}

        {/* BOTÕES DE EXCLUSÃO EM MASSA (APARECEM NA SELEÇÃO) */}
        {selecaoAtiva && (
          <View style={styles.massActions}>
            <TouchableOpacity style={styles.btnMassDelete}>
              <Text style={styles.btnMassDeleteText}>Excluir Selecionados</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>

      {/* MODAL CRIAR PASTA */}
      <Modal animationType="fade" transparent={true} visible={modalPastaVisible}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Criar Nova Pasta</Text>
              <TouchableOpacity onPress={() => setModalPastaVisible(false)}>
                <Feather name="x" size={24} color={COLORS.textSecondary} />
              </TouchableOpacity>
            </View>

            <Text style={styles.label}>Nome da Pasta</Text>
            <TextInput 
              style={styles.input} 
              placeholder="Ex: Documentação" 
              placeholderTextColor="#94A3B8" 
            />

            <View style={styles.modalFooter}>
              <TouchableOpacity 
                style={styles.btnCancel} 
                onPress={() => setModalPastaVisible(false)}
              >
                <Text style={styles.btnCancelText}>Cancelar</Text>
              </TouchableOpacity>
              <TouchableOpacity 
                style={styles.btnSave} 
                onPress={() => setModalPastaVisible(false)}
              >
                <Text style={styles.btnSaveText}>Criar Pasta</Text>
              </TouchableOpacity>
            </View>
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 15,
    elevation: 4,
  },
  headerTitle: { color: 'white', fontSize: 18, fontWeight: 'bold' },
  backButton: { width: 40 },
  downloadHeader: { width: 40, alignItems: 'flex-end' },
  
  scrollContent: { padding: 16, paddingBottom: 40 },

  // Breadcrumb
  breadcrumbCard: {
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
    borderLeftWidth: 5,
    borderLeftColor: COLORS.primary,
  },
  breadcrumbPath: { fontSize: 11, color: COLORS.textSecondary },
  projetoBadge: { fontSize: 15, fontWeight: 'bold', color: COLORS.darkBlue, marginTop: 2 },
  btnActionMain: { width: 45, height: 45, borderRadius: 12, justifyContent: 'center', alignItems: 'center' },

  // Listagem
  sectionHeader: { 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'center', 
    marginBottom: 12,
    paddingHorizontal: 4
  },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', color: COLORS.textMain },
  btnToggleText: { color: COLORS.primary, fontWeight: 'bold', fontSize: 13 },
  btnUploadSmall: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    backgroundColor: 'white', 
    paddingHorizontal: 10, 
    paddingVertical: 5, 
    borderRadius: 6,
    borderWidth: 1,
    borderColor: COLORS.primary
  },
  btnUploadSmallText: { color: COLORS.primary, fontSize: 12, fontWeight: 'bold', marginLeft: 5 },

  itemCard: {
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 10,
    elevation: 1,
  },
  folderBorder: { borderLeftWidth: 4, borderLeftColor: COLORS.primary },
  fileBorder: { borderLeftWidth: 4, borderLeftColor: COLORS.textSecondary },
  
  itemInfo: { flexDirection: 'row', alignItems: 'center', flex: 1 },
  itemName: { fontSize: 14, fontWeight: '600', color: COLORS.textMain },
  itemSub: { fontSize: 11, color: COLORS.textSecondary },
  checkboxPlaceholder: { 
    width: 20, 
    height: 20, 
    borderRadius: 4, 
    borderWidth: 2, 
    borderColor: COLORS.primary, 
    marginRight: 10 
  },

  // Mass Actions
  massActions: { marginTop: 10, alignItems: 'center' },
  btnMassDelete: { 
    backgroundColor: '#FEE2E2', 
    padding: 12, 
    borderRadius: 8, 
    width: '100%', 
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.danger
  },
  btnMassDeleteText: { color: COLORS.danger, fontWeight: 'bold' },

  // Modal
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'center', padding: 20 },
  modalContent: { backgroundColor: 'white', borderRadius: 20, padding: 20 },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  modalTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.darkBlue },
  label: { fontSize: 14, color: COLORS.textMain, marginBottom: 8, fontWeight: '500' },
  input: {
    backgroundColor: '#F8FAFC',
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 10,
    padding: 12,
    marginBottom: 20,
    color: COLORS.textMain
  },
  modalFooter: { flexDirection: 'row', gap: 10 },
  btnCancel: { flex: 1, padding: 14, borderRadius: 10, alignItems: 'center', backgroundColor: '#F1F5F9' },
  btnCancelText: { color: COLORS.textSecondary, fontWeight: 'bold' },
  btnSave: { flex: 2, padding: 14, borderRadius: 10, alignItems: 'center', backgroundColor: COLORS.accent },
  btnSaveText: { color: 'white', fontWeight: 'bold' }
});