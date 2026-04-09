import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  TextInput,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";

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

  const abrirTopico = (topico) => {
    navigation.navigate("Conversa", {
      topico: topico.titulo,
    });
  };

  const criarTopico = () => {
    if (novoTitulo.trim() !== "") {
      const novo = {
        id: Date.now().toString(),
        titulo: novoTitulo,
        autor: "Você",
        mensagens: 0,
      };

      setTopicos((prev) => [novo, ...prev]);
      setNovoTitulo("");
      setModalVisible(false);
    }
  };

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => abrirTopico(item)}
    >
      <View style={styles.iconLeft}>
        <Ionicons name="chatbubble-ellipses" size={24} color="#1e4f8a" />
      </View>

      <View style={styles.center}>
        <Text style={styles.titulo}>{item.titulo}</Text>
        <Text style={styles.info}>
          {item.autor} • {item.mensagens} mensagens
        </Text>
      </View>

      <Ionicons name="chevron-forward" size={20} color="#999" />
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      
      {/* 🔝 HEADER */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <TouchableOpacity onPress={() => navigation.goBack()}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>

          <Ionicons
            name="chatbubbles"
            size={26}
            color="#fff"
            style={{ marginHorizontal: 8 }}
          />

          <View>
            <Text style={styles.headerTitle}>Fórum</Text>
            <Text style={styles.headerSubtitle}>Títulos</Text>
          </View>
        </View>
      </View>

      {/* 💬 LISTA */}
      <FlatList
        data={topicos}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={{ padding: 15 }}
      />

      {/* ➕ BOTÃO FLUTUANTE */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => setModalVisible(true)}
      >
        <Ionicons name="add" size={28} color="#fff" />
      </TouchableOpacity>

      {/* 📝 MODAL SIMPLES */}
      {modalVisible && (
        <View style={styles.modal}>
          <View style={styles.modalBox}>
            <Text style={styles.modalTitle}>Novo Tópico</Text>

            <TextInput
              placeholder="Digite o título..."
              value={novoTitulo}
              onChangeText={setNovoTitulo}
              style={styles.input}
            />

            <View style={styles.botoes}>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Text style={styles.cancelar}>Cancelar</Text>
              </TouchableOpacity>

              <TouchableOpacity onPress={criarTopico}>
                <Text style={styles.salvar}>Salvar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#eaeef3",
  },

  /* HEADER */
  header: {
    paddingTop: 35,
    height: 90,
    backgroundColor: "#1e4f8a",
    justifyContent: "center",
    paddingHorizontal: 10,
    elevation: 4,
  },

  headerLeft: {
    flexDirection: "row",
    alignItems: "center",
  },

  headerTitle: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "bold",
  },

  headerSubtitle: {
    color: "#ddd",
    fontSize: 12,
  },

  /* LISTA */
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

  /* FAB */
  fab: {
    position: "absolute",
    bottom: 25,
    right: 20,
    backgroundColor: "#187cf6",
    width: 60,
    height: 60,
    borderRadius: 50,
    justifyContent: "center",
    alignItems: "center",
    elevation: 5,
  },

  /* MODAL */
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
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 10,
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