import React, { useState, useEffect, useRef } from "react";
import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView, Modal, TouchableWithoutFeedback, ActivityIndicator, Alert, Keyboard } from "react-native";
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

  const [mensagens, setMensagens] = useState([]);
  const [novaMensagem, setNovaMensagem] = useState("");
  const [carregando, setCarregando] = useState(true);
  const [usuarioLogadoId, setUsuarioLogadoId] = useState(null);

  const [menuVisible, setMenuVisible] = useState(false);
  const [editarVisible, setEditarVisible] = useState(false);
  const [textoEditando, setTextoEditando] = useState("");
  const [mensagemSelecionada, setMensagemSelecionada] = useState(null);

  // ==========================================
  // BUSCA DE DADOS (API + STORAGE)
  // ==========================================
  const carregarDados = async () => {
    try {
      setCarregando(true);

      const idSalvo = await AsyncStorage.getItem('idUsuario');
      const idUser = idSalvo ? parseInt(idSalvo) : null;
      setUsuarioLogadoId(idUser);

      if (topico?.id) {
        console.log("📡 Buscando mensagens na URL:", `${URL_MENSAGEM}/topico/${topico.id}`);
        const response = await fetch(`${URL_MENSAGEM}/topico/${topico.id}`);

        // MODIFICAÇÃO AQUI: Captura o erro real do servidor
        if (!response.ok) {
          const textoErro = await response.text();
          throw new Error(`Status ${response.status}: ${textoErro || "Sem detalhes"}`);
        }

        const dados = await response.json();

        const formatadas = dados.map(msg => ({
          id: msg.id,
          nome: msg.nome || "Usuário",
          texto: msg.texto,
          hora: formatarHora(msg.data),
          meu: msg.autorId === idUser
        }));

        setMensagens(formatadas);
      }
    } catch (error) {
      console.error("❌ Erro ao carregar dados:", error);
      // Alerta melhorado para te mostrar o culpado:
      Alert.alert("Erro no Carregamento", error.message);
    } finally {
      setCarregando(false);
    }
  };

  useEffect(() => {
    carregarDados();
  }, [topico]);

  const formatarHora = (dataString) => {
    if (!dataString) return "Agora";
    const d = new Date(dataString);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
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
      const response = await fetch(URL_MENSAGEM, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conteudo: novaMensagem.trim(),
          topicoId: topico.id,
          usuarioId: usuarioLogadoId
        })
      });

      // Captura o texto puro retornado pelo backend (seja JSON ou HTML de erro)
      const textoResposta = await response.text();

      if (!response.ok) {
        throw new Error(`Status ${response.status}: ${textoResposta || "Sem detalhes"}`);
      }

      setNovaMensagem("");
      Keyboard.dismiss();
      carregarDados(); // Recarrega o chat com a nova mensagem
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
          contentContainerStyle={{ paddingBottom: 100, paddingHorizontal: 10 }}
          onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
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
                  <View style={[styles.avatar, { backgroundColor: theme.primary }]}>
                    <Ionicons name="person" size={16} color="#fff" />
                  </View>
                )}

                <View style={styles.userInfo}>
                  {!item.meu && (
                    <View style={styles.nameRow}>
                      <Text
                        style={[
                          styles.message,
                          {
                            color: item.meu ? '#fff' : theme.text,
                            fontSize: 15 * fontSizeScale
                          }
                        ]}
                      ></Text>
                    </View>
                  )}
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
  {item.texto}
