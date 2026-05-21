import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  TextInput,
  KeyboardAvoidingView,
  Platform,
  TouchableWithoutFeedback,
  Keyboard,
  Modal,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";
import Header from "../components/Header";

export default function TopicosScreen({ navigation }) {
  const [topicos, setTopicos] = useState([
    {
      id: "1",
      titulo: "React Native é difícil?",
      autor: "Ana",
      mensagens: 12,
    },
    {
      id: "2",
      titulo: "Como usar useState?",
      autor: "Carlos",
      mensagens: 8,
    },
  ]);

  const [topicoSelecionado, setTopicoSelecionado] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [novoTitulo, setNovoTitulo] = useState("");
  const [editandoId, setEditandoId] = useState(null);

  // selecionar tópico
  const abrirTopico = (topico) => {
    setTopicoSelecionado(topico);

    navigation.navigate("Conversa", {
      topico: topico.titulo,
    });
  };

  // criar ou editar
  const criarOuEditarTopico = () => {
    if (novoTitulo.trim() === "") return;

    if (editandoId) {
      setTopicos((prev) =>
        prev.map((item) =>
          item.id === editandoId ? { ...item, titulo: novoTitulo } : item,
        ),
      );
    } else {
      const novo = {
        id: Date.now().toString(),
        titulo: novoTitulo,
        autor: "Você",
        mensagens: 0,
      };

      setTopicos((prev) => [novo, ...prev]);
    }

    setNovoTitulo("");
    setEditandoId(null);
    setModalVisible(false);
    Keyboard.dismiss();
  };

  // editar
  const editarTopico = (item) => {
    setNovoTitulo(item.titulo);
    setEditandoId(item.id);
    setModalVisible(true);
  };

  // excluir
  const excluirTopico = (id) => {
    setTopicos((prev) => prev.filter((item) => item.id !== id));
  };

  // renderização dos cards
  const renderItem = ({ item }) => (
    <TouchableOpacity style={styles.card} onPress={() => abrirTopico(item)}>
      <View style={styles.iconLeft}>
        <Ionicons name="chatbubble-ellipses" size={24} color="#1e4f8a" />
      </View>

      <View style={styles.center}>
        <Text style={styles.titulo}>{item.titulo}</Text>

        <Text style={styles.info}>
          {item.autor} • {item.mensagens} mensagens
        </Text>
      </View>

      <View style={styles.actions}>
        <TouchableOpacity onPress={() => editarTopico(item)}>
          <Ionicons name="create-outline" size={20} color="#187cf6" />
        </TouchableOpacity>

        <TouchableOpacity
          onPress={() => excluirTopico(item.id)}
          style={{ marginLeft: 10 }}
        >
          <Ionicons name="trash-outline" size={20} color="red" />
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Header foto={null} escolherImagem={null} nomeTela={" Título "} />

      {/* BUSCA */}
      <View style={styles.searchWrapper}>
        <View style={styles.searchContainer}>
          <Ionicons name="search" size={20} color="#1e4f8a" />

          <TextInput
            placeholder="Pesquisar Títulos..."
            placeholderTextColor="#999"
            style={styles.searchInput}
          />
        </View>
      </View>

      {/* TÍTULO Subtitulo */}
      <TouchableOpacity style={styles.subtitulo}>
        {/* <Ionicons
            name="calendar-outline"
            size={22}
            color="#0D6EFD"
        /> */}
        <Text style={styles.text}>Nome do subtitulo</Text>
      </TouchableOpacity>

      {/* LISTA */}
      <FlatList
        data={topicos}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={{
          padding: 15,
        }}
      />

      {/* BOTÃO FLUTUANTE */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => {
          console.log("clicou");
          setEditandoId(null);
          setNovoTitulo("");
          setModalVisible(true);
        }}
      >
        <Ionicons name="add" size={28} color="#fff" />
      </TouchableOpacity>

      <Modal transparent visible={modalVisible} animationType="fade">
        <View style={styles.overlay}>
          <View style={styles.modalContainer}>
            <Text style={styles.title}>Criar  Título</Text>

            <TextInput
              placeholder="Digite o título..."
              value={novoTitulo}
              onChangeText={setNovoTitulo}
              style={styles.input}
            />

            <View style={styles.buttons}>
              <TouchableOpacity
                style={styles.cancelButton}
                onPress={() => setModalVisible(false)}
              >
                <Text style={styles.cancelText}>Cancelar</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.createButton}
                onPress={() => {
                  console.log("Criar tópico:", novoTitulo);

                  setModalVisible(false);
                }}
              >
                <Text style={styles.createText}>Criar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#eaeef3",
  },

  // Modal 
   overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.4)",
    justifyContent: "center",
    alignItems: "center",
  },

  modalContainer: {
    width: "85%",
    backgroundColor: "#fff",
    borderRadius: 20,
    padding: 20,
  },

  title: {
    fontSize: 22,
    fontWeight: "bold",
    textAlign: "center",
    color: "#1E4D8C",
    marginBottom: 20,
  },

  input: {
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 10,
    paddingHorizontal: 15,
    height: 50,
    marginBottom: 20,
  },

  buttons: {
    flexDirection: "row",
    justifyContent: "space-between",
  },

  cancelButton: {
    borderWidth: 1,
    borderColor: "#999",
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 20,
  },

  createButton: {
    backgroundColor: "#ff9800",
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 25,
  },

  cancelText: {
    color: "#777",
    fontWeight: "600",
  },

  createText: {
    color: "#fff",
    fontWeight: "bold",
  },






  // subtitulo

  subtitulo: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#F2F2F2",
    paddingVertical: 15,
    paddingHorizontal: 15,
    borderRadius: 12,

    borderLeftWidth: 5,
    borderLeftColor: "#0D6EFD",

    marginHorizontal: 15,
    marginTop: 10,
  },

  text: {
    marginLeft: 10,
    fontSize: 18,
    fontWeight: "600",
    color: "#0D6EFD",
  },

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
    elevation: 2,
  },

  searchInput: {
    flex: 1,
    marginLeft: 8,
  },

  card: {
    backgroundColor: "#fff",
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
    flexDirection: "row",
    alignItems: "center",
    elevation: 2,
  },

  iconLeft: {
    marginRight: 10,
  },

  center: {
    flex: 1,
  },

  titulo: {
    fontSize: 15,
    fontWeight: "bold",
  },

  info: {
    fontSize: 12,
    color: "#777",
  },

  actions: {
    flexDirection: "row",
    alignItems: "center",
  },

  fab: {
    position: "absolute",
    bottom: 130,
    right: 13,
    top: 720,
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: "#ff8c00",
    justifyContent: "center",
    alignItems: "center",
  },
});
