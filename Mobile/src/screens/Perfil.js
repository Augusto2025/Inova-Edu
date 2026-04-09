import React, { useState } from 'react';
import { 
  View, Text, StyleSheet, ScrollView, 
  TouchableOpacity, Modal, TextInput, SafeAreaView 
} from 'react-native';
// Usando o pacote de ícones padrão do Expo
import { Ionicons, FontAwesome5 } from '@expo/vector-icons';

export default function ProfileScreen() {
  const [user, setUser] = useState({
    nome: "João",
    sobrenome: "Silva",
    descricao: "Desenvolvedor Full Stack em formação no Senac.",
    imagem: null, // Mantendo null como solicitado
    turma: "T924 - 2026 (Noite)"
  });

  const [certificados, setCertificados] = useState([
    { id: 1, nome: "React Basic", descricao: "Curso de Hooks e Componentes" }
  ]);

  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <SafeAreaView style={styles.container}>
      {/* HEADER (ESTILO INOVAEDU) */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>InovaEdu</Text>
        <View style={styles.headerAvatar}>
          <Text style={styles.avatarText}>JS</Text>
        </View>
      </View>

      <ScrollView contentContainerStyle={{ paddingBottom: 40 }}>
        
        {/* CARD DE PERFIL */}
        <View style={styles.profileCard}>
          <View style={styles.photoWrapper}>
            {/* ALTERAÇÃO 1: Apenas a borda circular, sem imagem */}
            <View style={styles.profileImagePlaceholder} />
            
            <TouchableOpacity style={styles.cameraBtn}>
              <Ionicons name="camera" size={16} color="white" />
            </TouchableOpacity>
          </View>

          <Text style={styles.userName}>{user.nome} {user.sobrenome}</Text>
          <View style={styles.turmaBadge}>
            <Text style={styles.turmaText}>{user.turma}</Text>
          </View>
          
          <Text style={styles.userDesc}>{user.descricao}</Text>

          <TouchableOpacity 
            style={styles.editProfileBtn} 
            onPress={() => setIsModalOpen(true)}
          >
            <Ionicons name="create-outline" size={18} color="white" />
            <Text style={styles.editProfileBtnText}>Editar Perfil</Text>
          </TouchableOpacity>
        </View>

        {/* SEÇÃO CERTIFICADOS */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Certificados</Text>
            <TouchableOpacity style={styles.plusBtn}>
              <Ionicons name="add" size={20} color="white" />
            </TouchableOpacity>
          </View>

          {certificados.map(cert => (
            <View key={cert.id} style={styles.certCard}>
              {/* ALTERAÇÃO 2: Substituído o calendário por um ícone de certificado */}
              <View style={styles.certIconBadge}>
                <FontAwesome5 name="award" size={24} color="#1459b3" />
              </View>

              <View style={styles.certInfo}>
                <Text style={styles.certTitle}>{cert.nome}</Text>
                <Text style={styles.certSub}>{cert.descricao}</Text>
                <View style={styles.certActions}>
                   <Text style={styles.actionEdit}>Editar</Text>
                   <Text style={styles.actionDelete}>Excluir</Text>
                </View>
              </View>
            </View>
          ))}
        </View>

        {/* SEÇÃO PROJETOS */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Projetos</Text>
          <View style={styles.projectCard}>
            <Text style={styles.projectTitle}>Sistema de Gestão Escolar</Text>
            <Text style={styles.projectSub}>
              <Ionicons name="people" size={12} /> Turma: T924 - ADS
            </Text>
            <TouchableOpacity style={styles.repoBtn}>
              <Text style={styles.repoBtnText}>Abrir Repositório</Text>
            </TouchableOpacity>
          </View>
        </View>

      </ScrollView>

      {/* MODAL DE EDIÇÃO */}
      <Modal visible={isModalOpen} animationType="slide" transparent={true}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Editar Perfil</Text>
              <TouchableOpacity onPress={() => setIsModalOpen(false)}>
                <Ionicons name="close-circle" size={28} color="white" />
              </TouchableOpacity>
            </View>
            <View style={styles.modalBody}>
              <TextInput style={styles.input} placeholder="Nome" defaultValue={user.nome} />
              <TextInput 
                style={[styles.input, { height: 80 }]} 
                placeholder="Bio" 
                multiline 
                defaultValue={user.descricao} 
              />
              <TouchableOpacity style={styles.saveBtn} onPress={() => setIsModalOpen(false)}>
                <Text style={styles.saveBtnText}>Salvar Alterações</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#cfe0e8' },
  header: { 
    backgroundColor: '#1459b3', 
    height: 100, 
    flexDirection: 'row', 
    alignItems: 'center', 
    justifyContent: 'space-between', 
    paddingHorizontal: 20,
    borderBottomLeftRadius: 25,
    borderBottomRightRadius: 25,
    paddingTop: 20
  },
  headerTitle: { color: 'white', fontSize: 20, fontWeight: 'bold' },
  headerAvatar: { width: 35, height: 35, backgroundColor: '#F7941D', borderRadius: 20, justifyContent: 'center', alignItems: 'center' },
  avatarText: { color: 'white', fontWeight: 'bold', fontSize: 12 },

  // Profile Card
  profileCard: { backgroundColor: 'white', margin: 15, borderRadius: 20, padding: 20, alignItems: 'center', elevation: 3 },
  photoWrapper: { position: 'relative' },
  // Estilo para o placeholder circular com borda
  profileImagePlaceholder: { 
    width: 100, 
    height: 100, 
    borderRadius: 50, 
    borderWidth: 3, // Borda visível
    borderColor: '#1459b3', // Cor azul Senac
    backgroundColor: '#f0f0f0' // Um cinza muito claro interno
  },
  cameraBtn: { position: 'absolute', bottom: 0, right: 0, backgroundColor: '#1459b3', borderRadius: 20, padding: 8, borderWidth: 2, borderColor: 'white' },
  userName: { fontSize: 22, fontWeight: 'bold', color: '#1459b3', marginTop: 10 },
  turmaBadge: { backgroundColor: '#1459b3', paddingHorizontal: 12, paddingVertical: 4, borderRadius: 15, marginTop: 5 },
  turmaText: { color: 'white', fontSize: 11, fontWeight: 'bold' },
  userDesc: { textAlign: 'center', color: '#666', marginTop: 12, fontSize: 14, lineHeight: 20 },
  editProfileBtn: { flexDirection: 'row', backgroundColor: '#28a745', marginTop: 15, paddingHorizontal: 20, paddingVertical: 10, borderRadius: 12, alignItems: 'center', gap: 8 },
  editProfileBtnText: { color: 'white', fontWeight: 'bold' },

  // Sections
  section: { paddingHorizontal: 20, marginTop: 15 },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 15 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', color: '#333', marginBottom: 5 },
  plusBtn: { backgroundColor: '#28a745', padding: 5, borderRadius: 8 },
  
  // Certificados (Novo Estilo com Ícone)
  certCard: { backgroundColor: 'white', flexDirection: 'row', padding: 15, borderRadius: 15, marginBottom: 10, elevation: 1, alignItems: 'center' },
  // Estilo para o container do ícone à esquerda
  certIconBadge: { 
    width: 50, 
    height: 50, 
    justifyContent: 'center', 
    alignItems: 'center', 
    marginRight: 15 
  },
  certInfo: { flex: 1 },
  certTitle: { fontWeight: 'bold', fontSize: 15, color: '#333' },
  certSub: { fontSize: 12, color: '#888' },
  certActions: { flexDirection: 'row', gap: 15, marginTop: 8 },
  actionEdit: { color: '#1459b3', fontSize: 12, fontWeight: 'bold' },
  actionDelete: { color: '#F44336', fontSize: 12, fontWeight: 'bold' },

  // Projeto
  projectCard: { backgroundColor: 'white', padding: 15, borderRadius: 15, borderLeftWidth: 5, borderLeftColor: '#1459b3' },
  projectTitle: { fontWeight: 'bold', color: '#1459b3', fontSize: 16 },
  projectSub: { fontSize: 12, color: '#666', marginTop: 5 },
  repoBtn: { backgroundColor: '#1459b3', marginTop: 15, padding: 10, borderRadius: 8, alignItems: 'center' },
  repoBtnText: { color: 'white', fontWeight: 'bold', fontSize: 13 },

  // Modal
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center' },
  modalContent: { backgroundColor: 'white', borderTopLeftRadius: 30, borderTopRightRadius: 30, overflow: 'hidden' },
  modalHeader: { backgroundColor: '#1459b3', flexDirection: 'row', justifyContent: 'space-between', padding: 20, alignItems: 'center' },
  modalTitle: { color: 'white', fontSize: 18, fontWeight: 'bold' },
  modalBody: { padding: 20 },
  input: { borderWidth: 1, borderColor: '#ddd', borderRadius: 12, padding: 12, marginBottom: 15 },
  saveBtn: { backgroundColor: '#1459b3', padding: 15, borderRadius: 12, alignItems: 'center' },
  saveBtnText: { color: 'white', fontWeight: 'bold' }
});