</Text>
                </View>
              </View>

              <View style={styles.footer}>
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
          ))}
        </ScrollView>
      )}

      {/* INPUT BARRA INFERIOR */}
      <View style={[styles.inputContainer, { backgroundColor: theme.card, borderTopColor: theme.border }]}>
        <TextInput
          placeholder="Escreva sua mensagem..."
          placeholderTextColor={theme.text + '80'}
          style={[styles.input, { color: theme.text, fontSize: 16 * fontSizeScale }]}
          value={novaMensagem}
          onChangeText={setNovaMensagem}
        />
        <TouchableOpacity style={[styles.sendButton, { backgroundColor: theme.primary }]} onPress={enviarMensagem}>
          <Ionicons name="send" size={18} color="#fff" />
        </TouchableOpacity>
      </View>

      {/* MODAL MENU OPÇÕES */}
      <Modal visible={menuVisible} transparent animationType="fade">
        <TouchableOpacity style={styles.overlay} activeOpacity={1} onPress={() => setMenuVisible(false)}>
          <View style={[styles.menuContainer, { backgroundColor: theme.card }]}>
            <TouchableOpacity style={styles.menuItem} onPress={abrirEditar}>
              <Feather name="edit-2" size={18} color="#2563EB" />
              <Text style={[styles.menuText, { color: theme.text }]}>Editar</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.menuItem} onPress={excluirMensagem}>
              <MaterialIcons name="delete-outline" size={20} color="#EF4444" />
              <Text style={[styles.menuText, { color: "#EF4444" }]}>Excluir</Text>
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      </Modal>

      {/* ... (Repita a lógica de temas no Modal de Edição também) */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#ffffff" },
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
  pathContainer: { flexDirection: "row", alignItems: "center", paddingHorizontal: 15, marginTop: 12, marginBottom: 10 },
  pathText: { color: "#777", fontSize: 13, marginRight: 4, maxWidth: 100 },
  pathActive: { color: "#2563EB", fontSize: 13, fontWeight: "700", marginLeft: 4 },
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
  message: { fontSize: 13, color: "#333", lineHeight: 18 },
  footer: { marginTop: 6, flexDirection: "row", justifyContent: "space-between", alignItems: "center", minWidth: 45 },
  time: { fontSize: 10, color: "#888", marginRight: 5 },
  moreButton: { padding: 2, marginLeft: 5 },
  inputContainer: { position: "absolute", bottom: 15, left: 10, right: 10, backgroundColor: "#fff", borderRadius: 18, flexDirection: "row", alignItems: "center", paddingHorizontal: 10, height: 50, elevation: 3 },
  clipButton: { marginRight: 8 },
  input: { flex: 1, fontSize: 14 },
  sendButton: { width: 36, height: 36, borderRadius: 18, backgroundColor: COLORS.primary, justifyContent: "center", alignItems: "center" },
  overlay: { flex: 1, backgroundColor: "rgba(0,0,0,0.2)", justifyContent: "center", alignItems: "center" },
  menuContainer: { width: 160, backgroundColor: "#fff", borderRadius: 16, paddingVertical: 6, elevation: 6 },
  menuItem: { flexDirection: "row", alignItems: "center", paddingVertical: 12, paddingHorizontal: 16 },
  menuText: { marginLeft: 12, fontSize: 14, color: "#333", fontWeight: "600" },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0, 0, 0, 0.67)', justifyContent: 'center', padding: 15 },
  modalContent: { backgroundColor: 'white', borderRadius: 25, overflow: 'hidden' },
  modalHeader: { backgroundColor: COLORS.primary, flexDirection: 'row', padding: 20, alignItems: 'center', justifyContent: 'center' },
  modalTitle: { color: 'white', fontSize: 18, fontWeight: 'bold' },
  modalBody: { padding: 20 },
  inputContainerModal: { marginBottom: 15 },
  inputLabel: { fontSize: 14, fontWeight: "600", color: "#333", marginBottom: 6, paddingLeft: 2 },
  inputField: { borderWidth: 1, borderColor: '#ddd', borderRadius: 12, padding: 12 },
  saveBtn: { backgroundColor: COLORS.primary, padding: 15, borderRadius: 12, alignItems: 'center', marginTop: 10 },
  saveBtnText: { color: 'white', fontWeight: 'bold' }
});