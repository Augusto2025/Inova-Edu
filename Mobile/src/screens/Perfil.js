import React, { useState } from 'react';
import { 
  View, Text, StyleSheet, ScrollView, 
  TouchableOpacity, ActivityIndicator, Alert,
  Modal, TextInput, TouchableWithoutFeedback,
  Image,
  Linking
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons, FontAwesome5, Feather } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker'; 
import * as FileSystem from 'expo-file-system/legacy';
import Header from "../components/Header";
import Skeleton from "../components/Skeleton";
import { COLORS } from "../components/Cores";
import { useTheme } from '../context/ThemeContext';
import { useUser } from '../context/UserContext';
import { RAW_BACKEND_URL, URL_BASE } from '../config/backend';

export default function ProfileScreen() {
  const [carregando, setCarregando] = useState(true);
  const { theme, fontSizeScale } = useTheme();
  const { user, carregarUsuario, atualizarPerfil, atualizarFoto } = useUser();
  const usuarioExibicao = user || { nome: '', sobrenome: '', descricao: '', imagem: null, turma: '' };
  
  // Estado local para dados que o Perfil precisa
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
  // Estados de salvamento para os modais
  const [savingPerfil, setSavingPerfil] = useState(false);
  const [savingCert, setSavingCert] = useState(false);

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
        // Carrega certificados e projetos
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
      const carregar = async () => {
        // Recarrega dados do usuário do backend via contexto primeiro
        await carregarUsuario();
        // Depois carrega certificados e projetos locais
        await carregarDadosPerfil();
      };
      carregar();
    }, [])
  );

  // --- FUNÇÃO: SELECIONAR, ENVIAR OU REMOVER FOTO ---
  const alterarFotoPerfil = async () => {
    const idSalvo = await AsyncStorage.getItem('idUsuario');

    if (!idSalvo) {
      Alert.alert("Erro", "Usuário não identificado. Faça login novamente.");
      return;
    }

    Alert.alert(
      "Foto de Perfil",
      "Escolha o que deseja fazer com sua foto:",
      [
        {
          text: "Escolher da Galeria",
          onPress: async () => {
            const dadosPermissao = await ImagePicker.requestMediaLibraryPermissionsAsync();
            if (!dadosPermissao.granted) {
              Alert.alert("Permissão necessária", "Precisamos de acesso às fotos para alterar o perfil.");
              return;
            }

            const resultado = await ImagePicker.launchImageLibraryAsync({
              mediaTypes: ['images'],
              allowsEditing: true,
              aspect: [1, 1],
              quality: 0.3, // Reduzir bastante a qualidade para evitar payload grande
              base64: true, // Adicionar base64
            });

            if (resultado.canceled) return;

            const { uri: fotoLocalUriRaw, type: assetType, fileName: assetName, base64: base64Data } = resultado.assets[0];
            const fileName = assetName || 'profile.jpg';
            const fileExtension = fileName.split('.').pop()?.toLowerCase();
            const mimeType = assetType && assetType.includes('/')
              ? assetType
              : fileExtension === 'png'
                ? 'image/png'
                : fileExtension === 'gif'
                  ? 'image/gif'
                  : fileExtension === 'jpg' || fileExtension === 'jpeg'
                    ? 'image/jpeg'
                    : 'application/octet-stream';

            console.log('📸 Upload de imagem:', {
              fileName,
              assetType,
              hasBase64: !!base64Data,
              mimeType,
            });

            try {
              setCarregando(true);

              const hasCloudinaryConfig = process.env.EXPO_PUBLIC_CLOUDINARY_UPLOAD_PRESET && process.env.EXPO_PUBLIC_CLOUD_NAME;
              const isLocalBackend = URL_BASE.includes('localhost') || URL_BASE.includes('127.0.0.1') || URL_BASE.includes('192.168.');

              if (hasCloudinaryConfig) {
                console.log("📤 Enviando para Cloudinary...");

                const CLOUD_NAME = process.env.EXPO_PUBLIC_CLOUD_NAME;
                const UPLOAD_PRESET = process.env.EXPO_PUBLIC_CLOUDINARY_UPLOAD_PRESET;
                const cloudinaryForm = new FormData();

                cloudinaryForm.append('file', {
                  uri: fotoLocalUri,
                  type: mimeType,
                  name: fileName,
                });
                cloudinaryForm.append('upload_preset', UPLOAD_PRESET);

                const respostaCloudinary = await fetch(
                  `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/image/upload`,
                  {
                    method: 'POST',
                    body: cloudinaryForm,
                  }
                );

                const dadosFoto = await respostaCloudinary.json();
                if (!respostaCloudinary.ok) {
                  console.error("❌ Erro Cloudinary:", dadosFoto);
                  throw new Error(dadosFoto.error?.message || "Erro no Cloudinary");
                }

                const urlCloudinary = dadosFoto.secure_url;
                console.log("✅ URL Cloudinary:", urlCloudinary);
                await atualizarFotoNoBackend(idSalvo, urlCloudinary);
              } else {
                console.log("📤 Enviando para backend via /perfil/upload-foto...");

                if (!base64Data) {
                  throw new Error('Não foi possível obter os dados da imagem.');
                }

                const mimeType = assetType === 'image' ? 'image/jpeg' : assetType || 'image/jpeg';
                
                const respostaServidor = await fetch(`${URL_BASE}/perfil/upload-foto`, {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json',
                  },
                  body: JSON.stringify({
                    idUsuario: idSalvo,
                    fileName,
                    mimeType,
                    base64: base64Data,
                  }),
                });

                console.log("📊 Status da resposta:", respostaServidor.status);

                if (respostaServidor.status < 200 || respostaServidor.status >= 300) {
                  const errorText = await respostaServidor.text();
                  console.error('❌ Erro no upload backend:', respostaServidor.status, errorText);
                  throw new Error(`Upload falhou: ${respostaServidor.status}`);
                }

                const dadosServidor = await respostaServidor.json();
                console.log("📦 Resposta do servidor:", dadosServidor);

                if (dadosServidor.sucesso) {
                  console.log("✅ Foto atualizada com sucesso");
                  await atualizarFotoNoBackend(idSalvo, dadosServidor.imagem);
                } else {
                  throw new Error(dadosServidor.mensagem || "Erro ao fazer upload no servidor");
                }
              }

            } catch (error) {
              console.error("❌ Erro ao subir imagem:", error);
              Alert.alert("Erro ao subir imagem", error.message);
            } finally {
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
              await atualizarFotoNoBackend(idSalvo, null); 
            } catch (error) {
              Alert.alert("Erro ao remover foto", error.message);
            } finally {
              setCarregando(false);
            }
          }
        },
        { text: "Cancelar", style: "cancel" }
      ]
    );
  };

  const atualizarFotoNoBackend = async (idUsuario, urlImagem) => {
    try {
      const respostaBackend = await fetch(`${URL_BASE}/perfil/atualizar-foto`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idUsuario, imagem: urlImagem })
      });

      const dadosBack = await respostaBackend.json();

      if (dadosBack.sucesso) {
        console.log("✅ Foto salva no backend:", urlImagem);
        // Atualiza o contexto global de usuário
        atualizarFoto(urlImagem);
        // Recarrega dados completos do backend para garantir sincronização
        await carregarUsuario();
        Alert.alert("Sucesso", "Foto de perfil atualizada!");
      } else {
        throw new Error(dadosBack.mensagem || "Erro ao salvar no servidor.");
      }
    } catch (error) {
      console.error("❌ Erro ao atualizar foto:", error);
      throw error;
    }
  };

  // --- FUNÇÕES DE AÇÃO DOS MODAIS ---
  const abrirEditarPerfil = () => {
    if (!user) {
      Alert.alert("Aguarde", "Os dados do perfil ainda estão sendo carregados.");
      return;
    }
    setPerfilForm({ nome: usuarioExibicao.nome, sobrenome: usuarioExibicao.sobrenome, descricao: usuarioExibicao.descricao });
    setModalPerfilVisible(true);
  };

  const salvarPerfil = async () => {
    try {
      const idSalvo = await AsyncStorage.getItem('idUsuario');
      if (!idSalvo) {
        Alert.alert("Erro", "Usuário não identificado. Faça login novamente.");
        return;
      }
      setSavingPerfil(true);
      setCarregando(true);
      const response = await fetch(`${URL_BASE}/perfil/atualizar-dados`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          idUsuario: idSalvo,
          nome: perfilForm.nome.trim(),
          sobrenome: perfilForm.sobrenome.trim(),
          descricao: perfilForm.descricao.trim()
        })
      });

      const dados = await response.json();
      if (!response.ok || !dados.sucesso) {
        throw new Error(dados.mensagem || 'Erro ao salvar perfil.');
      }

      // Atualiza o contexto global de usuário
      atualizarPerfil({
        nome: perfilForm.nome.trim(),
        sobrenome: perfilForm.sobrenome.trim(),
        descricao: perfilForm.descricao.trim()
      });
      
      // Recarrega dados completos do backend
      await carregarUsuario();
      
      setModalPerfilVisible(false);
      Alert.alert("Sucesso", "Perfil atualizado com sucesso!");
    } catch (error) {
      Alert.alert("Erro", error.message);
    } finally {
      setSavingPerfil(false);
      setCarregando(false);
    }
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

  const salvarCertificado = async () => {
    // Validação simples para não salvar em branco
    if (!certForm.nome.trim()) {
      Alert.alert("Erro", "O nome do certificado é obrigatório.");
      return;
    }

    try {
      setSavingCert(true);
      if (modalCertModo === "Criar") {
        const response = await fetch(`${URL_BASE}/perfil/certificado`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            usuarioId: user.idUsuario, // Certifique-se de usar a variável que guarda o ID do usuário logado
            nome: certForm.nome, 
            descricao: certForm.descricao 
          }),
        });

        const dados = await response.json();

        if (dados.sucesso) {
          // Atualiza a tela usando o ID REAL gerado pelo banco de dados (Postgres)
          setCertificados([...certificados, dados.certificado]);
          Alert.alert("Sucesso", "Certificado adicionado ao banco!");
        } else {
          Alert.alert("Erro", dados.mensagem || "Erro ao adicionar certificado.");
        }

      } else {
        // 📝 ATUALIZA NO BANCO DE DADOS (PUT)
        const response = await fetch(`${URL_BASE}/perfil/certificado/${certForm.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            nome: certForm.nome, 
            descricao: certForm.descricao 
          }),
        });

        const dados = await response.json();

        if (dados.sucesso) {
          // Atualiza o estado na tela refletindo a mudança real do banco
          setCertificados(certificados.map(c => c.id === certForm.id ? { ...c, ...certForm } : c));
          Alert.alert("Sucesso", "Certificado atualizado com sucesso!");
        } else {
          Alert.alert("Erro", dados.mensagem || "Erro ao atualizar certificado.");
        }
      }

      // Fecha o modal após o sucesso da requisição
      setModalCertVisible(false);

    } catch (error) {
      console.error("❌ Erro ao salvar certificado no banco:", error);
      Alert.alert("Erro", "Não foi possível conectar ao servidor.");
    }
    finally {
      setSavingCert(false);
    }
  };

  const abrirExcluirCertificado = (cert) => {
    setCertParaExcluir({ id: cert.id, nome: cert.nome });
    setModalExcluirVisible(true);
  };

  const confirmarExclusao = async () => {
    try {
      // ⚠️ ATENÇÃO: Substitua pelo endereço do seu servidor (o mesmo usado no salvar)
      const response = await fetch(`${URL_BASE}/perfil/certificado/${certParaExcluir.id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        // Se o seu backend exigir o usuarioId no DELETE, descomente a linha abaixo:
        // body: JSON.stringify({ usuarioId: user.idUsuario }) 
      });

      const dados = await response.json();

      if (dados.sucesso) {
        // Remove da tela somente se o banco confirmar a exclusão
        setCertificados(certificados.filter(c => c.id !== certParaExcluir.id));
        setModalExcluirVisible(false);
        Alert.alert("Sucesso", "Certificado removido do banco!");
      } else {
        Alert.alert("Erro", dados.mensagem || "Não foi possível excluir no servidor.");
      }
    } catch (error) {
      console.error("❌ Erro ao excluir certificado:", error);
      Alert.alert("Erro", "Falha ao conectar com o servidor.");
    }
  };

  if (carregando) {
    return (
      <SafeAreaView style={[styles.container, { backgroundColor: theme.background }]}> 
        <Header nomeTela="Perfil" temGoBack={true} telaDestino={"Config"} carregando={true} />
        <ScrollView contentContainerStyle={{ padding: 20, gap: 18 }} showsVerticalScrollIndicator={false}>
          <View style={[styles.profileHeaderCard, { backgroundColor: theme.card }]}> 
            <Skeleton width={105} height={105} borderRadius={55} style={{ alignSelf: 'center', marginBottom: 18 }} />
            <Skeleton width="70%" height={22} borderRadius={10} style={{ alignSelf: 'center', marginBottom: 8 }} />
            <Skeleton width="45%" height={16} borderRadius={8} style={{ alignSelf: 'center', marginBottom: 8 }} />
            <Skeleton width="90%" height={14} borderRadius={8} style={{ alignSelf: 'center', marginBottom: 8 }} />
            <Skeleton width="60%" height={42} borderRadius={16} style={{ alignSelf: 'center', marginTop: 12 }} />
          </View>

          <View style={styles.section}>
            <View style={[styles.sectionHeader, { borderBottomColor: theme.border, borderBottomWidth: 1, paddingBottom: 10 }]}> 
              <Skeleton width="45%" height={18} borderRadius={8} />
              <Skeleton width={40} height={40} borderRadius={12} />
            </View>
            {[1, 2].map((item) => (
              <View key={item} style={[styles.certCard, { backgroundColor: theme.card, borderColor: theme.border }]}> 
                <Skeleton width={46} height={46} borderRadius={14} />
                <View style={{ flex: 1, marginLeft: 14, justifyContent: 'center', gap: 8 }}>
                  <Skeleton width="80%" height={16} borderRadius={8} />
                  <Skeleton width="60%" height={12} borderRadius={8} />
                </View>
                <Skeleton width={36} height={36} borderRadius={12} />
              </View>
            ))}
          </View>

          <View style={styles.section}>
            <View style={[styles.sectionHeader, { borderBottomColor: theme.border, borderBottomWidth: 1, paddingBottom: 10 }]}> 
              <Skeleton width="55%" height={18} borderRadius={8} />
            </View>
            {[1, 2].map((item) => (
              <View key={item} style={[styles.projectCard, { backgroundColor: theme.card, borderColor: theme.border }]}> 
                <Skeleton width="100%" height={18} borderRadius={10} style={{ marginBottom: 10 }} />
                <Skeleton width="90%" height={14} borderRadius={10} />
              </View>
            ))}
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: theme.background }]}>
      <Header nomeTela="Perfil" temGoBack={true} telaDestino={"Config"} carregando={carregando} />
      
      <ScrollView contentContainerStyle={{ paddingBottom: 40 }} showsVerticalScrollIndicator={false}>
        
        {/* CARD PRINCIPAL DO PERFIL */}
        <View style={[styles.profileHeaderCard, { backgroundColor: theme.card }]}>
          <View style={styles.photoContainer}>
            <View style={[styles.profileImagePlaceholder, { backgroundColor: theme.background }]}>
              {usuarioExibicao.imagem && usuarioExibicao.imagem !== 'null' && usuarioExibicao.imagem.trim() !== '' ? (
                <Image source={{ uri: usuarioExibicao.imagem }} style={styles.profileImage} />
              ) : (
                <Ionicons name="person" size={50} color="#B0B8C4" />
              )}
            </View>
            <TouchableOpacity style={styles.cameraBtn} activeOpacity={0.7} onPress={alterarFotoPerfil}>
              <Ionicons name="camera" size={16} color="white" />
            </TouchableOpacity>
          </View>

          <Text style={[styles.userName, { color: theme.text, fontSize: 20 * fontSizeScale }]}>{usuarioExibicao.nome} {usuarioExibicao.sobrenome}</Text>
          
          <View style={[styles.turmaBadge, { backgroundColor: theme.card, borderColor: theme.border }]}>
            <Ionicons name="school-outline" size={14} color={COLORS.primary} style={{ marginRight: 4 }} />
            <Text style={[styles.turmaText, { color: theme.text, fontSize: 13 * fontSizeScale }]}>{usuarioExibicao.turma}</Text>
          </View>
          
          <Text style={[styles.userDesc, { color: theme.text, fontSize: 14 * fontSizeScale }]}>{usuarioExibicao.descricao}</Text>

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
              <Text style={[styles.sectionTitle, { color: theme.text, fontSize: 16 * fontSizeScale }]}>Certificados</Text>
            </View>
            <TouchableOpacity style={styles.plusBtn} activeOpacity={0.7} onPress={abrirCriarCertificado}>
              <Ionicons name="add" size={20} color="white" />
            </TouchableOpacity>
          </View>
          
          {/* faltando o tema escuro */}
          {certificados.length === 0 ? (
            <View style={[styles.emptyContainer, { backgroundColor: theme.background, borderColor: theme.border }]}>
              <Ionicons name="document-text-outline" size={32} color={theme.text === 'white' ? '#666' : '#BBB'} />
              <Text style={[styles.emptyText, { color: theme.text, fontSize: 14 * fontSizeScale }]}>Nenhum certificado adicionado.</Text>
            </View>
          ) : (
            certificados.map(cert => (
              <View key={cert.id} style={[styles.certCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
                <View style={styles.certIconBadge}>
                  <FontAwesome5 name="award" size={22} color={COLORS.primary} />
                </View>

                <View style={styles.certInfo}>
                  <Text style={[styles.certTitle, { color: theme.text, fontSize: 15 * fontSizeScale }]} numberOfLines={1}>{cert.nome}</Text>
                  <Text style={[styles.certSub, { color: theme.text, fontSize: 12 * fontSizeScale }]} numberOfLines={2}>{cert.descricao || "Sem descrição"}</Text>
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
              <Text style={[styles.sectionTitle, { color: theme.text, fontSize: 16 * fontSizeScale }]}>Projetos Integradores</Text>
            </View>
          </View>
          
          {projetos.length === 0 ? (
            <View style={[styles.emptyContainer, { backgroundColor: theme.background, borderColor: theme.border }]}>
              <Ionicons name="code-slash" size={32} color={theme.text === 'white' ? '#666' : '#BBB'} />
              <Text style={[styles.emptyText, { color: theme.text, fontSize: 14 * fontSizeScale }]}>Nenhum projeto vinculado a você.</Text>
            </View>
          ) : (
            projetos.map(proj => (
              <View key={proj.id} style={styles.projectCard}>
                <View style={styles.projectMainInfo}>
                  <Text style={[styles.projectTitle, { color: theme.text, fontSize: 16 * fontSizeScale }]}>{proj.nome}</Text>
                  <Text style={[styles.projectSub, { color: theme.text, fontSize: 14 * fontSizeScale }]}>{proj.descricao || "Sem descrição disponível."}</Text>
                </View>
                
                {/* ✅ SISTEMA DE LINK REDIRECIONÁVEL ATIVADO */}
                <TouchableOpacity 
                  style={styles.repoLinkBtn} 
                  activeOpacity={0.7}
                  onPress={() => proj.link_repo ? Linking.openURL(proj.link_repo) : Alert.alert("Ops", "Link do repositório não disponível.")}
                >
                  <Text style={[styles.repoLinkText, { color: theme.text, fontSize: 14 * fontSizeScale }]}>Acessar Repositório</Text>
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
            <View style={[styles.modalContent, { backgroundColor: theme.card }]}>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>Editar Perfil</Text>
                <TouchableOpacity onPress={() => setModalPerfilVisible(false)} style={{ position: 'absolute', right: 20 }}>
                  <Feather name="x" size={20} color="white" />
                </TouchableOpacity>
              </View>

              <View style={styles.modalBody}>
                <View style={styles.inputContainer}>
                  <Text style={[styles.inputLabel, { color: theme.text, fontSize: 14 * fontSizeScale }]}>Nome</Text>
                  <TextInput placeholder="Digite seu nome..." value={perfilForm.nome} onChangeText={(text) => setPerfilForm({ ...perfilForm, nome: text })} style={[styles.input, { backgroundColor: theme.background, color: theme.text }]} placeholderTextColor="#94A3B8" editable={!savingPerfil} />
                </View>

                <View style={styles.inputContainer}>
                  <Text style={[styles.inputLabel, { color: theme.text, fontSize: 14 * fontSizeScale }]}>Sobrenome</Text>
                  <TextInput placeholder="Digite seu sobrenome..." value={perfilForm.sobrenome} onChangeText={(text) => setPerfilForm({ ...perfilForm, sobrenome: text })} style={[styles.input, { backgroundColor: theme.background, color: theme.text }]} placeholderTextColor="#94A3B8" editable={!savingPerfil} />
                </View>

                <View style={styles.inputContainer}>
                  <Text style={[styles.inputLabel, { color: theme.text, fontSize: 14 * fontSizeScale }]}>Bio / Descrição</Text>
                  <TextInput placeholder="Fale um pouco sobre você..." value={perfilForm.descricao} onChangeText={(text) => setPerfilForm({ ...perfilForm, descricao: text })} style={[styles.input, styles.inputMultiline, { backgroundColor: theme.background, color: theme.text }]} multiline numberOfLines={3} textAlignVertical="top" placeholderTextColor="#94A3B8" editable={!savingPerfil} />
                </View>

                <TouchableOpacity style={styles.saveBtn} onPress={salvarPerfil} disabled={savingPerfil} activeOpacity={0.8}>
                  {savingPerfil ? (
                    <ActivityIndicator size="small" color="white" />
                  ) : (
                    <Text style={styles.saveBtnText}>Salvar Alterações</Text>
                  )}
                </TouchableOpacity>
              </View>
            </View>
          </TouchableWithoutFeedback>
        </TouchableOpacity>
      </Modal>

      {/* 2. MODAL CERTIFICADO (CORRIGIDO) */}
      <Modal visible={modalCertVisible} transparent animationType="fade" onRequestClose={() => setModalCertVisible(false)}>
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setModalCertVisible(false)}>
          <TouchableWithoutFeedback>
            <View style={[styles.modalContent, { backgroundColor: theme.card }]}>
              <View style={styles.modalHeader}>
                {/* 🛠️ CORREÇÃO REALIZADA AQUI: O texto condicional foi extraído do style */}
                <Text style={styles.modalTitle}>{modalCertModo === "Criar" ? "Adicionar Certificado" : "Editar Certificado"}</Text>
                <TouchableOpacity onPress={() => setModalCertVisible(false)} style={{ position: 'absolute', right: 20 }}>
                  <Feather name="x" size={20} color="white" />
                </TouchableOpacity>
              </View>

              <View style={styles.modalBody}>
                <View style={styles.inputContainer}>
                  <Text style={[styles.inputLabel, { color: theme.text, fontSize: 14 * fontSizeScale }]}>Nome do Certificado</Text>
                  <TextInput placeholder="Ex: Curso de React Native" value={certForm.nome} onChangeText={(text) => setCertForm({ ...certForm, nome: text })} style={[styles.input, { backgroundColor: theme.background, color: theme.text }]} placeholderTextColor="#94A3B8" editable={!savingCert} />
                </View>

                <View style={styles.inputContainer}>
                  <Text style={[styles.inputLabel, { color: theme.text, fontSize: 14 * fontSizeScale }]}>Descrição / Instituição</Text>
                  <TextInput placeholder="Ex: Udemy - 40 horas" value={certForm.descricao} onChangeText={(text) => setCertForm({ ...certForm, descricao: text })} style={[styles.input, styles.inputMultiline, { backgroundColor: theme.background, color: theme.text }]} multiline numberOfLines={2} textAlignVertical="top" placeholderTextColor="#94A3B8" editable={!savingCert} />
                </View>

                <TouchableOpacity style={styles.saveBtn} onPress={salvarCertificado} disabled={savingCert} activeOpacity={0.8}>
                  {savingCert ? (
                    <ActivityIndicator size="small" color="white" />
                  ) : (
                    <Text style={styles.saveBtnText}>{modalCertModo === "Criar" ? "Adicionar" : "Salvar"}</Text>
                  )}
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
            <View style={[styles.modalContent, { backgroundColor: theme.card }]}>
              <View style={[styles.modalHeader, { backgroundColor: '#F44336' }]}>
                <Text style={styles.modalTitle}>Excluir Certificado</Text>
                <TouchableOpacity onPress={() => setModalExcluirVisible(false)} style={{ position: 'absolute', right: 20 }}>
                  <Feather name="x" size={20} color="white" />
                </TouchableOpacity>
              </View>

              <View style={styles.modalBody}>
                <Text style={[styles.deleteConfirmText, { color: theme.text, fontSize: 14 * fontSizeScale }]}>
                  Tem certeza de que deseja remover o certificado <Text style={{ fontWeight: 'bold', color: theme.text }}>"{certParaExcluir.nome}"</Text>? Essa ação não pode ser desfeita.
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
    backgroundColor: 'white', marginHorizontal: 20, marginTop: 20, marginBottom: 10, borderRadius: 24, padding: 24, alignItems: 'center', borderWidth: 1, borderColor: '#E2E8F0',
    shadowColor: "#0F172A", shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.05, shadowRadius: 12, elevation: 4 
  },
  photoContainer: { position: 'relative', marginBottom: 12 },
  profileImagePlaceholder: { 
    width: 105, height: 105, borderRadius: 55, backgroundColor: '#F1F5F9', justifyContent: 'center', alignItems: 'center', 
    borderWidth: 3, borderColor: '#0D9FFF', overflow: 'hidden' 
  },
  profileImage: { width: '100%', height: '100%', resizeMode: 'cover' }, 
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
  certCard: { backgroundColor: 'white', flexDirection: 'row', padding: 16, borderRadius: 18, marginBottom: 12, alignItems: 'center', borderWidth: 1, borderColor: '#E2E8F0', shadowColor: "#0F172A", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.03, shadowRadius: 8, elevation: 2 },
  certIconBadge: { width: 46, height: 46, borderRadius: 12, backgroundColor: '#EFF6FF', justifyContent: 'center', alignItems: 'center', marginRight: 14 },
  certInfo: { flex: 1, paddingRight: 8 },
  certTitle: { fontWeight: '600', fontSize: 15, color: '#1E293B' },
  certSub: { fontSize: 13, color: '#64748B', marginTop: 2 },
  certActionColumn: { flexDirection: 'column', gap: 8, justifyContent: 'center', alignItems: 'center', borderLeftWidth: 1, borderLeftColor: '#F1F5F9', paddingLeft: 12 },
  miniActionBtn: { padding: 4 },
  projectCard: { backgroundColor: 'white', padding: 20, borderRadius: 18, marginBottom: 12, borderWidth: 1, borderColor: '#E2E8F0', shadowColor: "#0F172A", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.03, shadowRadius: 8, elevation: 2 },
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