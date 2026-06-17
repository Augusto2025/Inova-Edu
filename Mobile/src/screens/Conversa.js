import React, { useState, useEffect, useRef } from "react";
import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView, Modal, TouchableWithoutFeedback, ActivityIndicator, Alert, Keyboard } from "react-native";
import { Ionicons, Feather, MaterialIcons } from "@expo/vector-icons";
import Header from "../components/Header";
import AsyncStorage from '@react-native-async-storage/async-storage';

const COLORS = { primary: "#0e68d6" };

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');
const URL_MENSAGEM = URL_BASE.endsWith('/') ? `${URL_BASE}mensagem` : `${URL_BASE}/mensagem`;

export default function ConversaScreen({ navigation, route }) {
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
      
      // 1. Pega quem está logado no celular
      const idSalvo = await AsyncStorage.getItem('idUsuario');
      const idUser = idSalvo ? parseInt(idSalvo) : null;
      setUsuarioLogadoId(idUser);

      // 2. Busca as mensagens do tópico na API
      if (topico?.id) {
        const response = await fetch(`${URL_MENSAGEM}/topico/${topico.id}`);
        if (!response.ok) throw new Error("Não foi possível carregar o chat.");
        const dados = await response.json();

        // Mapeia os dados adaptando para o layout dos balões (meu vs outro)
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
      console.error(error);
      Alert.alert("Erro", "Erro ao sincronizar mensagens.");
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
    if (!novaMensagem.trim() || !topico?.id || !usuarioLogadoId) return;

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

      if (!response.ok) throw new Error();

      setNovaMensagem("");
      Keyboard.dismiss();
      carregarDados(); // Recarrega para trazer a nova mensagem na lista
    } catch (error) {
      Alert.alert("Erro", "Não foi possível enviar sua mensagem.");
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
    <View style={styles.container}>
      <Header nomeTela={"Conversa"} temGoBack={true} telaDestino={"Titulo"} />

      <View style={styles.pathContainer}>
        <Text style={styles.pathText} numberOfLines={1}>{forumNome}</Text>
        <Ionicons name="chevron-forward" size={14} color="#777" />
        <Text style={styles.pathText} numberOfLines={1}>{topico?.titulo || "Tópico"}</Text>
        <Ionicons name="chevron-forward" size={14} color="#777" />
        <Text style={styles.pathActive}>Conversa</Text>
      </View>

      {carregando ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color={COLORS.primary} />
        </View>
      ) : (
        <ScrollView 
          ref={scrollViewRef}
          showsVerticalScrollIndicator={false} 
          contentContainerStyle={{ paddingBottom: 100, paddingHorizontal: 10 }}
          onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
        >
          {mensagens.map((item) => (
            <View key={item.id.toString()} style={[styles.messageCard, item.meu ? styles.myMessageCard : styles.otherMessageCard]}>
              <View style={styles.topRow}>
                {!item.meu && (
                  <View style={styles.avatar}>
                    <Ionicons name="person" size={16} color="#fff" />
                  </View>
                )}

                <View style={styles.userInfo}>
                  {!item.meu && (
                    <View style={styles.nameRow}>
                      <Text style={styles.name}>{item.nome}</Text>
                    </View>
                  )}
                  <Text style={styles.message}>{item.texto}</Text>
                </View>
              </View>

              <View style={styles.footer}>
                <Text style={styles.time}>{item.hora}</Text>
                {item.meu && (
                  <TouchableOpacity onPress={() => abrirMenu(item)} style={styles.moreButton}>
                    <Feather name="more-vertical" size={14} color="#777" />
                  </TouchableOpacity>
                )}
              </View>
            </View>
          ))}
        </ScrollView>
      )}

      {/* INPUT BARRA INFERIOR */}
      <View style={styles.inputContainer}>
        <TouchableOpacity style={styles.clipButton}><Feather name="paperclip" size={18} color="#666" /></TouchableOpacity>
        <TextInput 
          placeholder="Escreva sua mensagem..." 
          placeholderTextColor="#999" 
          style={styles.input} 
          value={novaMensagem}
          onChangeText={setNovaMensagem}
        />
        <TouchableOpacity style={styles.sendButton} onPress={enviarMensagem}><Ionicons name="send" size={18} color="#fff" /></TouchableOpacity>
      </View>

      {/* MODAL MENU OPÇÕES */}
      <Modal visible={menuVisible} transparent animationType="fade">
        <TouchableOpacity style={styles.overlay} activeOpacity={1} onPress={() => setMenuVisible(false)}>
          <TouchableWithoutFeedback>
            <View style={styles.menuContainer}>
              <TouchableOpacity style={styles.menuItem} onPress={abrirEditar}>
                <Feather name="edit-2" size={18} color="#2563EB" />
                <Text style={styles.menuText}>Editar</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.menuItem} onPress={excluirMensagem}>
                <MaterialIcons name="delete-outline" size={20} color="#EF4444" />
                <Text style={[styles.menuText, { color: "#EF4444" }]}>Excluir</Text>
              </TouchableOpacity>
            </View>
          </TouchableWithoutFeedback>
        </TouchableOpacity>
      </Modal>

      {/* MODAL EDITAR */}
      <Modal visible={editarVisible} transparent animationType="fade" onRequestClose={() => setEditarVisible(false)}>
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setEditarVisible(false)}>
          <TouchableWithoutFeedback>
            <View style={styles.modalContent}>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>Editar Mensagem</Text>
                <TouchableOpacity onPress={() => setEditarVisible(false)} style={{ position: 'absolute', right: 20 }}>
                  <Feather name="x" size={20} color="white" />
                </TouchableOpacity>
              </View>

              <View style={styles.modalBody}>
                <View style={styles.inputContainerModal}>
                  <Text style={styles.inputLabel}>Sua Mensagem</Text>
                  <TextInput value={textoEditando} onChangeText={setTextoEditando} multiline style={[styles.inputField, { height: 90, textAlignVertical: 'top' }]} />
                </View>
                <TouchableOpacity style={styles.saveBtn} onPress={salvarEdicao}>
                  <Text style={styles.saveBtnText}>Salvar</Text>
                </TouchableOpacity>
              </View>
            </View>
          </TouchableWithoutFeedback>
        </TouchableOpacity>
      </Modal>
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
  myMessageCard: { backgroundColor: "#EEF2FF", alignSelf: "flex-end" }, 
  otherMessageCard: { backgroundColor: "#fff", alignSelf: "flex-start" }, 
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