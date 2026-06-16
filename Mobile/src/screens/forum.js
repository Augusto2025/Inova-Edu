import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Modal, ScrollView, TouchableWithoutFeedback, ActivityIndicator, Alert } from "react-native";
import { Ionicons, Feather, MaterialIcons } from "@expo/vector-icons";
import Header from "../components/Header";
import BarraPesquisa from "../components/BarraPesquisa";
import { COLORS } from "../components/Cores";

// Ajusta a URL base removendo o /login se existir
const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');
// Cria a URL específica para o endpoint do fórum, garantindo a barra correta
const URL_FORUM = URL_BASE.endsWith('/') ? `${URL_BASE}forum` : `${URL_BASE}/forum`;
  
export default function ForumScreen({ navigation }) {
  const [topicos, setTopicos] = useState([]);
  const [carregando, setCarregando] = useState(true);

  // Modal com o 'id' do banco
  const [modal, setModal] = useState({ visible: false, modo: "Criar", titulo: "", id: null });

  // ==========================================
  // 1. BUSCAR OS TÓPICOS DO BACKEND (GET)
  // ==========================================
  const carregarTopicos = async () => {
    try {
      setCarregando(true);
      
      // Agora aponta para URL_FORUM (ex: http://.../forum)
      const response = await fetch(URL_FORUM); 
      
      if (!response.ok) {
        const textoErro = await response.text();
        throw new Error(`Status ${response.status}: ${textoErro || "Erro no servidor"}`);
      }
      
      const dados = await response.json();
      setTopicos(dados);
    } catch (error) {
      console.error("Erro ao carregar fórum:", error);
      Alert.alert("Erro de Conexão", `Não foi possível carregar o fórum.\n\nDetalhe: ${error.message}`);
    } finally {
      setCarregando(false);
    }
  };

  useEffect(() => {
    carregarTopicos();
  }, []);

  // ==========================================
  // 2. SALVAR / EDITAR NO BACKEND (POST / PUT)
  // ==========================================
  const salvarTopico = async () => {
    if (!modal.titulo.trim()) return;

    try {
      if (modal.modo === "Criar") {
        // Envia requisição POST para URL_FORUM
        const response = await fetch(URL_FORUM, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            titulo: modal.titulo,
            usuarioId: 1 // ID temporário do autor do fórum
          })
        });

        if (!response.ok) throw new Error("Erro ao criar tópico no servidor.");
      } else {
        // Envia requisição PUT para URL_FORUM/id
        const response = await fetch(`${URL_FORUM}/${modal.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            titulo: modal.titulo
          })
        });

        if (!response.ok) throw new Error("Erro ao editar tópico no servidor.");
      }

      carregarTopicos();
      fecharModal();

    } catch (error) {
      console.error("Erro ao salvar:", error);
      Alert.alert("Erro", `Houve um problema ao salvar o tópico:\n${error.message}`);
    }
  };

  // ==========================================
  // 3. ELIMINAR DO BACKEND (DELETE)
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
              // Envia requisição DELETE para URL_FORUM/id
              const response = await fetch(`${URL_FORUM}/${id}`, { method: "DELETE" });
              if (!response.ok) throw new Error("Erro ao eliminar do servidor.");
              
              setTopicos(topicos.filter(item => item.id !== id));
            } catch (error) {
              console.error("Erro ao eliminar:", error);
              Alert.alert("Erro", `Não foi possível eliminar o tópico:\n${error.message}`);
            }
          }
        }
      ]
    );
  };

  const fecharModal = () => setModal({ visible: false, modo: "Criar", titulo: "", id: null });

  return (
    <View style={styles.container}>
      <Header nomeTela={"Forum"} />
      <BarraPesquisa />

      {carregando ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color={COLORS.primary} />
          <Text style={{ marginTop: 10, color: '#777' }}>Carregando fórum...</Text>
        </View>
      ) : (
        <ScrollView showsVerticalScrollIndicator={false}>
          {topicos.map((item) => (
            <TouchableOpacity key={item.id} style={styles.card} onPress={() => navigation.navigate("Titulo", { topico: item })}>
              <View style={[styles.iconBox, { backgroundColor: item.cor }]}><Ionicons name="chatbubble-ellipses" size={22} color="#fff" /></View>
              <View style={styles.content}>
                <View style={styles.topRow}>
                  <Text style={styles.title} numberOfLines={1}>{item.titulo}</Text>
                  <Text style={styles.time}>{item.tempo}</Text>
                </View>
                <Text style={styles.description} numberOfLines={2}>{item.descricao}</Text>
                
                <View style={styles.footer}>
                  <View style={styles.footerLeft}>
                    <View style={styles.info}>
                      <Ionicons name="person-outline" size={13} color="#777" />
                      <Text style={[styles.infoText, { fontWeight: '600' }]} numberOfLines={1}>
                        {item.autor}
                      </Text>
                    </View>
                    <View style={styles.info}>
                      <Ionicons name="chatbubble-outline" size={13} color="#777" />
                      <Text style={styles.infoText}>{item.mensagens}</Text>
                    </View>
                    <View style={styles.info}>
                      <Feather name="tag" size={13} color="#777" />
                      <Text style={styles.infoText}>{item.categoria}</Text>
                    </View>
                  </View>

                  <View style={styles.actions}>
                    <TouchableOpacity style={styles.editButton} onPress={() => setModal({ visible: true, modo: "Editar", titulo: item.titulo, id: item.id })}><Feather name="edit-2" size={16} color="#5B5EF7" /></TouchableOpacity>
                    <TouchableOpacity style={styles.deleteButton} onPress={() => eliminarTopico(item.id)}><MaterialIcons name="delete-outline" size={18} color="#FF6B6B" /></TouchableOpacity>
                  </View>
                </View>
              </View>
            </TouchableOpacity>
          ))}
        </ScrollView>
      )}

      <TouchableOpacity style={styles.fab} onPress={() => setModal({ visible: true, modo: "Criar", titulo: "", id: null })}><Ionicons name="add" size={28} color="#fff" /></TouchableOpacity>

      {/* MODAL DE CRIAÇÃO / EDIÇÃO */}
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

                {/* Nota: Removemos o input de descrição aqui pois o seu modelo de Banco de Dados não possui este campo */}

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
  card: { backgroundColor: "#fff", marginHorizontal: 12, marginBottom: 12, borderRadius: 16, padding: 14, flexDirection: "row", elevation: 2 },
  iconBox: { width: 42, height: 42, borderRadius: 21, justifyContent: "center", alignItems: "center", marginRight: 12 },
  content: { flex: 1 },
  topRow: { flexDirection: "row", justifyContent: "space-between" },
  title: { flex: 1, fontSize: 15, fontWeight: "700", color: "#222" },
  time: { fontSize: 11, color: "#888" },
  description: { fontSize: 13, color: "#555", marginTop: 4, lineHeight: 18 },
  footer: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginTop: 10 },
  footerLeft: { flexDirection: "row", flex: 1, marginRight: 8, alignItems: 'center' }, 
  info: { flexDirection: "row", alignItems: "center", marginRight: 10, maxWidth: 90 }, 
  infoText: { marginLeft: 4, color: "#777", fontSize: 11 },
  actions: { flexDirection: "row" },
  editButton: { marginRight: 10, padding: 4 },
  deleteButton: { padding: 4 },
  fab: { position: "absolute", bottom: 20, right: 20, width: 56, height: 56, borderRadius: 28, backgroundColor: "#ff8c00", justifyContent: "center", alignItems: "center", elevation: 4 },
  
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