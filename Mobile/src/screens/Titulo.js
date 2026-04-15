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

  const [modalVisible, setModalVisible] = useState(false);
  const [novoTitulo, setNovoTitulo] = useState("");
  const [editandoId, setEditandoId] = useState(null);

  const abrirTopico = (topico) => {
    navigation.navigate("Forum", {
      topico: topico.titulo,
    });
  };

  const criarOuEditarTopico = () => {
    if (novoTitulo.trim() === "") return;

    if (editandoId) {
      // EDITAR
      setTopicos((prev) =>
        prev.map((item) =>
          item.id === editandoId ? { ...item, titulo: novoTitulo } : item,
        ),
      );
    } else {
      // CRIAR
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

  const editarTopico = (item) => {
    setNovoTitulo(item.titulo);
    setEditandoId(item.id);
    setModalVisible(true);
  };

  const excluirTopico = (id) => {
    setTopicos((prev) => prev.filter((item) => item.id !== id));
  };

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
      <Header navigation={navigation} nomeTela={"Fórum Títulos"} />


      {/* Busca */}
      <View style={styles.searchWrapper}>
        <View style={styles.searchContainer}>
          <Ionicons name="search" size={20} color="#1e4f8a" />

          <TextInput
            placeholder="Pesquisar Titulos..."
            placeholderTextColor="#999"
            style={styles.searchInput}
          />
        </View>
      </View>

      {/* LISTA */}
      <FlatList
        data={topicos}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={{ padding: 15 }}
      />

      {/* BOTÃO FLUTUANTE */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => {
          setEditandoId(null);
          setNovoTitulo("");
          setModalVisible(true);
        }}
      >
        <Ionicons name="add" size={28} color="#fff" />
      </TouchableOpacity>

      {/* MODAL */}
      {modalVisible && (
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
          <KeyboardAvoidingView
            style={styles.modal}
            behavior={Platform.OS === "ios" ? "padding" : "height"}
          >
            <View style={styles.modalBox}>
              <Text style={styles.modalTitle}>
                {editandoId ? "Editar Tópico" : "Novo Tópico"}
              </Text>

              <TextInput
                placeholder="Digite o título..."
                value={novoTitulo}
                onChangeText={setNovoTitulo}
                style={styles.input}
                autoFocus
                returnKeyType="done"
              />

              <View style={styles.botoes}>
                <TouchableOpacity onPress={() => setModalVisible(false)}>
                  <Text style={styles.cancelar}>Cancelar</Text>
                </TouchableOpacity>

                <TouchableOpacity onPress={criarOuEditarTopico}>
                  <Text style={styles.salvar}>
                    {editandoId ? "Atualizar" : "Salvar"}
                  </Text>
                </TouchableOpacity>
              </View>
            </View>
          </KeyboardAvoidingView>
        </TouchableWithoutFeedback>
      )}
      
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#eaeef3",
  },


  // busca
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
    fontSize: 14,
    color: "#000",
  },

  // card
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
    bottom: 70,
    right: 20,
    backgroundColor: "#187cf6",
    width: 60,
    height: 60,
    borderRadius: 50,
    justifyContent: "center",
    alignItems: "center",
    elevation: 5,
  },

  modal: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "#00000088",
    justifyContent: "center",
    alignItems: "center",
  },

  modalBox: {
    width: "80%",
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 20,
  },

  modalTitle: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#1e4f8a",
    textAlign: "center",
    borderBottomWidth: 2,
    borderBottomColor: "#ff8c00",
    paddingBottom: 6,
    marginBottom: 15,
  },

  input: {
    backgroundColor: "#eee",
    borderRadius: 10,
    padding: 10,
    marginBottom: 15,
  },

  botoes: {
    flexDirection: "row",
    justifyContent: "flex-end",
  },

  cancelar: {
    marginRight: 15,
    color: "red",
  },

  salvar: {
    color: "#187cf6",
    fontWeight: "bold",
  },
});
