import React, { useState, useEffect } from 'react';
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
  const [avatarLoadFailed, setAvatarLoadFailed] = useState(false);

  useEffect(() => {
    setAvatarLoadFailed(false);
  }, [usuarioExibicao.imagem]);
  
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
      console.log("================================");
      console.log("👤 ID USUARIO:", idSalvo);
      console.log("================================");
      
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
        await carregarUsuario();
        await carregarDadosPerfil();
      };
      carregar();
    }, [])
  );

  // --- FUNÇÃO: SELECIONAR, ENVIAR OU REMOVER FOTO ---
 const alterarFotoPerfil = async () => {
  const idSalvo = await AsyncStorage.getItem('idUsuario');

  if (!idSalvo) {
    Alert.alert(
      "Erro",
      "Usuário não identificado. Faça login novamente."
    );
    return;
  }

  Alert.alert(
    "Foto de Perfil",
    "Escolha o que deseja fazer com sua foto:",
    [
      {
        text: "Escolher da Galeria",
        onPress: async () => {
          try {
            const dadosPermissao =
              await ImagePicker.requestMediaLibraryPermissionsAsync();

            if (!dadosPermissao.granted) {
              Alert.alert(
                "Permissão necessária",
                "Precisamos de acesso às fotos para alterar o perfil."
              );
              return;
            }

            const resultado =
              await ImagePicker.launchImageLibraryAsync({
                mediaTypes: ['images'],
                allowsEditing: true,
                aspect: [1, 1],
                quality: 0.3,
                base64: true,
              });

            if (resultado.canceled) {
              return;
            }

            const asset = resultado.assets[0];

            const {
              uri: fotoLocalUriRaw,
              fileName: assetName,
              base64: base64Data,
              mimeType: assetMimeType,
            } = asset;

            if (!base64Data) {
              throw new Error(
                "Não foi possível obter os dados da imagem."
              );
            }

            const fileName =
              assetName || `perfil_${idSalvo}.jpg`;

            const mimeType =
              assetMimeType || 'image/jpeg';

            console.log("================================");
            console.log("📸 FOTO SELECIONADA");
            console.log("👤 ID:", idSalvo);
            console.log("📄 Nome:", fileName);
            console.log("🖼️ Tipo:", mimeType);
            console.log("📦 Base64 recebido:", !!base64Data);
            console.log("🌐 Backend:", URL_BASE);
            console.log("================================");

            setCarregando(true);

            console.log(
              "📤 Enviando imagem para o backend..."
            );

            const respostaServidor = await fetch(
              `${URL_BASE}/perfil/upload-foto`,
              {
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
              }
            );

            const textoResposta =
              await respostaServidor.text();

            console.log(
              "📥 Status backend:",
              respostaServidor.status
            );

            console.log(
              "📥 Resposta backend:",
              textoResposta
            );

            if (!respostaServidor.ok) {
              throw new Error(
                `Upload falhou (${respostaServidor.status}): ${textoResposta}`
              );
            }

            let dadosServidor;

            try {
              dadosServidor = JSON.parse(textoResposta);
            } catch {
              throw new Error(
                "O servidor retornou uma resposta inválida."
              );
            }

            if (!dadosServidor.sucesso) {
              throw new Error(
                dadosServidor.mensagem ||
                dadosServidor.message ||
                "Erro ao fazer upload."
              );
            }

            console.log(
              "☁️ URL Cloudinary:",
              dadosServidor.imagem
            );

            atualizarFoto(dadosServidor.imagem);

            await carregarUsuario();

            Alert.alert(
              "Sucesso",
              "Foto de perfil atualizada!"
            );

          } catch (error) {
            console.error(
              "❌ Erro ao subir imagem:",
              error
            );

            Alert.alert(
              "Erro ao subir imagem",
              error.message ||
              "Não foi possível atualizar sua foto."
            );
          } finally {
            setCarregando(false);
          }
        },
      },
      {
        text: "Remover Foto Atual",
        style: "destructive",
        onPress: async () => {
          try {
            setCarregando(true);

            await atualizarFotoNoBackend(
              idSalvo,
              null
            );

          } catch (error) {
            Alert.alert(
              "Erro ao remover foto",
              error.message
            );
          } finally {
            setCarregando(false);
          }
        },
      },
      {
        text: "Cancelar",
        style: "cancel",
      },
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
        atualizarFoto(urlImagem);
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

      atualizarPerfil({
        nome: perfilForm.nome.trim(),
        sobrenome: perfilForm.sobrenome.trim(),
        descricao: perfilForm.descricao.trim()
      });
      
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
            usuarioId: user.idUsuario, 
            nome: certForm.nome, 
            descricao: certForm.descricao 
          }),
        });

        const dados = await response.json();

        if (dados.sucesso) {
          setCertificados([...certificados, dados.certificado]);
          Alert.alert("Sucesso", "Certificado adicionado ao banco!");
        } else {
          Alert.alert("Erro", dados.mensagem || "Erro ao adicionar certificado.");
        }

      } else {
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
          setCertificados(certificados.map(c => c.id === certForm.id ? { ...c, ...certForm } : c));
          Alert.alert("Sucesso", "Certificado atualizado com sucesso!");
        } else {
          Alert.alert("Erro", dados.mensagem || "Erro ao atualizar certificado.");
        }
      }

      setModalCertVisible(false);

    } catch (error) {
      console.error("❌ Erro ao salvar certificado no banco:", error);
      Alert.alert("Erro", "Não foi possível conectar ao servidor.");
    } finally {
      setSavingCert(false);
    }
  };

  const abrirExcluirCertificado = (cert) => {
    setCertParaExcluir({ id: cert.id, nome: cert.nome });
    setModalExcluirVisible(true);
  };

  const confirmarExclusao = async () => {
    try {
      const response = await fetch(`${URL_BASE}/perfil/certificado/${certParaExcluir.id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
      });

      const dados = await response.json();

      if (dados.sucesso) {
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
      <View style={[styles.container, { backgroundColor: theme.background }]}> 
        <Header nomeTela="Perfil" temGoBack={true} telaDestino={"Config"} carregando={true} />
        <ScrollView style={{ flex: 1 }} contentContainerStyle={{ flexGrow: 1, paddingTop: 0, paddingBottom: 40, gap: 18 }} showsVerticalScrollIndicator={false}>
          <View style={[styles.profileHeaderCard, { backgroundColor: theme.card, borderColor: theme.border, borderWidth: 1 }]}> 
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
      </View>
    );
  }

  return (
    <View style={[styles.container, { backgroundColor: theme.background }]}>
      <Header nomeTela="Perfil" temGoBack={true} telaDestino={"Config"} carregando={carregando} />
      
      <ScrollView style={{ flex: 1 }} contentContainerStyle={{ flexGrow: 1, paddingTop: 0, paddingBottom: 40 }} showsVerticalScrollIndicator={false}>
        
        {/* CARD PRINCIPAL DO PERFIL */}
        <View style={[styles.profileHeaderCard, { backgroundColor: theme.card, borderColor: theme.border, borderWidth: 1 }]}> 
          <View style={styles.photoContainer}>
            <View style={[styles.profileImagePlaceholder, { backgroundColor: theme.background }]}>
              {usuarioExibicao.imagem && usuarioExibicao.imagem !== 'null' && usuarioExibicao.imagem.trim() !== '' && !avatarLoadFailed ? (
                <Image source={{ uri: usuarioExibicao.imagem }} style={styles.profileImage} resizeMode="cover" onError={() => setAvatarLoadFailed(true)} />
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

      {/* 2. MODAL CERTIFICADO */}
      <Modal visible={modalCertVisible} transparent animationType="fade" onRequestClose={() => setModalCertVisible(false)}>
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setModalCertVisible(false)}>
          <TouchableWithoutFeedback>
            <View style={[styles.modalContent, { backgroundColor: theme.card }]}>
              <View style={styles.modalHeader}>
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
                  Tem certeza de que deseja excluir o certificado <Text style={{ fontWeight: 'bold' }}>{certParaExcluir.nome}</Text>?
                </Text>

                <View style={{ flexDirection: 'row', gap: 12, marginTop: 20 }}>
                  <TouchableOpacity 
                    style={[styles.saveBtn, { backgroundColor: '#94A3B8', flex: 1 }]} 
                    onPress={() => setModalExcluirVisible(false)}
                  >
                    <Text style={styles.saveBtnText}>Cancelar</Text>
                  </TouchableOpacity>
                  <TouchableOpacity 
                    style={[styles.saveBtn, { backgroundColor: '#F44336', flex: 1 }]} 
                    onPress={confirmarExclusao}
                  >
                    <Text style={styles.saveBtnText}>Excluir</Text>
                  </TouchableOpacity>
                </View>
              </View>
            </View>
          </TouchableWithoutFeedback>
        </TouchableOpacity>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  profileHeaderCard: {
    padding: 20,
    margin: 16,
    borderRadius: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  photoContainer: {
    position: 'relative',
    marginBottom: 16,
  },
  profileImagePlaceholder: {
    width: 100,
    height: 100,
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
  },
  profileImage: {
    width: '100%',
    height: '100%',
  },
  cameraBtn: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    backgroundColor: COLORS.primary,
    padding: 8,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  userName: {
    fontWeight: 'bold',
    marginBottom: 8,
    textAlign: 'center',
  },
  turmaBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    borderWidth: 1,
    marginBottom: 12,
  },
  turmaText: {
    fontWeight: '500',
  },
  userDesc: {
    textAlign: 'center',
    marginBottom: 16,
    paddingHorizontal: 10,
  },
  editProfileBtn: {
    flexDirection: 'row',
    backgroundColor: COLORS.primary,
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 12,
    alignItems: 'center',
    gap: 8,
  },
  editProfileBtnText: {
    color: 'white',
    fontWeight: '600',
  },
  section: {
    marginHorizontal: 16,
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  sectionTitle: {
    fontWeight: 'bold',
  },
  plusBtn: {
    backgroundColor: COLORS.primary,
    padding: 6,
    borderRadius: 8,
  },
  emptyContainer: {
    padding: 24,
    borderRadius: 12,
    borderWidth: 1,
    borderStyle: 'dashed',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  emptyText: {
    textAlign: 'center',
  },
  certCard: {
    flexDirection: 'row',
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    alignItems: 'center',
    marginBottom: 10,
  },
  certIconBadge: {
    width: 44,
    height: 44,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  certInfo: {
    flex: 1,
  },
  certTitle: {
    fontWeight: '600',
    marginBottom: 2,
  },
  certSub: {
    opacity: 0.7,
  },
  certActionColumn: {
    flexDirection: 'row',
    gap: 8,
  },
  miniActionBtn: {
    padding: 6,
  },
  projectCard: {
    padding: 16,
    borderRadius: 12,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: 'transparent',
  },
  projectMainInfo: {
    marginBottom: 12,
  },
  projectTitle: {
    fontWeight: 'bold',
    marginBottom: 4,
  },
  projectSub: {
    opacity: 0.8,
  },
  repoLinkBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  repoLinkText: {
    fontWeight: '600',
    color: COLORS.primary,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContent: {
    width: '100%',
    borderRadius: 16,
    overflow: 'hidden',
  },
  modalHeader: {
    padding: 16,
    backgroundColor: COLORS.primary,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  modalTitle: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  modalBody: {
    padding: 20,
  },
  inputContainer: {
    marginBottom: 16,
  },
  inputLabel: {
    marginBottom: 6,
    fontWeight: '500',
  },
  input: {
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 8,
    fontSize: 16,
  },
  inputMultiline: {
    minHeight: 80,
    textAlignVertical: 'top',
  },
  saveBtn: {
    backgroundColor: COLORS.primary,
    padding: 14,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  saveBtnText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
  deleteConfirmText: {
    textAlign: 'center',
  },
});