import React, { useState, useEffect } from 'react';
import { 
  View, Text, StyleSheet, ScrollView, 
  TouchableOpacity, Modal, TextInput, SafeAreaView, ActivityIndicator, Alert 
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons, FontAwesome5 } from '@expo/vector-icons';
import Header from "../components/Header";
import { COLORS } from "../components/Cores";

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');
const API_PERFIL = `${URL_BASE}/perfil`;

export default function ProfileScreen() {
  const [carregando, setCarregando] = useState(true);
  const [user, setUser] = useState({
    nome: "",
    sobrenome: "",
    descricao: "",
    imagem: null,
    turma: ""
  });

  const [certificados, setCertificados] = useState([]);
  const [projetos, setProjetos] = useState([]); // Estado dinâmico para os projetos

  const [isModalOpen, setIsModalOpen] = useState(false);

  // Função para buscar os dados do backend
  const carregarDadosPerfil = async () => {
    try {
      setCarregando(true);
      const idSalvo = await AsyncStorage.getItem('idUsuario');
      
      if (!idSalvo) {
        Alert.alert("Erro", "Usuário não identificado. Faça login novamente.");
        return;
      }

      console.log(`📡 Buscando perfil na URL: ${URL_BASE}/perfil/${idSalvo}`);
      const response = await fetch(`${URL_BASE}/perfil/${idSalvo}`);
      
      // 1. Pegamos a resposta como texto puro primeiro para evitar o crash do JSON
      const textoRaw = await response.text();

      // 2. Se o servidor retornou erro (404, 500, etc), disparamos o texto puro
      if (!response.ok) {
        throw new Error(`Status ${response.status}: ${textoRaw || "Sem detalhes"}`);
      }

      // 3. Se deu certo, aí sim transformamos o texto em objeto JSON
      const dados = JSON.parse(textoRaw);

      if (dados.sucesso) {
        setUser({
          nome: dados.usuario.nome || "Sem nome",
          sobrenome: dados.usuario.sobrenome || "",
          descricao: dados.usuario.descricao || "Nenhuma descrição informada.",
          imagem: dados.usuario.imagem || null,
          turma: dados.usuario.turma || "Sem Turma Vinculada"
        });
        setCertificados(dados.certificados || []);
        setProjetos(dados.projetos || []);
      } else {
        throw new Error(dados.mensagem || "Erro desconhecido");
      }
    } catch (error) {
      console.error("❌ Erro detalhado ao carregar perfil:", error);
      // Exibe o erro real (HTML ou mensagem) na tela do celular
      Alert.alert("Erro no Carregamento", error.message);
    } finally {
      setCarregando(false);
    }
  };

  // Recarrega os dados toda vez que o usuário entra na tela de Perfil
  useFocusEffect(
    React.useCallback(() => {
      carregarDadosPerfil();
    }, [])
  );

  if (carregando) {
    return (
      <SafeAreaView style={[styles.container, { justifyContent: 'center', alignItems: 'center' }]}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <Header nomeTela="Perfil" temGoBack={true} telaDestino={"Config"}/>
      
      <ScrollView contentContainerStyle={{ paddingBottom: 40}}>
        
        {/* CARD DE PERFIL */}
        <View style={styles.profileCard}>
          <View style={styles.photoWrapper}>
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

          <TouchableOpacity style={styles.editProfileBtn}>
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

          {certificados.length === 0 ? (
            <Text style={styles.emptyText}>Nenhum certificado adicionado.</Text>
          ) : (
            certificados.map(cert => (
              <View key={cert.id} style={styles.certCard}>
                <View style={styles.certIconBadge}>
                  <FontAwesome5 name="award" size={24} color={COLORS.primary} />
                </View>

                <View style={styles.certInfo}>
                  <Text style={styles.certTitle}>{cert.nome}</Text>
                  <Text style={styles.certSub}>{cert.descricao || "Sem descrição"}</Text>
                  <View style={styles.certActions}>
                     <Text style={styles.actionEdit}>Editar</Text>
                     <Text style={styles.actionDelete}>Excluir</Text>
                  </View>
                </View>
              </View>
            ))
          )}
        </View>

        {/* SEÇÃO PROJETOS */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Projetos</Text>
          
          {projetos.length === 0 ? (
            <Text style={styles.emptyText}>Nenhum projeto vinculado a você.</Text>
          ) : (
            projetos.map(proj => (
              <View key={proj.id} style={[styles.projectCard, { marginBottom: 10 }]}>
                <Text style={styles.projectTitle}>{proj.nome}</Text>
                <Text style={styles.projectSub}>{proj.descricao || "Sem descrição disponível."}</Text>
                <TouchableOpacity style={styles.repoBtn}>
                  <Text style={styles.repoBtnText}>Abrir Repositório</Text>
                </TouchableOpacity>
              </View>
            ))
          )}
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.backgroundCard },
  profileCard: { backgroundColor: 'white', margin: 15, borderRadius: 20, padding: 20, alignItems: 'center', elevation: 3 },
  photoWrapper: { position: 'relative' },
  profileImagePlaceholder: { width: 100, height: 100, borderRadius: 50, borderWidth: 3, borderColor: COLORS.primary, backgroundColor: '#f0f0f0' },
  cameraBtn: { position: 'absolute', bottom: 0, right: 0, backgroundColor: COLORS.primary, borderRadius: 20, padding: 8, borderWidth: 2, borderColor: 'white' },
  userName: { fontSize: 22, fontWeight: 'bold', color: COLORS.primary, marginTop: 10 },
  turmaBadge: { backgroundColor: COLORS.primary, paddingHorizontal: 12, paddingVertical: 4, borderRadius: 15, marginTop: 5 },
  turmaText: { color: 'white', fontSize: 11, fontWeight: 'bold' },
  userDesc: { textAlign: 'center', color: '#666', marginTop: 12, fontSize: 14, lineHeight: 20 },
  editProfileBtn: { flexDirection: 'row', backgroundColor: COLORS.accent, marginTop: 15, paddingHorizontal: 20, paddingVertical: 10, borderRadius: 12, alignItems: 'center', gap: 8 },
  editProfileBtnText: { color: 'white', fontWeight: 'bold' },
  section: { paddingHorizontal: 20, marginTop: 15 },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 15 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.primary, marginBottom: 5 },
  plusBtn: { backgroundColor: COLORS.accent, padding: 5, borderRadius: 8 },
  certCard: { backgroundColor: 'white', flexDirection: 'row', padding: 15, borderRadius: 15, marginBottom: 10, elevation: 1, alignItems: 'center' },
  certIconBadge: { width: 50, height: 50, justifyContent: 'center', alignItems: 'center', marginRight: 15 },
  certInfo: { flex: 1 },
  certTitle: { fontWeight: 'bold', fontSize: 15, color: '#333' },
  certSub: { fontSize: 12, color: '#888' },
  certActions: { flexDirection: 'row', gap: 15, marginTop: 8 },
  actionEdit: { color: COLORS.primary, fontSize: 12, fontWeight: 'bold' },
  actionDelete: { color: '#F44336', fontSize: 12, fontWeight: 'bold' },
  projectCard: { backgroundColor: 'white', padding: 15, borderRadius: 15, borderLeftWidth: 5, borderLeftColor: COLORS.primary },
  projectTitle: { fontWeight: 'bold', color: COLORS.primary, fontSize: 16 },
  projectSub: { fontSize: 12, color: '#666', marginTop: 5 },
  repoBtn: { backgroundColor: COLORS.primary, marginTop: 15, padding: 10, borderRadius: 8, alignItems: 'center' },
  repoBtnText: { color: 'white', fontWeight: 'bold', fontSize: 13 },
  emptyText: { color: '#999', italic: true, textAlign: 'center', marginTop: 10, fontSize: 13 }
});