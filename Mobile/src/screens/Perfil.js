import React, { useState } from 'react';
import { 
  View, Text, StyleSheet, ScrollView, 
  TouchableOpacity, SafeAreaView, ActivityIndicator, Alert,
  Modal, TextInput, TouchableWithoutFeedback,
  Image // ✅ ADICIONADO: Importado para exibir a foto de perfil
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons, FontAwesome5, Feather } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker'; // ✅ ADICIONADO: Import do seletor de imagens
import Header from "../components/Header";
import { COLORS } from "../components/Cores";

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

export default function ProfileScreen() {
  const [carregando, setCarregando] = useState(true);
  
  // Dados do Usuário
  const [user, setUser] = useState({
    nome: "",
    sobrenome: "",
    descricao: "",
    imagem: null,
    turma: ""
  });

  const [certificados, setCertificados] = useState([]);
  const [projetos, setProjetos] = useState([]);

  // --- ESTADOS DOS MODAIS ---
  const [modalPerfilVisible, setModalPerfilVisible] = useState(false);
  const [perfilForm, setPerfilForm] = useState({ nome: "", sobrenome: "", descricao: "" });
  const [modalCertVisible, setModalCertVisible] = useState(false);
  const [modalCertModo, setModalCertModo] = useState("Criar"); 
  const [certForm, setCertForm] = useState({ id: null, nome: "", descricao: "" });
  const [modalExcluirVisible, setModalExcluirVisible] = useState(false);
  const [certParaExcluir, setCertParaExcluir] = useState({ id: null, nome: "" });

  // --- FUNÇÕES DE CARREGAMENTO ---
  const carregarDadosPerfil = async () => {
    try {
      setCarregando(true);
      const idSalvo = await AsyncStorage.getItem('idUsuario');
      
      if (!idSalvo) {
        Alert.alert("Erro", "Usuário não identificado. Faça login novamente.");
        return;
      }

      const response = await fetch(`${URL_BASE}/perfil/${idSalvo}`);
      const textoRaw = await response.text();

      if (!response.ok) {
        throw new Error(`Status ${response.status}: ${textoRaw || "Sem detalhes"}`);
      }

      const dados = JSON.parse(textoRaw);

      if (dados.sucesso) {
        setUser({
          nome: dados.usuario.nome || "Sem nome",
          sobrenome: dados.usuario.sobrenome || "",
          descricao: dados.usuario.descricao || "Nenhuma descrição informada.",
          imagem: dados.usuario.imagem || null, // Recebe a string URL do banco
          turma: dados.usuario.turma || "Sem Turma Vinculada"
        });
        setCertificados(dados.certificados || []);
        setProjetos(dados.projetos || []);
      } else {
        throw new Error(dados.mensagem || "Erro desconhecido");
      }
    } catch (error) {
      console.error("❌ Erro ao carregar perfil:", error);
      Alert.alert("Erro no Carregamento", error.message);
    } finally {
      setCarregando(false);
    }
  };

  useFocusEffect(
    React.useCallback(() => {
      carregarDadosPerfil();
    }, [])
  );

  // --- ✅ NOVA FUNÇÃO: SELECIONAR, ENVIAR OU REMOVER FOTO ---
  const alterarFotoPerfil = async () => {
    const idSalvo = await AsyncStorage.getItem('idUsuario');

    Alert.alert(
      "Foto de Perfil",
      "Escolha o que deseja fazer com sua foto:",
      [
        {
          text: "Escolher da Galeria",
          onPress: async () => {
            // Pedir permissão da galeria
            const dadosPermissao = await ImagePicker.requestMediaLibraryPermissionsAsync();
            if (!dadosPermissao.granted) {
              Alert.alert("Permissão necessária", "Precisamos de acesso às fotos para alterar o perfil.");
              return;
            }

            // Abrir a galeria
            const resultado = await ImagePicker.launchImageLibraryAsync({
              mediaTypes: ImagePicker.MediaTypeOptions.Images,
              allowsEditing: true,
              aspect: [1, 1],
              quality: 0.7,
            });

            if (resultado.canceled) return;

            const fotoLocalUri = resultado.assets[0].uri;

            try {
              setCarregando(true);

              // 1. Preparar FormData para o Cloudinary
              const formData = new FormData();
              formData.append('file', {
                uri: fotoLocalUri,
                type: 'image/jpeg',
                name: 'profile.jpg',
              });
              
              // ⚠️ COLOQUE SEUS DADOS DO CLOUDINARY AQUI:
              formData.append('upload_preset', process.env.CLOUDINARY_UPLOAD_PRESET);
              const CLOUD_NAME = process.env.CLOUD_NAME;

              // 2. Enviar direto para o Cloudinary
              const respostaCloudinary = await fetch(
                `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/image/upload`,
                { method: 'POST', body: formData, headers: { 'Content-Type': 'multipart/form-data' } }
              );

              const dadosFoto = await respostaCloudinary.json();
              if (!respostaCloudinary.ok) throw new Error(dadosFoto.error?.message || "Erro no Cloudinary");

              const urlCloudinary = dadosFoto.secure_url;

              // 3. Salvar no seu backend Node.js
              await atualizarFotoNoBackend(idSalvo, urlCloudinary);

            } catch (error) {
              Alert.alert("Erro ao subir imagem", error.message);
              setCarregando(false);
            }
          }
        },
        {
          text: "Remover Foto Atual",
          style: "destructive",
          onPress: async () => {
            try {
              setCarregando(true);
              // Passa 'null' para apagar a foto do banco
              await atualizarFotoNoBackend(idSalvo, null); 
            } catch (error) {
              Alert.alert("Erro ao remover foto", error.message);
              setCarregando(false);
            }
          }
        },
        { text: "Cancelar", style: "cancel" }
      ]
    );
  };

  // Função auxiliar para atualizar a URL no banco de dados
  const atualizarFotoNoBackend = async (idUsuario, urlImagem) => {
    const respostaBackend = await fetch(`${URL_BASE}/perfil/atualizar-foto`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idUsuario, imagem: urlImagem })
    });

    const dadosBack = await respostaBackend.json();

    if (dadosBack.sucesso) {
      setUser({ ...user, imagem: urlImagem }); // Atualiza o estado da tela na hora
      Alert.alert("Sucesso", "Foto de perfil atualizada!");
    } else {
      throw new Error(dadosBack.mensagem || "Erro ao salvar no servidor.");
    }
    setCarregando(false);
  };

  // --- FUNÇÕES DE AÇÃO DOS MODAIS ---
  const abrirEditarPerfil = () => {
    setPerfilForm({ nome: user.nome, sobrenome: user.sobrenome, descricao: user.descricao });
    setModalPerfilVisible(true);
  };

  const salvarPerfil = () => {
    setUser({ ...user, ...perfilForm });
    setModalPerfilVisible(false);
    Alert.alert("Sucesso", "Perfil updated com sucesso!");
  };

  const abrirCriarCertificado = () => {
    setModalCertModo("Criar");
    setCertForm({ id: null, nome: "", descricao: "" });
    setModalCertVisible(true);
  };

  const abrirEditarCertificado = (cert) => {
    setModalCertModo("Editar");
    setCertForm({ id: cert.id, nome: cert.nome, descricao: cert.descricao });
    setModalCertVisible(true);
  };

  const salvarCertificado = () => {
    if (modalCertModo === "Criar") {
      const novoCert = { id: Date.now(), nome: certForm.nome, descricao: certForm.descricao };
      setCertificados([...certificados, novoCert]);
    } else {
      setCertificados(certificados.map(c => c.id === certForm.id ? { ...c, ...certForm } : c));
    }
    setModalCertVisible(false);
    Alert.alert("Sucesso", `Certificado ${modalCertModo === "Criar" ? "adicionado" : "atualizado"}!`);
  };

  const abrirExcluirCertificado = (cert) => {
    setCertParaExcluir({ id: cert.id, nome: cert.nome });
    setModalExcluirVisible(true);
  };

  const confirmarExclusao = () => {
    setCertificados(certificados.filter(c => c.id !== certParaExcluir.id));
    setModalExcluirVisible(false);
    Alert.alert("Sucesso", "Certificado removido.");
  };

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
      
      <ScrollView contentContainerStyle={{ paddingBottom: 40 }} showsVerticalScrollIndicator={false}>
        
        {/* CARD PRINCIPAL DO PERFIL */}
        <View style={styles.profileHeaderCard}>
          <View style={styles.photoContainer}>
            <View style={styles.profileImagePlaceholder}>
              {/* RENDERIZAÇÃO CONDICIONAL DA IMAGEM */}
              {user.imagem ? (
                <Image source={{ uri: user.imagem }} style={styles.profileImage} />
              ) : (
                <Ionicons name="person" size={50} color="#B0B8C4" />
              )}
            </View>
            {/* Botão da câmera agora chama a função real */}
            <TouchableOpacity style={styles.cameraBtn} activeOpacity={0.7} onPress={alterarFotoPerfil}>
              <Ionicons name="camera" size={16} color="white" />
            </TouchableOpacity>
          </View>

          <Text style={styles.userName}>{user.nome} {user.sobrenome}</Text>
          
          <View style={styles.turmaBadge}>
            <Ionicons name="school-outline" size={14} color={COLORS.primary} style={{ marginRight: 4 }} />
            <Text style={styles.turmaText}>{user.turma}</Text>
          </View>
          
          <Text style={styles.userDesc}>{user.descricao}</Text>

          <TouchableOpacity style={styles.editProfileBtn} activeOpacity={0.8} onPress={abrirEditarPerfil}>
            <Ionicons name="create-outline" size={18} color="white" />
            <Text style={styles.editProfileBtnText}>Editar Perfil</Text>
          </TouchableOpacity>
        </View>

        {/* SEÇÃO: CERTIFICADOS */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <View style={styles.titleRow}>
              <Ionicons name="ribbon-outline" size={22} color={COLORS.primary} style={{ marginRight: 8 }} />
              <Text style={styles.sectionTitle}>Certificados</Text>
            </View>
            <TouchableOpacity style={styles.plusBtn} activeOpacity={0.7} onPress={abrirCriarCertificado}>
              <Ionicons name="add" size={20} color="white" />
            </TouchableOpacity>
          </View>

          {certificados.length === 0 ? (
            <View style={styles.emptyContainer}>
              <Ionicons name="document-text-outline" size={32} color="#BBB" />
              <Text style={styles.emptyText}>Nenhum certificado adicionado.</Text>
            </View>
          ) : (
            certificados.map(cert => (
              <View key={cert.id} style={styles.certCard}>
                <View style={styles.certIconBadge}>
                  <FontAwesome5 name="award" size={22} color={COLORS.primary} />
                </View>

                <View style={styles.certInfo}>
                  <Text style={styles.certTitle} numberOfLines={1}>{cert.nome}</Text>
                  <Text style={styles.certSub} numberOfLines={2}>{cert.descricao || "Sem descrição"}</Text>
                </View>

                <View style={styles.certActionColumn}>
                  <TouchableOpacity style={styles.miniActionBtn} onPress={() => abrirEditarCertificado(cert)}>
                    <Ionicons name="pencil" size={16} color={COLORS.primary} />
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.miniActionBtn} onPress={() => abrirExcluirCertificado(cert)}>
                    <Ionicons name="trash-outline" size={16} color="#F44336" />
                  </TouchableOpacity>
                </View>
              </View>
            ))
          )}
        </View>

        {/* SEÇÃO: PROJETOS */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <View style={styles.titleRow}>
              <Ionicons name="folder-open-outline" size={22} color={COLORS.primary} style={{ marginRight: 8 }} />
              <Text style={styles.sectionTitle}>Projetos Integradores</Text>
            </View>
          </View>
          
          {projetos.length === 0 ? (
            <View style={styles.emptyContainer}>
              <Ionicons name="code-slash" size={32} color="#BBB" />
              <Text style={styles.emptyText}>Nenhum projeto vinculado a você.</Text>
            </View>
          ) : (
            projetos.map(proj => (
              <View key={proj.id} style={styles.projectCard}>
                <View style={styles.projectMainInfo}>
                  <Text style={styles.projectTitle}>{proj.nome}</Text>
                  <Text style={styles.projectSub}>{proj.descricao || "Sem descrição disponível."}</Text>
                </View>
                
                <TouchableOpacity style={styles.repoLinkBtn} activeOpacity={0.7}>
                  <Text style={styles.repoLinkText}>Acessar Repositório</Text>
                  <Ionicons name="arrow-forward" size={14} color={COLORS.primary} />
                </TouchableOpacity>
              </View>
            ))
          )}
        </View>

      </ScrollView>

      {/* 1. MODAL EDITAR PERFIL */}
      <Modal visible={modalPerfilVisible} transparent animationType="fade" onRequestClose={() => setModalPerfilVisible(false)}>
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setModalPerfilVisible(false)}>
          <TouchableWithoutFeedback>
            <View style={styles.modalContent}>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>Editar Perfil</Text>
                <TouchableOpacity onPress={() => setModalPerfilVisible(false)} style={{ position: 'absolute', right: 20 }}>
                  <Feather name="x" size={20} color="white" />
                </TouchableOpacity>
              </View>

              <View style={styles.modalBody}>
                <View style={styles.inputContainer}>
                  <Text style={styles.inputLabel}>Nome</Text>
                  <TextInput placeholder="Digite seu nome..." value={perfilForm.nome} onChangeText={(text) => setPerfilForm({ ...perfilForm, nome: text })} style={styles.input} />
                </View>

                <View style={styles.inputContainer}>
                  <Text style={styles.inputLabel}>Sobrenome</Text>
                  <TextInput placeholder="Digite seu sobrenome..." value={perfilForm.sobrenome} onChangeText={(text) => setPerfilForm({ ...perfilForm, sobrenome: text })} style={styles.input} />
                </View>

                <View style={styles.inputContainer}>
                  <Text style={styles.inputLabel}>Bio / Descrição</Text>
                  <TextInput placeholder="Fale um pouco sobre você..." value={perfilForm.descricao} onChangeText={(text) => setPerfilForm({ ...perfilForm, descricao: text })} style={[styles.input, styles.inputMultiline]} multiline numberOfLines={3} textAlignVertical="top" />
                </View>

                <TouchableOpacity style={styles.saveBtn} onPress={salvarPerfil}>
                  <Text style={styles.saveBtnText}>Salvar Alterações</Text>
                </TouchableOpacity>
              </View>
            </View>
          </TouchableWithoutFeedback>
        </TouchableOpacity>
      </Modal>

      {/* 2. MODAL CERTIFICADO */}
      <Modal visible={modalCertVisible} transparent animationType="fade" onRequestClose={() => setModalCertVisible(false)}>
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setModalCertVisible(false)}>
          <TouchableWithoutFeedback>
            <View style={styles.modalContent}>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>{modalCertModo === "Criar" ? "Adicionar Certificado" : "Editar Certificado"}</Text>
                <TouchableOpacity onPress={() => setModalCertVisible(false)} style={{ position: 'absolute', right: 20 }}>
                  <Feather name="x" size={20} color="white" />
                </TouchableOpacity>
              </View>

              <View style={styles.modalBody}>
                <View style={styles.inputContainer}>
                  <Text style={styles.inputLabel}>Nome do Certificado</Text>
                  <TextInput placeholder="Ex: Curso de React Native" value={certForm.nome} onChangeText={(text) => setCertForm({ ...certForm, nome: text })} style={styles.input} />
                </View>

                <View style={styles.inputContainer}>
                  <Text style={styles.inputLabel}>Descrição / Instituição</Text>
                  <TextInput placeholder="Ex: Udemy - 40 horas" value={certForm.descricao} onChangeText={(text) => setCertForm({ ...certForm, descricao: text })} style={[styles.input, styles.inputMultiline]} multiline numberOfLines={2} textAlignVertical="top" />
                </View>

                <TouchableOpacity style={styles.saveBtn} onPress={salvarCertificado}>
                  <Text style={styles.saveBtnText}>{modalCertModo === "Criar" ? "Adicionar" : "Salvar"}</Text>
                </TouchableOpacity>
              </View>
            </View>
          </TouchableWithoutFeedback>
        </TouchableOpacity>
      </Modal>

      {/* 3. MODAL DE CONFIRMAÇÃO DE EXCLUSÃO */}
      <Modal visible={modalExcluirVisible} transparent animationType="fade" onRequestClose={() => setModalExcluirVisible(false)}>
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setModalExcluirVisible(false)}>
          <TouchableWithoutFeedback>
            <View style={styles.modalContent}>
              <View style={[styles.modalHeader, { backgroundColor: '#F44336' }]}>
                <Text style={styles.modalTitle}>Excluir Certificado</Text>
                <TouchableOpacity onPress={() => setModalExcluirVisible(false)} style={{ position: 'absolute', right: 20 }}>
                  <Feather name="x" size={20} color="white" />
                </TouchableOpacity>
              </View>

              <View style={styles.modalBody}>
                <Text style={styles.deleteConfirmText}>
                  Tem certeza de que deseja remover o certificado <Text style={{ fontWeight: 'bold', color: '#1E293B' }}>"{certParaExcluir.nome}"</Text>? Essa ação não pode ser desfeita.
                </Text>

                <View style={styles.deleteActionRow}>
                  <TouchableOpacity style={[styles.saveBtn, styles.btnCancelar]} onPress={() => setModalExcluirVisible(false)}>
                    <Text style={[styles.saveBtnText, { color: '#64748B' }]}>Cancelar</Text>
                  </TouchableOpacity>

                  <TouchableOpacity style={[styles.saveBtn, styles.btnConfirmarExcluir]} onPress={confirmarExclusao}>
                    <Text style={styles.saveBtnText}>Excluir</Text>
                  </TouchableOpacity>
                </View>
              </View>
            </View>
          </TouchableWithoutFeedback>
        </TouchableOpacity>
      </Modal>

    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8FAFC' },
  profileHeaderCard: { 
    backgroundColor: 'white', marginHorizontal: 20, marginTop: 20, marginBottom: 10, borderRadius: 24, padding: 24, alignItems: 'center', 
    shadowColor: "#0F172A", shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.05, shadowRadius: 12, elevation: 4 
  },
  photoContainer: { position: 'relative', marginBottom: 12 },
  profileImagePlaceholder: { 
    width: 105, height: 105, borderRadius: 55, backgroundColor: '#F1F5F9', justifyContent: 'center', alignItems: 'center', 
    borderWidth: 1, borderColor: '#E2E8F0',
    overflow: 'hidden' // ✅ ADICIONADO: Corta a imagem para ficar redondinha perfeita
  },
  profileImage: { width: '100%', height: '100%', resizeMode: 'cover' }, // ✅ ADICIONADO: Estilo da imagem do Cloudinary
  cameraBtn: { position: 'absolute', bottom: 2, right: 2, backgroundColor: COLORS.primary, borderRadius: 18, padding: 8, borderWidth: 3, borderColor: 'white', elevation: 3 },
  userName: { fontSize: 22, fontWeight: '700', color: '#1E293B', textAlign: 'center' },
  turmaBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#EFF6FF', paddingHorizontal: 14, paddingVertical: 5, borderRadius: 20, marginTop: 8 },
  turmaText: { color: COLORS.primary, fontSize: 12, fontWeight: '600' },
  userDesc: { textAlign: 'center', color: '#64748B', marginTop: 14, fontSize: 14, lineHeight: 21, paddingHorizontal: 10 },
  editProfileBtn: { flexDirection: 'row', backgroundColor: COLORS.primary, marginTop: 20, paddingHorizontal: 24, paddingVertical: 12, borderRadius: 16, alignItems: 'center', gap: 8, width: '100%', justifyContent: 'center' },
  editProfileBtnText: { color: 'white', fontWeight: '600', fontSize: 15 },
  section: { paddingHorizontal: 20, marginTop: 25 },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 },
  titleRow: { flexDirection: 'row', alignItems: 'center' },
  sectionTitle: { fontSize: 18, fontWeight: '700', color: '#1E293B' },
  plusBtn: { backgroundColor: COLORS.primary, padding: 6, borderRadius: 10 },
  certCard: { backgroundColor: 'white', flexDirection: 'row', padding: 16, borderRadius: 18, marginBottom: 12, alignItems: 'center', shadowColor: "#0F172A", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.03, shadowRadius: 8, elevation: 2 },
  certIconBadge: { width: 46, height: 46, borderRadius: 12, backgroundColor: '#EFF6FF', justifyContent: 'center', alignItems: 'center', marginRight: 14 },
  certInfo: { flex: 1, paddingRight: 8 },
  certTitle: { fontWeight: '600', fontSize: 15, color: '#1E293B' },
  certSub: { fontSize: 13, color: '#64748B', marginTop: 2 },
  certActionColumn: { flexDirection: 'column', gap: 8, justifyContent: 'center', alignItems: 'center', borderLeftWidth: 1, borderLeftColor: '#F1F5F9', paddingLeft: 12 },
  miniActionBtn: { padding: 4 },
  projectCard: { backgroundColor: 'white', padding: 20, borderRadius: 18, marginBottom: 12, shadowColor: "#0F172A", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.03, shadowRadius: 8, elevation: 2 },
  projectMainInfo: { marginBottom: 14 },
  projectTitle: { fontWeight: '700', color: '#1E293B', fontSize: 16 },
  projectSub: { fontSize: 13, color: '#64748B', marginTop: 6, lineHeight: 18 },
  repoLinkBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'flex-start', gap: 4, paddingVertical: 4 },
  repoLinkText: { color: COLORS.primary, fontWeight: '600', fontSize: 14 },
  emptyContainer: { backgroundColor: '#F1F5F9', borderRadius: 16, padding: 20, alignItems: 'center', justifyContent: 'center', borderStyle: 'dashed', borderWidth: 1, borderColor: '#CBD5E1', marginTop: 5 },
  emptyText: { color: '#64748B', fontStyle: 'italic', textAlign: 'center', marginTop: 8, fontSize: 13 },

  modalOverlay: { flex: 1, backgroundColor: 'rgba(0, 0, 0, 0.55)', justifyContent: 'center', padding: 20 },
  modalContent: { backgroundColor: 'white', borderRadius: 24, overflow: 'hidden', shadowColor: '#000', shadowOffset: { width: 0, height: 10 }, shadowOpacity: 0.1, shadowRadius: 20, elevation: 10 },
  modalHeader: { backgroundColor: COLORS.primary, flexDirection: 'row', padding: 20, alignItems: 'center', justifyContent: 'center' },
  modalTitle: { color: 'white', fontSize: 18, fontWeight: '700' },
  modalBody: { padding: 24 },
  inputContainer: { marginBottom: 16 },
  inputLabel: { fontSize: 14, fontWeight: "600", color: "#334155", marginBottom: 6, paddingLeft: 2 },
  input: { borderWidth: 1, borderColor: '#E2E8F0', borderRadius: 14, padding: 14, color: '#1E293B', backgroundColor: '#F8FAFC', fontSize: 15 },
  inputMultiline: { minHeight: 70 },
  saveBtn: { backgroundColor: COLORS.primary, padding: 15, borderRadius: 14, alignItems: 'center', marginTop: 10, justifyContent: 'center' },
  saveBtnText: { color: 'white', fontWeight: '700', fontSize: 15 },
  deleteConfirmText: { fontSize: 15, color: '#475569', textAlign: 'center', lineHeight: 22, marginBottom: 20 },
  deleteActionRow: { flexDirection: 'row', gap: 12 },
  btnCancelar: { flex: 1, backgroundColor: '#E2E8F0', marginTop: 0 },
  btnConfirmarExcluir: { flex: 1, backgroundColor: '#F44336', marginTop: 0 }
});