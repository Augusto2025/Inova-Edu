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
          item.id === editandoId
            ? { ...item, titulo: novoTitulo }
            : item
        )
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
    setTopicos((prev) =>
      prev.filter((item) => item.id !== id)
    );
  };

  // renderização dos cards
  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => abrirTopico(item)}
    >
      <View style={styles.iconLeft}>
        <Ionicons
          name="chatbubble-ellipses"
          size={24}
          color="#1e4f8a"
        />
      </View>

      <View style={styles.center}>
        <Text style={styles.titulo}>
          {item.titulo}
        </Text>

        <Text style={styles.info}>
          {item.autor} • {item.mensagens} mensagens
        </Text>
      </View>

      <View style={styles.actions}>
        <TouchableOpacity
          onPress={() => editarTopico(item)}
        >
          <Ionicons
            name="create-outline"
            size={20}
            color="#187cf6"
          />
        </TouchableOpacity>

        <TouchableOpacity
          onPress={() => excluirTopico(item.id)}
          style={{ marginLeft: 10 }}
        >
          <Ionicons
            name="trash-outline"
            size={20}
            color="red"
          />
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Header
        foto={null}
        escolherImagem={null}
        nomeTela={"Titulo"}
      />

      {/* BUSCA */}
      <View style={styles.searchWrapper}>
        <View style={styles.searchContainer}>
          <Ionicons
            name="search"
            size={20}
            color="#1e4f8a"
          />

          <TextInput
            placeholder="Pesquisar Títulos..."
            placeholderTextColor="#999"
            style={styles.searchInput}
          />
        </View>
      </View>

      {/* IDENTIFICAÇÃO DO TÓPICO */}
      {topicoSelecionado && (
        <View style={styles.identificacao}>
          <View style={styles.linhaLaranja} />

          <View style={styles.identificacaoContent}>
            <View style={styles.identificacaoLeft}>
              <Ionicons
                name="calendar-outline"
                size={22}
                color="#F7941D"
              />

              <Text style={styles.identificacaoTexto}>
                {topicoSelecionado.titulo}
              </Text>
            </View>

            <Ionicons
              name="chevron-up"
              size={20}
              color="#F7941D"
            />
          </View>
        </View>
      )}

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
          setEditandoId(null);
          setNovoTitulo("");
          setModalVisible(true);
        }}
      >
        <Ionicons
          name="add"
          size={28}
          color="#fff"
        />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#eaeef3",
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

  identificacao: {
    backgroundColor: "#EDEDED",
    marginHorizontal: 15,
    marginBottom: 10,
    borderRadius: 12,
    overflow: "hidden",
    elevation: 3,
  },

  linhaLaranja: {
    position: "absolute",
    left: 0,
    top: 0,
    bottom: 0,
    width: 5,
    backgroundColor: "#F7941D",
  },

  identificacaoContent: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 18,
  },

  identificacaoLeft: {
    flexDirection: "row",
    alignItems: "center",
  },

  identificacaoTexto: {
    marginLeft: 10,
    fontSize: 16,
    fontWeight: "bold",
    color: "#2F3A4B",
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
});