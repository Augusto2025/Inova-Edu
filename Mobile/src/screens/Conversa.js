import React, { useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView, Modal, TouchableWithoutFeedback } from "react-native";
import { Ionicons, Feather, MaterialIcons } from "@expo/vector-icons";
import Header from "../components/Header";

const COLORS = { primary: "#0e68d6" };

export default function ConversaScreen({ navigation, route }) {
  const forum = route.params?.forum || "React Native modulos e pacotes";
  const titulo = route.params?.topico || "React Native é difícil?";

  const [menuVisible, setMenuVisible] = useState(false);
  const [editarVisible, setEditarVisible] = useState(false);
  const [textoEditando, setTextoEditando] = useState("");
  const [mensagemSelecionada, setMensagemSelecionada] = useState(null);

  const [mensagens, setMensagens] = useState([
    { id: 1, nome: "Ana", hora: "12:30", texto: "Gente, estou começando no React Native...\nAlguém também sentiu isso no início?", meu: false },
    { id: 2, nome: "Carlos", hora: "12:32", texto: "Senti sim! No começo parece muita coisa.", meu: false },
    { id: 3, nome: "Mariana", hora: "12:34", texto: "Tenta focar nos conceitos primeiro.", meu: false },
    { id: 4, nome: "João", hora: "12:36", texto: "Concordo!", meu: true },
  ]);

  const abrirMenu = (item) => {
    setMensagemSelecionada(item);
    setMenuVisible(true);
  };

  const excluirMensagem = () => {
    setMensagens(mensagens.filter((item) => item.id !== mensagemSelecionada.id));
    setMenuVisible(false);
  };

  const abrirEditar = () => {
    setTextoEditando(mensagemSelecionada.texto);
    setMenuVisible(false);
    setEditarVisible(true);
  };

  const salvarEdicao = () => {
    setMensagens(mensagens.map((item) => item.id === mensagemSelecionada.id ? { ...item, texto: textoEditando } : item));
    setEditarVisible(false);
  };

  return (
    <View style={styles.container}>
      <Header nomeTela={"Conversa"} temGoBack={true} telaDestino={"Titulo"} />

      <View style={styles.pathContainer}>
        <Text style={styles.pathText} numberOfLines={1}>{forum}</Text>
        <Ionicons name="chevron-forward" size={14} color="#777" />
        <Text style={styles.pathText} numberOfLines={1}>{titulo}</Text>
        <Ionicons name="chevron-forward" size={14} color="#777" />
        <Text style={styles.pathActive}>Conversa</Text>
      </View>

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: 100, paddingHorizontal: 10 }}>
        {mensagens.map((item) => (
          <View key={item.id} style={[styles.messageCard, item.meu ? styles.myMessageCard : styles.otherMessageCard]}>
            <View style={styles.topRow}>
              
              {/* SÓ MOSTRA AVATAR SE NÃO FOR MEU */}
              {!item.meu && (
                <View style={styles.avatar}>
                  <Ionicons name="person" size={16} color="#fff" />
                </View>
              )}

              <View style={styles.userInfo}>
                {/* SÓ MOSTRA NOME SE NÃO FOR MEU */}
                {!item.meu && (
                  <View style={styles.nameRow}>
                    <Text style={styles.name}>{item.nome}</Text>
                  </View>
                )}
                <Text style={styles.message}>{item.texto}</Text>
              </View>
            </View>

            {/* RODAPÉ DO BALÃO: CONCENTRA O HORÁRIO E A OPÇÃO DE EDIÇÃO SE FOR SUA */}
            <View style={styles.footer}>
              <Text style={styles.time}>{item.hora}</Text>
              
              {/* BOTÃO DE MENUS APENAS NAS MINHAS MENSAGENS */}
              {item.meu && (
                <TouchableOpacity onPress={() => abrirMenu(item)} style={styles.moreButton}>
                  <Feather name="more-vertical" size={14} color="#777" />
                </TouchableOpacity>
              )}
            </View>
          </View>
        ))}
      </ScrollView>

      {/* INPUT BARRA INFERIOR */}
      <View style={styles.inputContainer}>
        <TouchableOpacity style={styles.clipButton}><Feather name="paperclip" size={18} color="#666" /></TouchableOpacity>
        <TextInput placeholder="Escreva sua mensagem..." placeholderTextColor="#999" style={styles.input} />
        <TouchableOpacity style={styles.sendButton}><Ionicons name="send" size={18} color="#fff" /></TouchableOpacity>
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
  pathContainer: { flexDirection: "row", alignItems: "center", paddingHorizontal: 15, marginTop: 12, marginBottom: 10 },
  pathText: { color: "#777", fontSize: 13, marginRight: 4 },
  pathActive: { color: "#2563EB", fontSize: 13, fontWeight: "700", marginLeft: 4 },
  
  // Estrutura de contenção com maxWidth e flexShrink
  messageCard: { marginBottom: 10, borderRadius: 16, padding: 12, maxWidth: "80%", elevation: 1 },
  myMessageCard: { backgroundColor: "#EEF2FF", alignSelf: "flex-end" }, 
  otherMessageCard: { backgroundColor: "#fff", alignSelf: "flex-start" }, 

  topRow: { flexDirection: "row", alignItems: "flex-start" },
  avatar: { width: 32, height: 32, borderRadius: 16, backgroundColor: COLORS.primary, justifyContent: "center", alignItems: "center", marginRight: 10, marginTop: 2 },
  
  // flexShrink impede o texto de empurrar as bordas e quebrar o layout
  userInfo: { justifyContent: "center", flexShrink: 1 }, 
  
  nameRow: { flexDirection: "row", alignItems: "center", marginBottom: 4 },
  name: { fontSize: 13, fontWeight: "700", color: "#222" },
  message: { fontSize: 13, color: "#333", lineHeight: 18 },
  
  // Organização do rodapé interno do balão
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