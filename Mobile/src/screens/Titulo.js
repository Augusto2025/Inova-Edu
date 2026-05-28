import React, { useState } from "react";

import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  TextInput,
  Modal,
  Keyboard,
} from "react-native";

import {
  Ionicons,
  Feather,
  MaterialIcons,
} from "@expo/vector-icons";

import Header from "../components/Header";
import BarraPesquisa from "../components/BarraPesquisa";

export default function TopicosScreen({
  navigation,
}) {
  const [topicos, setTopicos] = useState([
    {
      id: "1",
      titulo: "React Native é difícil?",
      mensagem:
        "Consegui resolver usando useEffect e useState juntos!",
      horario: "12:30",
      mensagens: 12,
    },

    {
      id: "2",
      titulo: "Como usar useState?",
      mensagem:
        "Você pode usar assim: const [estado, setEstado]...",
      horario: "Ontem",
      mensagens: 8,
    },

    {
      id: "3",
      titulo: "Dúvida sobre FlatList",
      mensagem:
        "Alguém sabe como otimizar a performance...",
      horario: "Ontem",
      mensagens: 6,
    },
  ]);

  const [modalVisible, setModalVisible] =
    useState(false);

  const [novoTitulo, setNovoTitulo] =
    useState("");

  const [editandoId, setEditandoId] =
    useState(null);

  // ABRIR CONVERSA
  const abrirTopico = (topico) => {
    navigation.navigate("Conversa", {
      forum: "Forum",
      topico: topico.titulo,
    });
  };

  // CRIAR OU EDITAR
  const criarOuEditarTopico = () => {
    if (novoTitulo.trim() === "") return;

    if (editandoId) {
      setTopicos((prev) =>
        prev.map((item) =>
          item.id === editandoId
            ? {
                ...item,
                titulo: novoTitulo,
              }
            : item,
        ),
      );
    } else {
      const novo = {
        id: Date.now().toString(),

        titulo: novoTitulo,

        mensagem: "Novo tópico criado...",

        horario: "Agora",

        mensagens: 0,
      };

      setTopicos((prev) => [novo, ...prev]);
    }

    setNovoTitulo("");
    setEditandoId(null);
    setModalVisible(false);

    Keyboard.dismiss();
  };

  // EDITAR
  const editarTopico = (item) => {
    setNovoTitulo(item.titulo);
    setEditandoId(item.id);
    setModalVisible(true);
  };

  // EXCLUIR
  const excluirTopico = (id) => {
    setTopicos((prev) =>
      prev.filter((item) => item.id !== id),
    );
  };

  // CARD
  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => abrirTopico(item)}
      activeOpacity={0.9}
    >
      {/* ÍCONE */}
      <View style={styles.iconBox}>
        <Ionicons
          name="chatbubble-ellipses"
          size={22}
          color="#fff"
        />
      </View>

      {/* CONTEÚDO */}
      <View style={styles.content}>
        {/* TOPO */}
        <View style={styles.topRow}>
          <Text
            style={styles.title}
            numberOfLines={1}
            ellipsizeMode="tail"
          >
            {item.titulo}
          </Text>

          <View style={styles.rightInfo}>
            <Text style={styles.time}>
              {item.horario}
            </Text>
          </View>
        </View>

        {/* DATA */}
        <Text style={styles.date}>
          Publicado em 10/05/2024
        </Text>

        {/* DESCRIÇÃO */}
        <Text
          style={styles.description}
          numberOfLines={2}
          ellipsizeMode="tail"
        >
          {item.mensagem}
        </Text>

        {/* FOOTER */}
        <View style={styles.footer}>
          <View style={styles.footerLeft}>
            <View style={styles.info}>
              <Ionicons
                name="chatbubble-outline"
                size={14}
                color="#777"
              />

              <Text style={styles.infoText}>
                {item.mensagens} mensagens
              </Text>
            </View>

            <View style={styles.info}>
              <Feather
                name="tag"
                size={14}
                color="#777"
              />

              <Text style={styles.infoText}>
                React Native
              </Text>
            </View>
          </View>

          {/* BOTÕES */}
          <View style={styles.actions}>
            <TouchableOpacity
              style={styles.editButton}
              onPress={() => editarTopico(item)}
            >
              <Feather
                name="edit-2"
                size={18}
                color="#5B5EF7"
              />
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.deleteButton}
              onPress={() =>
                excluirTopico(item.id)
              }
            >
              <MaterialIcons
                name="delete-outline"
                size={20}
                color="#FF6B6B"
              />
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Header
        foto={null}
        escolherImagem={null}
        nomeTela={"Título"}
      />

      {/* BUSCA */}
      <BarraPesquisa />

      {/* IDENTIFICAÇÃO */}
      <View style={styles.pathContainer}>
        <Text style={styles.pathLabel}>
          Fórum
        </Text>

        <Ionicons
          name="chevron-forward"
          size={14}
          color="#777"
          style={styles.iconArrow}
        />

        <Text
          style={styles.pathTitulo}
          numberOfLines={1}
          ellipsizeMode="tail"
        >
          Título
        </Text>

        <Ionicons
          name="chevron-forward"
          size={14}
          color="#777"
          style={styles.iconArrow}
        />

        <Text style={styles.pathActive}>
          Conversa
        </Text>
      </View>

      {/* LISTA */}
      <FlatList
        data={topicos}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={{
          paddingHorizontal: 14,
          paddingBottom: 120,
        }}
        showsVerticalScrollIndicator={false}
      />

      {/* FAB */}
      <TouchableOpacity
        activeOpacity={0.8}
        style={styles.fab}
        onPress={() => {
          setEditandoId(null);
          setNovoTitulo("");
          setModalVisible(true);
        }}
      >
        <Ionicons
          name="add"
          size={32}
          color="#fff"
        />
      </TouchableOpacity>

      {/* MODAL EDITAR */}
      <Modal
        visible={modalVisible}
        transparent
        animationType="fade"
      >
        <View style={styles.overlay}>
          <View style={styles.modalContainer}>
            <Text style={styles.modalTitle}>
              {editandoId
                ? "Editar Título"
                : "Criar Título"}
            </Text>

            <View style={styles.titleUnderline} />

            <TextInput
              placeholder="Digite o título..."
              value={novoTitulo}
              onChangeText={setNovoTitulo}
              style={styles.input}
              placeholderTextColor="#999"
            />

            <View style={styles.buttons}>
              <TouchableOpacity
                style={styles.cancelButton}
                onPress={() =>
                  setModalVisible(false)
                }
              >
                <Text style={styles.cancelText}>
                  Cancelar
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.createButton}
                onPress={
                  criarOuEditarTopico
                }
              >
                <Text style={styles.createText}>
                  {editandoId
                    ? "Salvar"
                    : "Criar"}
                </Text>
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
    backgroundColor: "#F4F6FB",
  },

  // CAMINHO
  pathContainer: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 16,
    marginBottom: 14,
  },

  pathLabel: {
    color: "#777",
    fontSize: 13,
  },

  pathTitulo: {
    color: "#777",
    fontSize: 13,
    maxWidth: 80,
  },

  pathActive: {
    color: "#2563EB",
    fontSize: 13,
    fontWeight: "700",
  },

  iconArrow: {
    marginHorizontal: 4,
  },

  // CARD
  card: {
    backgroundColor: "#fff",
    marginBottom: 14,
    borderRadius: 22,
    padding: 16,
    flexDirection: "row",

    shadowColor: "#000",

    shadowOffset: {
      width: 0,
      height: 3,
    },

    shadowOpacity: 0.05,
    shadowRadius: 5,

    elevation: 3,
  },

  iconBox: {
    width: 46,
    height: 46,
    borderRadius: 23,
    justifyContent: "center",
    alignItems: "center",
    marginRight: 14,
    backgroundColor: "#0e68d6",
  },

  content: {
    flex: 1,
  },

  topRow: {
    flexDirection: "row",
    justifyContent: "space-between",
  },

  title: {
    flex: 1,
    fontSize: 16,
    fontWeight: "700",
    color: "#222",
    marginRight: 10,
  },

  rightInfo: {
    alignItems: "flex-end",
  },

  time: {
    fontSize: 12,
    color: "#888",
    marginBottom: 6,
  },

  date: {
    fontSize: 12,
    color: "#888",
    marginTop: 4,
  },

  description: {
    fontSize: 14,
    color: "#555",
    marginTop: 8,
    lineHeight: 20,
  },

  footer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 16,
  },

  footerLeft: {
    flexDirection: "row",
    flexWrap: "wrap",
  },

  info: {
    flexDirection: "row",
    alignItems: "center",
    marginRight: 16,
  },

  infoText: {
    marginLeft: 4,
    color: "#777",
    fontSize: 12,
  },

  actions: {
    flexDirection: "row",
  },

  editButton: {
    width: 38,
    height: 38,
    borderRadius: 12,
    backgroundColor: "#EEF0FF",
    justifyContent: "center",
    alignItems: "center",
    marginRight: 10,
  },

  deleteButton: {
    width: 38,
    height: 38,
    borderRadius: 12,
    backgroundColor: "#FFF0F0",
    justifyContent: "center",
    alignItems: "center",
  },

  // FAB
  fab: {
    position: "absolute",

    bottom: 25,
    right: 20,

    width: 65,
    height: 65,
    borderRadius: 999,

    backgroundColor: "#ff8c00",

    justifyContent: "center",
    alignItems: "center",

    elevation: 8,
  },

  // MODAL
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.4)",
    justifyContent: "center",
    alignItems: "center",
  },

  modalContainer: {
    width: "85%",
    backgroundColor: "#FFF",
    borderRadius: 20,
    padding: 20,
  },

  modalTitle: {
    fontSize: 22,
    fontWeight: "bold",
    textAlign: "center",
    color: "#1E4D8C",
    marginBottom: 10,
  },

  titleUnderline: {
    width: 120,
    height: 3,
    backgroundColor: "#ff8c00",
    alignSelf: "center",
    marginBottom: 20,
    borderRadius: 10,
  },

  input: {
    borderWidth: 1,
    borderColor: "#E5E7EB",
    borderRadius: 12,
    paddingHorizontal: 15,
    height: 52,
    marginBottom: 20,
  },

  // botoes modal editar
  buttons: {
    flexDirection: "row",
    justifyContent: "space-between",
  },

  cancelButton: {
    borderWidth: 1,
    borderColor: "#d3dbd1",
    borderRadius: 12,
    paddingVertical: 12,
    paddingHorizontal: 20,
  },

  createButton: {
    backgroundColor: "#ff9800",
    borderRadius: 12,
    paddingVertical: 12,
    paddingHorizontal: 25,
  },

  cancelText: {
    color: "#777",
    fontWeight: "600",
  },

  createText: {
    color: "#FFF",
    fontWeight: "bold",
  },
});