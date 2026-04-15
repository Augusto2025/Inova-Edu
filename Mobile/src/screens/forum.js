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
    <View style={styles.container}>
      <Header navigation={navigation} nomeTela={"Topicos"} />
  

      {/* BUSCA */}
      <View style={styles.searchWrapper}>
        <View style={styles.searchContainer}>
          <Ionicons name="search" size={20} color="#1e4f8a" />
          <TextInput
            placeholder="Pesquisar Tópicos..."
            style={styles.input}
          />
        </View>
      </View>

      {/* LISTA */}
      <ScrollView style={{ marginBottom: 100 }}>
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

      {/* BOTÃO */}
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

   
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f2f2f2" },

  searchWrapper: {
    marginTop: 15,
    paddingHorizontal: 10,
    paddingBottom: 10,
  },

  searchContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#fff",
    borderRadius: 25,
    paddingHorizontal: 12,
    height: 40,
  },

  input: {
    flex: 1,
    marginLeft: 8,
  },


  card: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#fff",
    padding: 12,
    marginHorizontal: 20,
    marginTop: 10,
    borderRadius: 10,
    elevation: 2,
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
    bottom: 130,
    right: 13,
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: "#ff8c00",
    justifyContent: "center",
    alignItems: "center",
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
    color: "#1e4f8a",
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