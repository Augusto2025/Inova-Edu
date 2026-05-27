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

import { Ionicons, Feather, MaterialIcons } from "@expo/vector-icons";

import Header from "../components/Header";
import BarraPesquisa from "../components/BarraPesquisa";

export default function TopicosScreen({ navigation }) {
  const [topicos, setTopicos] = useState([
    {
      id: "1",
      titulo: "React Native é difícil?",
      autor: "Ana",
      status: "Online",
      mensagem: "Consegui resolver usando useEffect e useState juntos!",
      horario: "12:30",
      mensagens: 12,
    },

    {
      id: "2",
      titulo: "Como usar useState?",
      autor: "Carlos",
      status: "Há 1h",
      mensagem: "Você pode usar assim: const [estado, setEstado]...",
      horario: "Ontem",
      mensagens: 8,
    },

    {
      id: "3",
      titulo: "Dúvida sobre FlatList",
      autor: "Mariana",
      status: "Há 3h",
      mensagem: "Alguém sabe como otimizar a performance...",
      horario: "Ontem",
      mensagens: 6,
    },
  ]);

  const [modalVisible, setModalVisible] = useState(false);

  const [novoTitulo, setNovoTitulo] = useState("");

  const [editandoId, setEditandoId] = useState(null);

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

        autor: "Você",

        status: "Agora",

        mensagem: "Novo tópico criado.",

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
    setTopicos((prev) => prev.filter((item) => item.id !== id));
  };

  // CARD
  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => abrirTopico(item)}
      activeOpacity={0.9}
    >
      {/* LINHA AZUL */}
      <View style={styles.leftBorder} />

      <View style={styles.topContent}>
        {/* ÍCONE */}
        <View style={styles.avatarContainer}>
          <View style={styles.avatar}>
            <Ionicons name="chatbubble-ellipses" size={24} color="#fff" />
          </View>

          <View style={styles.onlineDot} />
        </View>

        {/* CONTEÚDO */}
        <View style={styles.infoContainer}>
          {/* TOPO */}
          <View style={styles.rowBetween}>
            <View>
              <Text style={styles.title} numberOfLines={1} ellipsizeMode="tail">
                {item.titulo}
              </Text>

              {/* AUTOR */}
              <View style={styles.authorRow}>
                <Text style={styles.author}>{item.autor}</Text>

                <Text style={styles.dot}>•</Text>

                <Text style={styles.onlineText}>{item.status}</Text>
              </View>
            </View>

            {/* HORÁRIO + BADGE */}
            <View style={styles.rightInfo}>
              <Text style={styles.time}>{item.horario}</Text>

              <View style={styles.messageBadge}>
                <Text style={styles.messageBadgeText}>{item.mensagens}</Text>
              </View>
            </View>
          </View>

          {/* MENSAGEM */}
          <Text style={styles.message} numberOfLines={1} ellipsizeMode="tail">
            {item.mensagem}
          </Text>

          {/* FOOTER */}
          <View style={styles.footer}>
            <View style={styles.footerItem}>
              <Ionicons name="chatbubble-outline" size={14} color="#6B7280" />

              <Text style={styles.footerText}>{item.mensagens} mensagens</Text>
            </View>

            <View style={styles.footerItem}>
              <Feather name="tag" size={13} color="#6B7280" />

              <Text style={styles.footerText}>React Native</Text>
            </View>
          </View>
        </View>

        {/* SETA */}
        <TouchableOpacity style={styles.arrowButton}>
          <Ionicons name="chevron-forward" size={20} color="#777" />
        </TouchableOpacity>
      </View>

      {/* BOTÕES */}
      <View style={styles.actions}>
        <TouchableOpacity
          style={styles.editButton}
          onPress={() => editarTopico(item)}
        >
          <Feather name="edit-2" size={16} color="#2563EB" />
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.deleteButton}
          onPress={() => excluirTopico(item.id)}
        >
          <MaterialIcons name="delete-outline" size={18} color="#EF4444" />
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Header foto={null} escolherImagem={null} nomeTela={"Título"} />

      {/* BUSCA */}
      <BarraPesquisa />

      {/* IDENTIFICAÇÃO */}
      <View style={styles.pathContainer}>
        <Text style={styles.pathLabel}>Fórum</Text>

        <Ionicons
          name="chevron-forward"
          size={14}
          color="#777"
          style={styles.iconArrow}
        />

        <Text style={styles.pathTitulo} numberOfLines={1} ellipsizeMode="tail">
          Título
        </Text>

        <Ionicons
          name="chevron-forward"
          size={14}
          color="#777"
          style={styles.iconArrow}
        />

        <Text style={styles.pathActive}>Conversa</Text>
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
        <Ionicons name="add" size={32} color="#fff" />
      </TouchableOpacity>

      {/* MODAL */}
      <Modal transparent visible={modalVisible} animationType="fade">
        <View style={styles.overlay}>
          <View style={styles.modalContainer}>
            <Text style={styles.modalTitle}>
              {editandoId ? "Editar Título" : "Criar Título"}
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
                onPress={() => setModalVisible(false)}
              >
                <Text style={styles.cancelText}>Cancelar</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.createButton}
                onPress={criarOuEditarTopico}
              >
                <Text style={styles.createText}>
                  {editandoId ? "Salvar" : "Criar"}
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

  // BUSCA
  searchWrapper: {
    marginTop: 15,
    paddingHorizontal: 14,
    paddingBottom: 10,
  },

  searchContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#FFF",
    borderRadius: 25,
    paddingHorizontal: 14,
    height: 48,
    elevation: 2,
  },

  searchInput: {
    flex: 1,
    marginLeft: 10,
  },

  // CAMINHO
  pathContainer: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 16,
    marginBottom: 14,
  },

  pathText: {
    color: "#777",
    fontSize: 13,
  },

  pathActive: {
    color: "#2563EB",
    fontSize: 13,
    fontWeight: "700",
  },

  // CARD
  card: {
    backgroundColor: "#fff",
    borderRadius: 20,
    marginBottom: 14,
    padding: 15,
    position: "relative",

    shadowColor: "#000",

    shadowOffset: {
      width: 0,
      height: 3,
    },

    shadowOpacity: 0.05,
    shadowRadius: 5,

    elevation: 3,
  },

  leftBorder: {
    position: "absolute",
    left: 0,
    top: 15,
    bottom: 15,
    width: 4,
    backgroundColor: "#4B5EFF",
    borderTopRightRadius: 10,
    borderBottomRightRadius: 10,
  },

  topContent: {
    flexDirection: "row",
    alignItems: "center",
  },

  avatarContainer: {
    position: "relative",
  },

  avatar: {
    width: 58,
    height: 58,
    borderRadius: 29,

    backgroundColor: "#4B5EFF",

    justifyContent: "center",
    alignItems: "center",
  },

  onlineDot: {
    position: "absolute",
    bottom: 2,
    right: 2,
    width: 14,
    height: 14,
    borderRadius: 7,
    backgroundColor: "#22C55E",
    borderWidth: 2,
    borderColor: "#fff",
  },

  infoContainer: {
    flex: 1,
    marginLeft: 12,
  },

  rowBetween: {
    flexDirection: "row",
    justifyContent: "space-between",
  },

  title: {
    fontSize: 17,
    fontWeight: "700",
    color: "#111827",
    maxWidth: 190,
  },

  authorRow: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 3,
  },

  author: {
    fontSize: 13,
    fontWeight: "600",
    color: "#374151",
  },

  dot: {
    marginHorizontal: 6,
    color: "#9CA3AF",
  },

  onlineText: {
    fontSize: 12,
    color: "#22C55E",
    fontWeight: "500",
  },

  rightInfo: {
    alignItems: "center",
  },

  time: {
    fontSize: 12,
    color: "#6B7280",
    marginBottom: 8,
  },

  message: {
    fontSize: 13,
    color: "#6B7280",
    marginTop: 8,
    lineHeight: 18,
    maxWidth: "95%",
  },

  messageBadge: {
    backgroundColor: "#4B5EFF",
    minWidth: 26,
    height: 26,
    borderRadius: 13,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 6,
  },

  messageBadgeText: {
    color: "#fff",
    fontWeight: "700",
    fontSize: 12,
  },

  footer: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 12,
  },

  footerItem: {
    flexDirection: "row",
    alignItems: "center",
    marginRight: 18,
  },

  footerText: {
    marginLeft: 5,
    fontSize: 12,
    color: "#6B7280",
  },

  arrowButton: {
    marginLeft: 8,
  },

  // ACTIONS
  actions: {
    flexDirection: "row",
    justifyContent: "flex-end",
    marginTop: 14,
  },

  editButton: {
    width: 38,
    height: 38,
    borderRadius: 12,
    backgroundColor: "#EEF2FF",

    justifyContent: "center",
    alignItems: "center",

    marginRight: 10,
  },

  deleteButton: {
    width: 38,
    height: 38,
    borderRadius: 12,
    backgroundColor: "#FEF2F2",

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

  buttons: {
    flexDirection: "row",
    justifyContent: "space-between",
  },

  cancelButton: {
    borderWidth: 1,
    borderColor: "#D1D5DB",
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
