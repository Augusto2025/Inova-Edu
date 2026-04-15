import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Modal,
  ScrollView,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import Header from "../components/Header";

export default function ForumScreen({ navigation }) {
  const [modalVisible, setModalVisible] = useState(false);
  const [modalEditarVisible, setModalEditarVisible] = useState(false);

  const [topicos, setTopicos] = useState([
    "Meu primeiro tópico",
    "Meu segundo tópico",
    "Meu terceiro tópico",
  ]);

  const [novoTopico, setNovoTopico] = useState("");
  const [topicoEditando, setTopicoEditando] = useState("");
  const [indexEditando, setIndexEditando] = useState(null);

  const abrirTopico = (topico) => {
    navigation.navigate("Conversa", { topico });
  };

  const criarTopico = () => {
    if (novoTopico.trim() === "") return;

    setTopicos([...topicos, novoTopico]);
    setNovoTopico("");
    setModalVisible(false);
  };

  const abrirEditar = (item, index) => {
    setTopicoEditando(item);
    setIndexEditando(index);
    setModalEditarVisible(true);
  };

  const salvarEdicao = () => {
    if (topicoEditando.trim() === "") return;

    const novos = [...topicos];
    novos[indexEditando] = topicoEditando;

    setTopicos(novos);
    setModalEditarVisible(false);
    setTopicoEditando("");
  };

  const excluirTopico = (index) => {
    const novos = topicos.filter((_, i) => i !== index);
    setTopicos(novos);
  };

  return (
    <SafeAreaView style={styles.container}>
      
        <Header
        navigation={navigation}
        nomeTela="Fórum"
      />

      {/* BUSCA */}
      <View style={styles.searchWrapper}>
        <View style={styles.searchContainer}>
          <Ionicons name="search" size={20} color="#1e4f8a" />
          <TextInput
            placeholder="Pesquisar tópicos..."
            style={styles.input}
          />
        </View>
      </View>

      {/* TÍTULO */}
      <View style={styles.containerTopicos}>
        <Text style={styles.textoTopicos}>Tópicos</Text>
        <View style={styles.linha} />
      </View>

      {/* LISTA */}
      <ScrollView contentContainerStyle={{ paddingBottom: 120 }}>
        {topicos.map((item, index) => (
          <TouchableOpacity
            key={index}
            style={styles.card}
            onPress={() => abrirTopico(item)}
          >
            <Text style={styles.nomeTopico}>{item}</Text>

            <View style={styles.acoes}>
              <TouchableOpacity onPress={() => abrirEditar(item, index)}>
                <Ionicons name="create-outline" size={20} color="#1e8a3e" />
              </TouchableOpacity>

              <TouchableOpacity
                style={{ marginLeft: 15 }}
                onPress={() => excluirTopico(index)}
              >
                <Ionicons name="trash-outline" size={20} color="#ff0000" />
              </TouchableOpacity>
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* BOTÃO FLUTUANTE */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => setModalVisible(true)}
      >
        <Ionicons name="add" size={28} color="#fff" />
      </TouchableOpacity>

      {/* MODAL CRIAR */}
      <Modal visible={modalVisible} transparent animationType="fade">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContainer}>
            <Text style={styles.modalTitle}>Criar Tópico</Text>

            <TextInput
              placeholder="Digite o título..."
              value={novoTopico}
              onChangeText={setNovoTopico}
              style={styles.modalInput}
            />

            <View style={styles.modalButtons}>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Text style={styles.bottomCancelar}>Cancelar</Text>
              </TouchableOpacity>

              <TouchableOpacity onPress={criarTopico}>
                <Text style={styles.bottomCriar}>Criar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

      {/* MODAL EDITAR */}
      <Modal visible={modalEditarVisible} transparent animationType="fade">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContainer}>
            <Text style={styles.modalTitle}>Editar Tópico</Text>

            <TextInput
              value={topicoEditando}
              onChangeText={setTopicoEditando}
              style={styles.modalInput}
            />

            <View style={styles.modalButtons}>
              <TouchableOpacity onPress={() => setModalEditarVisible(false)}>
                <Text style={styles.bottomCancelar}>Cancelar</Text>
              </TouchableOpacity>

              <TouchableOpacity onPress={salvarEdicao}>
                <Text style={styles.bottomCriar}>Salvar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f5f7fb" },

  searchWrapper: {
    marginTop: 10,
    paddingHorizontal: 15,
  },

  searchContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#fff",
    borderRadius: 20,
    paddingHorizontal: 12,
    height: 45,
    elevation: 2,
  },

  input: {
    flex: 1,
    marginLeft: 8,
  },

  containerTopicos: {
    alignItems: "center",
    marginTop: 15,
  },

  textoTopicos: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#1459b3",
  },

  linha: {
    width: 120,
    height: 3,
    backgroundColor: "#ff8c00",
    marginTop: 5,
  },

  card: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#fff",
    padding: 15,
    marginHorizontal: 15,
    marginTop: 10,
    borderRadius: 15,
    elevation: 3,
  },

  nomeTopico: {
    fontSize: 16,
    fontWeight: "bold",
  },

  acoes: {
    flexDirection: "row",
  },

  fab: {
    position: "absolute",
    bottom: 90, // 🔥 ajustado pro menu
    right: 20,
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: "#ff8c00",
    justifyContent: "center",
    alignItems: "center",
    elevation: 6,
  },

  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.5)",
    justifyContent: "center",
    alignItems: "center",
  },

  modalContainer: {
    width: "85%",
    backgroundColor: "#fff",
    padding: 20,
    borderRadius: 15,
  },

  modalTitle: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#1459b3",
    textAlign: "center",
    marginBottom: 15,
  },

  modalInput: {
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 10,
    padding: 10,
    marginBottom: 20,
  },

  modalButtons: {
    flexDirection: "row",
    justifyContent: "space-between",
  },

  bottomCriar: {
    backgroundColor: "#ff8c00",
    color: "#fff",
    padding: 10,
    borderRadius: 8,
  },

  bottomCancelar: {
    color: "#999",
    borderWidth: 1,
    padding: 10,
    borderRadius: 8,
  },
});