import React, { useState, useEffect, useRef } from "react";
import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView, Modal, TouchableWithoutFeedback, ActivityIndicator, Alert, Keyboard, Image, KeyboardAvoidingView, Platform } from "react-native";
import { Ionicons, Feather, MaterialIcons } from "@expo/vector-icons";
import Header from "../components/Header";
import Skeleton from "../components/Skeleton";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useTheme } from '../context/ThemeContext';
import { URL_BASE } from '../config/backend';

const COLORS = { primary: "#0e68d6" };

const URL_MENSAGEM = URL_BASE.endsWith('/') ? `${URL_BASE}conversa` : `${URL_BASE}/conversa`;

export default function ConversaScreen({ navigation, route }) {
  const { theme, fontSizeScale } = useTheme();
  const forumNome = route.params?.forum || "Fórum";
  // Agora recebemos o objeto completo do tópico vindo da tela anterior
  const topico = route.params?.topico;

  const scrollViewRef = useRef();

  const mostrarOpcaoPerfil = (usuario) => {
    if (!usuario?.id) return;
    Alert.alert(usuario.nome || "Usuário", "O que deseja fazer?", [
      { text: "Cancelar", style: "cancel" },
      {
        text: "Ver perfil",
        onPress: () => {
          setParticipantesVisible(false);
          navigation.navigate("Perfil", { usuarioId: usuario.id });
        }
      }
    ]);
  };

  const [mensagens, setMensagens] = useState([]);
  const [novaMensagem, setNovaMensagem] = useState("");
  const [carregando, setCarregando] = useState(true);
  const [usuarioLogadoId, setUsuarioLogadoId] = useState(null);

  // Normaliza URLs de imagens do banco de dados
  const normalizarUrlFoto = (fotoValue) => {
    if (!fotoValue || typeof fotoValue !== 'string') return null;
    const trimmed = fotoValue.trim();
    if (!trimmed || trimmed.toLowerCase() === 'null') return null;
    
    // Se já é uma URL completa
    if (/^https?:\/\//i.test(trimmed)) return trimmed;
    
    // Se é um caminho relativo da API
    if (/^\//.test(trimmed)) return `${URL_BASE}${trimmed}`;
    
    // Se é do Cloudinary (sem protocol)
    if (/^\/\//.test(trimmed)) return `https:${trimmed}`;
    
    // Tenta como URL do Cloudinary
    if (!trimmed.includes('/')) return `https://res.cloudinary.com/dw0pxfap3/${trimmed}`;
    
    return null;
  };

  const [menuVisible, setMenuVisible] = useState(false);
  const [editarVisible, setEditarVisible] = useState(false);
  const [textoEditando, setTextoEditando] = useState("");
  const [mensagemSelecionada, setMensagemSelecionada] = useState(null);
  const [participantesCount, setParticipantesCount] = useState(0);
  const [participantes, setParticipantes] = useState([]);
  const [participantesVisible, setParticipantesVisible] = useState(false);
  
  // Estados para o sistema de menções
  const [usuariosMencaoVisivel, setUsuariosMencaoVisivel] = useState(false);
  const [usuariosFiltrados, setUsuariosFiltrados] = useState([]);
  const [usuariosDisponiveisMencao, setUsuariosDisponiveisMencao] = useState([]);
  const [mencaoAtiva, setMencaoAtiva] = useState(false);
  const [textoBuscaMencao, setTextoBuscaMencao] = useState("");
  const [usuariosMencaoDaTela, setUsuariosMencaoDaTela] = useState(new Set());

  // ==========================================
  // BUSCA DE DADOS (API + STORAGE)
  // ==========================================
  const carregarDados = async (semLoading = false) => {
    try {
      if (!semLoading) setCarregando(true);

      const idSalvo = await AsyncStorage.getItem('idUsuario');
      const idUser = idSalvo ? parseInt(idSalvo) : null;
      if (idUser && !usuarioLogadoId) {
        setUsuarioLogadoId(idUser);
      }

      if (topico?.id) {
        const response = await fetch(`${URL_MENSAGEM}/topico/${topico.id}`);

        if (!response.ok) {
          const textoErro = await response.text();
          throw new Error(`Status ${response.status}: ${textoErro || "Sem detalhes"}`);
        }

        const dados = await response.json();

        const formatadas = dados.map(msg => ({
          id: msg.id,
          autorId: msg.autorId,
          nome: msg.nome || "Usuário",
          texto: msg.texto,
          hora: formatarHora(msg.data),
          foto: normalizarUrlFoto(msg.foto),
          meu: msg.autorId === idUser
        }));

        const participantesUnicos = new Map();
        dados.forEach(msg => {
          const id = msg.autorId;
          if (id !== null && id !== undefined && !participantesUnicos.has(id)) {
            participantesUnicos.set(id, {
              id,
              nome: msg.nome || "Usuário",
              foto: normalizarUrlFoto(msg.foto),
            });
          }
        });
        const participantesAtuais = Array.from(participantesUnicos.values());
        setParticipantes(participantesAtuais);
        setParticipantesCount(participantesAtuais.length);

        // Só atualiza se houver mudança
        if (JSON.stringify(formatadas) !== JSON.stringify(mensagens)) {
          setMensagens(formatadas);
        }
      }
    } catch (error) {
      console.error("❌ Erro ao carregar dados:", error);
      if (!semLoading) Alert.alert("Erro no Carregamento", error.message);
    } finally {
      if (!semLoading) setCarregando(false);
    }
  };

  useEffect(() => {
    if (!topico?.id) return;

    carregarDados();
    carregarUsuariosDoTopico();

    // Intervalo para atualizar em tempo real (silenciosamente)
    const intervaloAtualizacao = setInterval(() => {
      carregarDados(true);
      carregarUsuariosDoTopico();
    }, 6000); // 6 segundos

    // Sincroniza quando o app volta para primeiro plano
    const subscription = require('react-native').AppState.addEventListener('change', handleAppStateChange);

    return () => {
      clearInterval(intervaloAtualizacao);
      subscription?.remove();
    };
  }, [topico?.id]);

  const handleAppStateChange = (state) => {
    if (state === 'active') {
      carregarDados(true);
      carregarUsuariosDoTopico();
    }
  };

  const carregarUsuariosDoTopico = async () => {
    try {
      if (topico?.id) {
        const response = await fetch(`${URL_MENSAGEM}/topico/${topico.id}`);
        if (response.ok) {
          const dados = await response.json();
          // Extrai usuários únicos das mensagens
          const usuariosUnicos = new Set();
          dados.forEach(msg => {
            if (msg.nome && msg.id_Usuario !== usuarioLogadoId) {
              usuariosUnicos.add({ id: msg.id_Usuario, nome: msg.nome });
            }
          });
          setUsuariosDisponiveisMencao(Array.from(usuariosUnicos));
        }
      }
    } catch (error) {
      console.error("❌ Erro ao carregar usuários:", error);
    }
  };

  const formatarHora = (dataString) => {
    if (!dataString) return "Agora";
    const d = new Date(dataString);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const handleMudancaTexto = (texto) => {
    setNovaMensagem(texto);
    
    // Detecta se há @ no texto
    const ultimaArroba = texto.lastIndexOf('@');
    if (ultimaArroba !== -1) {
      const textoAposFinal = texto.substring(ultimaArroba + 1);
      // Se não tem espaço após @, ativa modo mencao
      if (!textoAposFinal.includes(' ')) {
        setMencaoAtiva(true);
        setTextoBuscaMencao(textoAposFinal.toLowerCase());
        
        // Filtra usuários que correspondem
        const filtrados = usuariosDisponiveisMencao.filter(u =>
          u.nome.toLowerCase().includes(textoAposFinal.toLowerCase())
        );
        setUsuariosFiltrados(filtrados);
        setUsuariosMencaoVisivel(filtrados.length > 0);
      } else {
        setMencaoAtiva(false);
        setUsuariosMencaoVisivel(false);
      }
    } else {
      setMencaoAtiva(false);
      setUsuariosMencaoVisivel(false);
    }
  };

  const inserirMencao = (usuario) => {
    const ultimaArroba = novaMensagem.lastIndexOf('@');
    const textoAntes = novaMensagem.substring(0, ultimaArroba);
    const novoTexto = textoAntes + '@' + usuario.nome + ' ';
    
    setNovaMensagem(novoTexto);
    setUsuariosMencaoDaTela(prev => new Set(prev).add(usuario.nome));
    setUsuariosMencaoVisivel(false);
    setMencaoAtiva(false);
    setTextoBuscaMencao("");
  };

  const renderizarMensagemComMencoes = (texto) => {
    // Detecta padrão @NomePessoa
    const padrao = /@(\w+)/g;
    const partes = [];
    let ultimoIndice = 0;
    let match;

    while ((match = padrao.exec(texto)) !== null) {
      // Texto antes da menção
      if (match.index > ultimoIndice) {
        partes.push({
          tipo: 'texto',
          conteudo: texto.substring(ultimoIndice, match.index)
        });
      }
      // Menção
      partes.push({
        tipo: 'mencao',
        conteudo: match[0]
      });
      ultimoIndice = match.index + match[0].length;
    }

    // Texto final
    if (ultimoIndice < texto.length) {
      partes.push({
        tipo: 'texto',
        conteudo: texto.substring(ultimoIndice)
      });
    }

    if (partes.length === 0) {
      return texto;
    }

    return partes;
  };

  // ==========================================
  // OPERAÇÕES DA API (POST, PUT, DELETE)
  // ==========================================
  const enviarMensagem = async () => {
    if (!novaMensagem.trim()) return;

    // Verificações de segurança para conferir no console do celular
    console.log("📌 Dados locais antes do envio:");
    console.log("- ID do Tópico:", topico?.id);
    console.log("- ID do Usuário Logado:", usuarioLogadoId);

    if (!topico?.id) {
      Alert.alert("Erro", "O ID do tópico está indefinido (undefined).");
      return;
    }
    if (!usuarioLogadoId) {
      Alert.alert("Erro", "O ID do usuário logado não foi encontrado no AsyncStorage.");
      return;
    }

    try {
      const payload = {
        conteudo: novaMensagem.trim(),
        topicoId: topico.id,
        usuarioId: usuarioLogadoId
      };

      const response = await fetch(URL_MENSAGEM, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      // Captura o texto puro retornado pelo backend (seja JSON ou HTML de erro)
      const textoResposta = await response.text();

      if (!response.ok) {
        throw new Error(`Status ${response.status}: ${textoResposta || "Sem detalhes"}`);
      }

      // Notifica usuários mencionados
      if (usuariosMencaoDaTela.size > 0) {
        for (const nomeMencionado of usuariosMencaoDaTela) {
          const usuarioMencionado = usuariosDisponiveisMencao.find(
            u => u.nome.toLowerCase() === nomeMencionado.toLowerCase()
          );
          
          if (usuarioMencionado) {
            try {
              await fetch(`${URL_BASE}/notifications`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  usuario_id: usuarioMencionado.id,
                  tipo: 'Forum',
                  titulo: 'Você foi mencionado',
                  subtitulo: `Você foi mencionado no tópico "${topico.titulo}"`,
                  tela_destino: 'Conversa',
                  parametros: JSON.stringify({ topicoId: topico.id }),
                  entidade_id: topico.id
                })
              });
            } catch (err) {
              console.error('❌ Erro ao enviar notificação de menção:', err);
            }
          }
        }
      }

      // Adiciona a mensagem localmente sem recarregar tudo
      const novaMensagemObj = {
        id: Math.random(),
        nome: "Você",
        texto: novaMensagem.trim(),
        hora: formatarHora(new Date().toISOString()),
        foto: null,
        meu: true
      };
      
      setMensagens(prev => [...prev, novaMensagemObj]);
      setNovaMensagem("");
      setUsuariosMencaoDaTela(new Set());
      Keyboard.dismiss();
    } catch (error) {
      console.error("❌ Erro detalhado no envio:", error);
      Alert.alert("Erro ao Enviar", error.message);
    }
  };

  const salvarEdicao = async () => {
    if (!textoEditando.trim() || !mensagemSelecionada) return;

    try {
      const response = await fetch(`${URL_MENSAGEM}/${mensagemSelecionada.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conteudo: textoEditando.trim(),
          usuarioId: usuarioLogadoId
        })
      });

      if (!response.ok) throw new Error("Falha ao salvar edição.");

      setEditarVisible(false);
      carregarDados();
    } catch (error) {
      Alert.alert("Erro", error.message);
    }
  };

  const excluirMensagem = async () => {
    if (!mensagemSelecionada) return;

    try {
      const response = await fetch(`${URL_MENSAGEM}/${mensagemSelecionada.id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuarioId: usuarioLogadoId })
      });

      if (!response.ok) throw new Error("Não foi possível excluir a mensagem.");

      setMenuVisible(false);
      setMensagens(prev => prev.filter(item => item.id !== mensagemSelecionada.id));
    } catch (error) {
      Alert.alert("Erro", error.message);
    }
  };

  // ==========================================
  // GERENCIAMENTO DOS MODAIS
  // ==========================================
  const abrirMenu = (item) => {
    setMensagemSelecionada(item);
    setMenuVisible(true);
  };

  const abrirEditar = () => {
    setTextoEditando(mensagemSelecionada.texto);
    setMenuVisible(false);
    setEditarVisible(true);
  };

  return (
    <View style={[styles.container, { backgroundColor: theme.background }]}>
      <Header nomeTela={"Conversa"} temGoBack={true} telaDestino={"Titulo"} carregando={carregando} />

      <View style={styles.pathContainer}>
        <Text style={[styles.pathText, { color: theme.text }]}>{forumNome}</Text>
        <Ionicons name="chevron-forward" size={14} color={theme.text} />
        <Text style={[styles.pathText, { color: theme.text }]} numberOfLines={1}>{topico?.titulo || "Tópico"}</Text>
        <Ionicons name="chevron-forward" size={14} color={theme.text} />
        <Text style={[styles.pathActive, { color: theme.primary }]}>Conversa</Text>
      </View>

      <TouchableOpacity
        style={[styles.infoContainer, { backgroundColor: theme.card, borderBottomColor: theme.border }]}
        onPress={() => setParticipantesVisible(true)}
        activeOpacity={0.7}
      >
        <View style={styles.participantesInfo}>
          <Ionicons name="people" size={16} color={theme.primary} />
          <Text style={[styles.participantesText, { color: theme.text }]}>
            {participantesCount} {participantesCount === 1 ? 'participante' : 'participantes'}
          </Text>
        </View>
        <Ionicons name="chevron-forward" size={18} color={theme.text} />
      </TouchableOpacity>

      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        {carregando ? (
          <View style={{ flex: 1, padding: 20 }}>
            {[1, 2, 3].map((item) => (
              <Skeleton key={item} width="100%" height={120} borderRadius={18} style={{ marginBottom: 16 }} />
            ))}
          </View>
        ) : (
          <ScrollView
            ref={scrollViewRef}
            showsVerticalScrollIndicator={false}
            contentContainerStyle={{ paddingBottom: 150, paddingHorizontal: 10 }}
            onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
            keyboardShouldPersistTaps="handled"
          >
          {mensagens.map((item) => (
            <View
              key={item.id.toString()}
              style={[
                styles.messageCard,
                item.meu ? styles.myMessageCard : [styles.otherMessageCard, { backgroundColor: theme.card }]
              ]}
            >
              <View style={styles.topRow}>
                {!item.meu && (
                  <TouchableOpacity
                    style={[styles.avatar, { backgroundColor: theme.primary }]}
                    onPress={() => mostrarOpcaoPerfil({ id: item.autorId, nome: item.nome, foto: item.foto })}
                  >
                    {item.foto ? (
                      <>
                        <Image
                          source={{ uri: item.foto }}
                          style={styles.avatarImage}
                          onLoad={() => console.log('✅ Foto carregada:', item.foto)}
                          onError={(e) => console.log('❌ Erro ao carregar foto:', item.foto, e.nativeEvent.error)}
                        />
                      </>
                    ) : (
                      <>
                        <Ionicons name="person" size={16} color="#fff" />
                        {console.log('ℹ️ Sem foto para usuário:', item.nome, 'Valor bruto:', item.foto)}
                      </>
                    )}
                  </TouchableOpacity>
                )}

                <View style={styles.userInfo}>
                  {!item.meu && (
                    <View style={styles.nameRow}>
                      <Text
                        style={[
                          styles.name,
                          {
                            color: item.meu ? '#fff' : theme.text,
                            fontSize: 13 * fontSizeScale,
                            fontWeight: '600'
                          }
                        ]}
                      >{item.nome}</Text>
                    </View>
                  )}
                  {/* RECURSO DE RESPOSTAS SERÁ IMPLEMENTADO QUANDO AS COLUNAS FOREM ADICIONADAS AO BANCO */}
                  <Text
                    style={[
                      styles.message,
                      {
                        color: item.meu ? "#FFFFFF" : theme.text,
                        fontSize: 15 * fontSizeScale,
                        lineHeight: 22,
                      },
                    ]}
                  >
                    {(() => {
                      const partes = renderizarMensagemComMencoes(item.texto);
                      if (typeof partes === 'string') {
                        return partes;
                      }
                      return partes.map((parte, idx) => (
                        <Text key={idx} style={parte.tipo === 'mencao' ? { fontWeight: 'bold', color: '#FFD700' } : {}}>
                          {parte.conteudo}
                        </Text>
                      ));
                    })()}
                  </Text>
                </View>
              </View>

              <View style={styles.footer}>
                <View style={styles.footerLeft}>
                  <Text
                    style={[
                      styles.time,
                      {
                        color: item.meu ? "rgba(255,255,255,0.75)" : "#888",
                        fontSize: 10 * fontSizeScale,
                      },
                    ]}
                  >
                    {item.hora}
                  </Text>

                  {/* RESPOSTASCOUNT REMOVIDO TEMPORARIAMENTE */}
                </View>

                <View style={styles.footerRight}>
                  {/* BOTÃO DE RESPOSTA SERÁ ATIVADO QUANDO AS COLUNAS FOREM ADICIONADAS AO BANCO */}
                  {/* {!item.meu && (
                    <TouchableOpacity
                      style={styles.replyButton}
                      onPress={() => responderMensagem(item)}
                    >
                      <MaterialIcons name="reply" size={16} color="#888" />
                    </TouchableOpacity>
                  )} */}

                  {item.meu && (
                    <TouchableOpacity
                      style={styles.moreButton}
                      onPress={() => abrirMenu(item)}
                    >
                      <Feather
                        name="more-vertical"
                        size={15}
                        color="#FFFFFF"
                      />
                    </TouchableOpacity>
                  )}
                </View>
              </View>
            </View>
          ))}
          </ScrollView>
        )}

        {/* CONTAINER BOTTOM COM PREVIEW + INPUT */}
        <View style={[styles.bottomContainer, { backgroundColor: theme.background }]}>
        {/* INPUT BARRA INFERIOR */}
        <View style={[styles.inputContainer, { backgroundColor: theme.card, borderTopColor: theme.border }]}>
          <TextInput
            placeholder="Escreva sua mensagem... (use @ para mencionar)"
            placeholderTextColor={theme.text + '80'}
            style={[styles.input, { color: theme.text, fontSize: 16 * fontSizeScale }]}
            value={novaMensagem}
            onChangeText={handleMudancaTexto}
          />
          <TouchableOpacity style={[styles.sendButton, { backgroundColor: theme.primary }]} onPress={enviarMensagem}>
            <Ionicons name="send" size={18} color="#fff" />
          </TouchableOpacity>
        </View>

        {/* MODAL DE SUGESTÕES DE MENÇÃO */}
        {usuariosMencaoVisivel && (
          <View style={[styles.mencaoContainer, { backgroundColor: theme.card, borderTopColor: theme.primary }]}>
            <ScrollView style={{ maxHeight: 150 }} nestedScrollEnabled={true}>
              {usuariosFiltrados.map((usuario, idx) => (
                <TouchableOpacity
                  key={idx}
                  style={[styles.mencaoItem, { backgroundColor: theme.card, borderBottomColor: theme.border }]}
                  onPress={() => inserirMencao(usuario)}
                >
                  <MaterialIcons name="person" size={16} color={theme.primary} />
                  <Text style={[styles.mencaoText, { color: theme.text }]}>@{usuario.nome}</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        )}
        </View>
      </KeyboardAvoidingView>

      {/* MODAL MENU OPÇÕES */}
      <Modal visible={menuVisible} transparent animationType="fade">
        <TouchableOpacity style={styles.overlay} activeOpacity={1} onPress={() => setMenuVisible(false)}>
          <View style={[styles.menuContainer, { backgroundColor: theme.card }]}>
            {/* RECURSO DE RESPOSTA REMOVIDO - USAR MENÇÕES @USUARIO */}
            {mensagemSelecionada?.meu && (
              <>
                <TouchableOpacity style={styles.menuItem} onPress={abrirEditar}>
                  <Feather name="edit-2" size={18} color="#2563EB" />
                  <Text style={[styles.menuText, { color: theme.text }]}>Editar</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.menuItem} onPress={excluirMensagem}>
                  <MaterialIcons name="delete-outline" size={20} color="#EF4444" />
                  <Text style={[styles.menuText, { color: "#EF4444" }]}>Excluir</Text>
                </TouchableOpacity>
              </>
            )}
          </View>
        </TouchableOpacity>
      </Modal>

      <Modal visible={participantesVisible} transparent animationType="fade" onRequestClose={() => setParticipantesVisible(false)}>
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setParticipantesVisible(false)}>
          <TouchableWithoutFeedback>
            <View style={[styles.modalContent, { backgroundColor: theme.card, width: '90%', maxHeight: '75%' }]}>
              <View style={[styles.modalHeader, { backgroundColor: theme.primary }]}> 
                <Text style={styles.modalTitle}>Participantes</Text>
                <TouchableOpacity style={styles.modalCloseButton} onPress={() => setParticipantesVisible(false)}>
                  <Ionicons name="close-circle" size={30} color="white" />
                </TouchableOpacity>
              </View>
              <ScrollView contentContainerStyle={{ padding: 12 }}>
                {participantes.map((participante) => (
                  <View key={String(participante.id)} style={styles.participanteItem}>
                    <TouchableOpacity
                      style={[styles.participanteAvatar, { backgroundColor: theme.primary }]}
                      onPress={() => mostrarOpcaoPerfil(participante)}
                    >
                      {participante.foto ? (
                        <Image source={{ uri: participante.foto }} style={styles.participanteAvatarImage} />
                      ) : (
                        <Ionicons name="person" size={18} color="#fff" />
                      )}
                    </TouchableOpacity>
                    <Text style={[styles.participanteNome, { color: theme.text }]}>{participante.nome}</Text>
                  </View>
                ))}
              </ScrollView>
            </View>
          </TouchableWithoutFeedback>
        </TouchableOpacity>
      </Modal>

      {/* ... (Repita a lógica de temas no Modal de Edição também) */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#ffffff" },
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
  pathContainer: { flexDirection: "row", alignItems: "center", paddingHorizontal: 15, marginTop: 12, marginBottom: 10, flexWrap: 'wrap' },
  pathText: { color: "#777", fontSize: 13, marginRight: 4, flexShrink: 1, minWidth: 0 },
  pathActive: { color: "#2563EB", fontSize: 13, fontWeight: "700", marginLeft: 4 },
  infoContainer: { paddingHorizontal: 15, paddingVertical: 10, borderBottomWidth: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'flex-start' },
  participantesInfo: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  participantesText: { fontSize: 13, fontWeight: '500' },
  messageCard: { marginBottom: 10, borderRadius: 16, padding: 12, maxWidth: "80%", elevation: 1 },
  myMessageCard: {
    backgroundColor: COLORS.primary,
    alignSelf: "flex-end",
    borderTopRightRadius: 6,
    borderTopLeftRadius: 18,
    borderBottomLeftRadius: 18,
    borderBottomRightRadius: 18,

    shadowColor: "#000",
    shadowOpacity: 0.12,
    shadowRadius: 5,
    shadowOffset: {
      width: 0,
      height: 2,
    },

    elevation: 3,
  },
  otherMessageCard: {
    backgroundColor: "#FFFFFF",
    alignSelf: "flex-start",
    borderTopLeftRadius: 6,
    borderTopRightRadius: 18,
    borderBottomLeftRadius: 18,
    borderBottomRightRadius: 18,

    shadowColor: "#000",
    shadowOpacity: 0.08,
    shadowRadius: 5,
    shadowOffset: {
      width: 0,
      height: 2,
    },

    elevation: 2,
  },
  topRow: { flexDirection: "row", alignItems: "flex-start" },
  avatar: { width: 32, height: 32, borderRadius: 16, backgroundColor: COLORS.primary, justifyContent: "center", alignItems: "center", marginRight: 10, marginTop: 2 },
  userInfo: { justifyContent: "center", flexShrink: 1 },
  nameRow: { flexDirection: "row", alignItems: "center", marginBottom: 4 },
  name: { fontSize: 13, fontWeight: "700", color: "#222" },
  avatarImage: { width: 32, height: 32, borderRadius: 16 },
  message: { fontSize: 13, color: "#333", lineHeight: 18 },
  footer: { marginTop: 6, flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  footerLeft: { flexDirection: "row", alignItems: "center", gap: 6 },
  footerRight: { flexDirection: "row", alignItems: "center" },
  time: { fontSize: 10, color: "#888", marginRight: 5 },
  respostasIndicator: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 6, paddingVertical: 2, borderRadius: 10, gap: 2 },
  respostasText: { fontWeight: '600', fontSize: 10 },
  replyButton: { padding: 4, marginLeft: 6 },
  moreButton: { padding: 2, marginLeft: 5 },
  bottomContainer: { flexDirection: 'column', paddingHorizontal: 10, paddingBottom: 15, paddingTop: 8 },
  replyPreview: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, paddingVertical: 8, marginBottom: 8, borderLeftWidth: 3, borderRadius: 8 },
  replyPreviewContent: { flex: 1, flexDirection: 'row', alignItems: 'center' },
  replyPreviewName: { fontWeight: '600', marginBottom: 2 },
  replyPreviewText: { opacity: 0.7 },
  quotedMessage: { paddingHorizontal: 10, paddingVertical: 8, marginVertical: 6, borderLeftWidth: 4, borderRadius: 8, marginBottom: 8 },
  quotedName: { fontWeight: '700', marginBottom: 3 },
  quotedText: { lineHeight: 18, opacity: 0.85, marginTop: 2 },
  inputContainer: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 10, height: 50, borderRadius: 18, elevation: 3, borderTopWidth: 1 },
  clipButton: { marginRight: 8 },
  input: { flex: 1, fontSize: 14 },
  sendButton: { width: 36, height: 36, borderRadius: 18, backgroundColor: COLORS.primary, justifyContent: "center", alignItems: "center" },
  overlay: { flex: 1, backgroundColor: "rgba(0,0,0,0.2)", justifyContent: "center", alignItems: "center" },
  menuContainer: { minWidth: 140, width: "auto", backgroundColor: "#fff", borderRadius: 16, paddingVertical: 6, elevation: 6 },
  menuItem: { flexDirection: "row", alignItems: "center", paddingVertical: 12, paddingHorizontal: 16 },
  menuText: { marginLeft: 12, fontSize: 14, color: "#333", fontWeight: "600" },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0, 0, 0, 0.67)', justifyContent: 'center', padding: 15 },
  modalContent: { backgroundColor: 'white', borderRadius: 25, overflow: 'hidden' },
  modalHeader: { backgroundColor: COLORS.primary, flexDirection: 'row', padding: 20, alignItems: 'center', justifyContent: 'center' },
  modalTitle: { color: 'white', fontSize: 18, fontWeight: 'bold' },
  modalCloseButton: { position: 'absolute', right: 18, top: 16 },
  modalBody: { padding: 20 },
  inputContainerModal: { marginBottom: 15 },
  inputLabel: { fontSize: 14, fontWeight: "600", color: "#333", marginBottom: 6, paddingLeft: 2 },
  inputField: { borderWidth: 1, borderColor: '#ddd', borderRadius: 12, padding: 12 },
  saveBtn: { backgroundColor: COLORS.primary, padding: 15, borderRadius: 12, alignItems: 'center', marginTop: 10 },
  saveBtnText: { color: 'white', fontWeight: 'bold' },
  mencaoContainer: { borderTopWidth: 2, paddingVertical: 8, maxHeight: 150 },
  mencaoItem: { flexDirection: 'row', alignItems: 'center', paddingVertical: 10, paddingHorizontal: 12, borderBottomWidth: 1 },
  mencaoText: { marginLeft: 10, fontSize: 14, fontWeight: '500' },
  participanteItem: { flexDirection: 'row', alignItems: 'center', paddingVertical: 10, paddingHorizontal: 8 },
  participanteAvatar: { width: 38, height: 38, borderRadius: 19, justifyContent: 'center', alignItems: 'center', marginRight: 12, overflow: 'hidden' },
  participanteAvatarImage: { width: '100%', height: '100%' },
  participanteNome: { fontSize: 15, fontWeight: '500' }
});