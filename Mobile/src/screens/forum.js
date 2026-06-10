import React, { useState } from "react";
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Modal, ScrollView, TouchableWithoutFeedback } from "react-native";
import { Ionicons, Feather, MaterialIcons } from "@expo/vector-icons";
import Header from "../components/Header";
import BarraPesquisa from "../components/BarraPesquisa";

const COLORS = { primary: "#0e68d6" };

export default function ForumScreen({ navigation }) {
  const [topicos, setTopicos] = useState([
    { titulo: "Meu primeiro tópico", descricao: "Estou tendo dificuldade para entender o useEffect no React Native...", categoria: "React Native", mensagens: 12, tempo: "há 2 min", cor: COLORS.primary },
    { titulo: "Meu segundo tópico", descricao: "Alguém pode me ajudar com o useState? Não estou entendendo...", categoria: "JavaScript", mensagens: 8, tempo: "Ontem", cor: COLORS.primary },
  ]);

  // Estado unificado controlando os inputs de Título e Descrição
  const [modal, setModal] = useState({ visible: false, modo: "Criar", titulo: "", descricao: "", index: null });

  const salvarTopico = () => {
    if (!modal.titulo.trim() || !modal.descricao.trim()) return;
    const novos = [...topicos];

    if (modal.modo === "Criar") {
      novos.push({ titulo: modal.titulo, descricao: modal.descricao, categoria: "React Native", mensagens: 0, tempo: "Agora", cor: COLORS.primary });
    } else {
      novos[modal.index].titulo = modal.titulo;
      novos[modal.index].descricao = modal.descricao;
    }

    setTopicos(novos);
    setModal({ visible: false, modo: "Criar", titulo: "", descricao: "", index: null });
  };

  const fecharModal = () => setModal({ ...modal, visible: false });

  return (
    <View style={styles.container}>
      <Header nomeTela={"Forum"} />
      <BarraPesquisa />

      <ScrollView showsVerticalScrollIndicator={false}>
        {topicos.map((item, index) => (
          <TouchableOpacity key={index} style={styles.card} onPress={() => navigation.navigate("Titulo", { topico: item })}>
            <View style={[styles.iconBox, { backgroundColor: item.cor }]}><Ionicons name="chatbubble-ellipses" size={22} color="#fff" /></View>
            <View style={styles.content}>
              <View style={styles.topRow}>
                <Text style={styles.title} numberOfLines={1}>{item.titulo}</Text>
                <Text style={styles.time}>{item.tempo}</Text>
              </View>
              <Text style={styles.description} numberOfLines={2}>{item.descricao}</Text>
              <View style={styles.footer}>
                <View style={styles.footerLeft}>
                  <View style={styles.info}><Ionicons name="chatbubble-outline" size={14} color="#777" /><Text style={styles.infoText}>{item.mensagens}</Text></View>
                  <View style={styles.info}><Feather name="tag" size={14} color="#777" /><Text style={styles.infoText}>{item.categoria}</Text></View>
                </View>
                <View style={styles.actions}>
                  <TouchableOpacity style={styles.editButton} onPress={() => setModal({ visible: true, modo: "Editar", titulo: item.titulo, descricao: item.descricao, index })}><Feather name="edit-2" size={16} color="#5B5EF7" /></TouchableOpacity>
                  <TouchableOpacity style={styles.deleteButton} onPress={() => setTopicos(topicos.filter((_, i) => i !== index))}><MaterialIcons name="delete-outline" size={18} color="#FF6B6B" /></TouchableOpacity>
                </View>
              </View>
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <TouchableOpacity style={styles.fab} onPress={() => setModal({ visible: true, modo: "Criar", titulo: "", descricao: "", index: null })}><Ionicons name="add" size={28} color="#fff" /></TouchableOpacity>

      {/* MODAL COM FECHAMENTO AO CLICAR FORA E DOIS CAMPOS */}
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
  card: { backgroundColor: "#fff", marginHorizontal: 12, marginBottom: 12, borderRadius: 16, padding: 14, flexDirection: "row", elevation: 2 },
  iconBox: { width: 42, height: 42, borderRadius: 21, justifyContent: "center", alignItems: "center", marginRight: 12 },
  content: { flex: 1 },
  topRow: { flexDirection: "row", justifyContent: "space-between" },
  title: { flex: 1, fontSize: 15, fontWeight: "700", color: "#222" },
  time: { fontSize: 11, color: "#888" },
  description: { fontSize: 13, color: "#555", marginTop: 4, lineHeight: 18 },
  footer: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginTop: 10 },
  footerLeft: { flexDirection: "row" },
  info: { flexDirection: "row", alignItems: "center", marginRight: 12 },
  infoText: { marginLeft: 4, color: "#777", fontSize: 11 },
  actions: { flexDirection: "row" },
  editButton: { marginRight: 10, padding: 4 },
  deleteButton: { padding: 4 },
  fab: { position: "absolute", bottom: 20, right: 20, width: 56, height: 56, borderRadius: 28, backgroundColor: "#ff8c00", justifyContent: "center", alignItems: "center", elevation: 4 },
  
  // Estilos do Modal originais mantidos
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