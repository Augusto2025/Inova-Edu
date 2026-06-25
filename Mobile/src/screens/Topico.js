import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, FlatList, TouchableOpacity, TextInput, Modal, Keyboard, TouchableWithoutFeedback, ActivityIndicator, Alert } from "react-native";
import { Ionicons, Feather, MaterialIcons } from "@expo/vector-icons";
import Header from "../components/Header";
import BarraPesquisa from "../components/BarraPesquisa";
import AsyncStorage from '@react-native-async-storage/async-storage';

const COLORS = { primary: "#0e68d6" };

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');
const URL_TOPICO = URL_BASE.endsWith('/') ? `${URL_BASE}topico` : `${URL_BASE}/topico`;

export default function TopicosScreen({ navigation, route }) {
  // Pega o objeto do Fórum que foi clicado na tela anterior
  const forumSelecionado = route.params?.topico; 

  const [topicos, setTopicos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [usuarioLogadoId, setUsuarioLogadoId] = useState(null);
  const [modal, setModal] = useState({ visible: false, modo: "Criar", titulo: "", descricao: "", id: null });

  // ==========================================
  // CARREGAR DADOS INICIAIS
  // ==========================================
  const carregarTopicos = async () => {
    if (!forumSelecionado?.id) return;
    try {
      setCarregando(true);
      const response = await fetch(`${URL_TOPICO}/forum/${forumSelecionado.id}`);
      if (!response.ok) throw new Error("Não foi possível buscar os tópicos.");
      const dados = await response.json();
      setTopicos(dados);
    } catch (error) {
      console.error(error);
      Alert.alert("Erro", "Erro ao carregar tópicos do servidor.");
    } finally {
      setCarregando(false);
    }
  };

  const obterUsuarioLogado = async () => {
    try {
      const idSalvo = await AsyncStorage.getItem('idUsuario');
      if (idSalvo !== null) {
        setUsuarioLogadoId(parseInt(idSalvo));
      }
    } catch (error) {
      console.error("Erro ao ler ID do usuário:", error);
    }
  };

  useEffect(() => {
    obterUsuarioLogado();
    carregarTopicos();
  }, [forumSelecionado]);

  // ==========================================
  // SALVAR / EDITAR NO BACKEND
  // ==========================================
  const salvarTopico = async () => {
    if (!modal.titulo.trim() || !modal.descricao.trim()) return;

    try {
      if (modal.modo === "Criar") {
        const response = await fetch(URL_TOPICO, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            titulo: modal.titulo,
            descricao: modal.descricao,
            forumId: forumSelecionado.id,
            usuarioId: usuarioLogadoId
          })
        });

        if (!response.ok) throw new Error("Erro ao criar tópico.");
      } else {
        const response = await fetch(`${URL_TOPICO}/${modal.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            titulo: modal.titulo,
            descricao: modal.descricao,
            usuarioId: usuarioLogadoId
          })
        });

        if (!response.ok) {
          if (response.status === 403) throw new Error("Você não tem permissão para editar este tópico.");
          throw new Error("Erro ao editar tópico.");
        }
      }

      carregarTopicos();
      fecharModal();
      Keyboard.dismiss();
    } catch (error) {
      Alert.alert("Ação Negada", error.message);
    }
  };

  // ==========================================
  // ELIMINAR DO BACKEND
  // ==========================================
  const eliminarTopico = (id) => {
    Alert.alert(
      "Confirmar Exclusão",
      "Tem certeza que deseja apagar este tópico?",
      [
        { text: "Cancelar", style: "cancel" },
        { 
          text: "Apagar", 
          style: "destructive", 
          onPress: async () => {
            try {
              const response = await fetch(`${URL_TOPICO}/${id}`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ usuarioId: usuarioLogadoId })
              });

              if (!response.ok) {
                if (response.status === 403) throw new Error("Você não tem permissão para apagar este tópico.");
                throw new Error("Erro ao eliminar do servidor.");
              }

              setTopicos((prev) => prev.filter((i) => i.id !== id));
              Alert.alert("Sucesso", "Tópico excluído!");
            } catch (error) {
              Alert.alert("Erro", error.message);
            }
          }
        }
      ]
    );
  };

  const fecharModal = () => setModal({ visible: false, modo: "Criar", titulo: "", descricao: "", id: null });

  const renderItem = ({ item }) => {
    const exibirBotoes = item.usuarioIdCriador === usuarioLogadoId && usuarioLogadoId !== null;

    return (
      <TouchableOpacity style={styles.card} onPress={() => navigation.navigate("Conversa", { forum: "Fórum", topico: item })} activeOpacity={0.9}>
        <View style={styles.iconBox}><Ionicons name="chatbubble-ellipses" size={22} color="#fff" /></View>
        <View style={styles.content}>
          <View style={styles.topRow}>
            <Text style={styles.title} numberOfLines={1}>{item.titulo}</Text>
            <Text style={styles.time}>{item.horario || "Agora"}</Text>
          </View>
          <Text style={styles.date}>Autor: {item.autor || "Anônimo"}</Text>
          <Text style={styles.description} numberOfLines={2}>{item.mensagem}</Text>
          <View style={styles.footer}>
            <View style={styles.footerLeft}>
              <View style={styles.info}><Ionicons name="chatbubble-outline" size={14} color="#777" /><Text style={styles.infoText}>Visualizar conversa</Text></View>
            </View>
            
            {exibirBotoes && (
              <View style={styles.actions}>
                <TouchableOpacity style={styles.editButton} onPress={() => setModal({ visible: true, modo: "Editar", titulo: item.titulo, descricao: item.mensagem, id: item.id })}><Feather name="edit-2" size={16} color="#5B5EF7" /></TouchableOpacity>
                <TouchableOpacity style={styles.deleteButton} onPress={() => eliminarTopico(item.id)}><MaterialIcons name="delete-outline" size={18} color="#FF6B6B" /></TouchableOpacity>
              </View>
            )}
          </View>
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <View style={styles.container}>
      <Header nomeTela={"Título"} temGoBack={true} telaDestino={"Fórum"} />
      <BarraPesquisa />

      <View style={styles.pathContainer}>
        <Text style={styles.pathLabel}>Fórum</Text>
        <Ionicons name="chevron-forward" size={14} color="#777" style={styles.iconArrow} />
        <Text style={styles.pathActive} numberOfLines={1}>{forumSelecionado?.titulo || "Tópicos"}</Text>
      </View>

      {carregando ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color={COLORS.primary} />
          <Text style={{ marginTop: 10, color: '#777' }}>Carregando tópicos...</Text>
        </View>
      ) : (
        <FlatList data={topicos} keyExtractor={(item) => item.id.toString()} renderItem={renderItem} contentContainerStyle={{ paddingHorizontal: 14, paddingBottom: 120 }} showsVerticalScrollIndicator={false} />
      )}

      <TouchableOpacity activeOpacity={0.8} style={styles.fab} onPress={() => setModal({ visible: true, modo: "Criar", titulo: "", descricao: "", id: null })}><Ionicons name="add" size={32} color="#fff" /></TouchableOpacity>

      {/* MODAL INTEGRADO */}
      <Modal visible={modal.visible} transparent animationType="fade" onRequestClose={fecharModal}>
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={fecharModal}>
          <TouchableWithoutFeedback>
            <View style={styles.modalContent}>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>{modal.modo === "Criar" ? "Criar Tópico" : "Editar Tópico"}</Text>
                <TouchableOpacity onPress={fecharModal} style={{ position: 'absolute', right: 20 }}>
                  <Feather name="x" size={20} color="white" />
                </TouchableOpacity>
              </View>

              <View style={styles.modalBody}>
                <View style={styles.inputContainer}>
                  <Text style={styles.inputLabel}>Título do Tópico</Text>
                  <TextInput placeholder="Digite o título..." value={modal.titulo} onChangeText={(t) => setModal({ ...modal, titulo: t })} style={styles.input} />
                </View>

                <View style={styles.inputContainer}>
                  <Text style={styles.inputLabel}>Descrição</Text>
                  <TextInput placeholder="Digite a descrição..." value={modal.descricao} onChangeText={(d) => setModal({ ...modal, descricao: d })} style={[styles.input, { height: 80, textAlignVertical: 'top' }]} multiline />
                </View>

                <TouchableOpacity style={styles.saveBtn} onPress={salvarTopico}>
                  <Text style={styles.saveBtnText}>{modal.modo === "Criar" ? "Criar" : "Salvar"}</Text>
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
  pathContainer: { flexDirection: "row", alignItems: "center", paddingHorizontal: 16, marginBottom: 14 },
  pathLabel: { color: "#777", fontSize: 13 },
  pathActive: { color: "#2563EB", fontSize: 13, fontWeight: "700", flex: 1 },
  iconArrow: { marginHorizontal: 4 },
  card: { backgroundColor: "#fff", marginBottom: 12, borderRadius: 16, padding: 14, flexDirection: "row", elevation: 2 },
  iconBox: { width: 42, height: 42, borderRadius: 21, justifyContent: "center", alignItems: "center", marginRight: 12, backgroundColor: COLORS.primary },
  content: { flex: 1 },
  topRow: { flexDirection: "row", justifyContent: "space-between" },
  title: { flex: 1, fontSize: 15, fontWeight: "700", color: "#222", marginRight: 10 },
  time: { fontSize: 11, color: "#888" },
  date: { fontSize: 11, color: "#888", marginTop: 2 },
  description: { fontSize: 13, color: "#555", marginTop: 6, lineHeight: 18 },
  footer: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginTop: 10 },
  footerLeft: { flexDirection: "row" },
  info: { flexDirection: "row", alignItems: "center", marginRight: 12 },
  infoText: { marginLeft: 4, color: "#777", fontSize: 11 },
  actions: { flexDirection: "row" },
  editButton: { marginRight: 10, padding: 4 },
  deleteButton: { padding: 4 },
  fab: { position: "absolute", bottom: 25, right: 20, width: 56, height: 56, borderRadius: 28, backgroundColor: "#ff8c00", justifyContent: "center", alignItems: "center", elevation: 4 },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0, 0, 0, 0.67)', justifyContent: 'center', padding: 15 },
  modalContent: { backgroundColor: 'white', borderRadius: 25, overflow: 'hidden' },
  modalHeader: { backgroundColor: COLORS.primary, flexDirection: 'row', padding: 20, alignItems: 'center', justifyContent: 'center' },
  modalTitle: { color: 'white', fontSize: 18, fontWeight: 'bold' },
  modalBody: { padding: 20 },
  inputContainer: { marginBottom: 15 },
  inputLabel: { fontSize: 14, fontWeight: "600", color: "#333", marginBottom: 6, paddingLeft: 2 },
  input: { borderWidth: 1, borderColor: '#ddd', borderRadius: 12, padding: 12 },
  saveBtn: { backgroundColor: COLORS.primary, padding: 15, borderRadius: 12, alignItems: 'center', marginTop: 10 },
  saveBtnText: { color: 'white', fontWeight: 'bold' }
});