import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  TextInput,
  Modal,
  Image,
  Keyboard,
} from "react-native";

import {
  Ionicons,
  Feather,
  MaterialIcons,
} from "@expo/vector-icons";

import Header from "../components/Header";

export default function TopicosScreen({ navigation }) {
  const [topicos, setTopicos] = useState([
    {
      id: "1",
      titulo: "React Native é difícil?",
      mensagem:
        "useEffect está me confundindo, alguém pode me ajudar?",
      horario: "12:30",
      mensagens: 12,
    

    
      id: "2",
      titulo: "Como usar useState?",
      mensagem:
        "Não estou entendendo como atualizar o estado corretamente.",
      horario: "Ontem",
      mensagens: 8,
    },
  ]);

  const [modalVisible, setModalVisible] = useState(false);
  const [novoTitulo, setNovoTitulo] = useState("");
  const [editandoId, setEditandoId] = useState(null);

  // ABRIR CONVERSA
  const abrirTopico = (topico) => {
    navigation.navigate("Conversa", {
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
            ? { ...item, titulo: novoTitulo }
            : item
        )
      );
    } else {
      const novo = {
        id: Date.now().toString(),
        titulo: novoTitulo,
        autor: "Você",
        status: "Agora",
        mensagem: "Nova conversa criada.",
        horario: "Agora",
        mensagens: 0,
        avatar:
          "https://cdn-icons-png.flaticon.com/512/9131/9131529.png",
        cor: "#F97316",
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
      prev.filter((item) => item.id !== id)
    );
  };

  // CARD
  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => abrirTopico(item)}
      activeOpacity={0.9}
    >
      {/* TOPO */}
      <View style={styles.topContent}>
        {/* AVATAR */}
        <View
          style={[
            styles.avatarContainer,
            { backgroundColor: item.cor },
          ]}
        >
          <Image
            source={{ uri: item.avatar }}
            style={styles.avatar}
          />

          <View style={styles.onlineDot} />
        </View>

        {/* CONTEÚDO */}
        <View style={styles.infoContainer}>
          {/* TITULO */}
          <View style={styles.rowBetween}>
            <Text
              style={styles.title}
              numberOfLines={1}
              ellipsizeMode="tail"
            >
              {item.titulo}
            </Text>

            <Text style={styles.time}>
              {item.horario}
            </Text>
          </View>

          {/* AUTOR */}
          <View style={styles.authorRow}>
            <Text style={styles.author}>
              {item.autor}
            </Text>

            <Text style={styles.dot}>•</Text>

            <Text style={styles.onlineText}>
              {item.status}
            </Text>
          </View>

          {/* MENSAGEM */}
          <Text
            style={styles.message}
            numberOfLines={2}
            ellipsizeMode="tail"
          >
            {item.mensagem}
          </Text>
        </View>

        {/* BADGE */}
        <View style={styles.messageBadge}>
          <Text style={styles.messageBadgeText}>
            {item.mensagens}
          </Text>
        </View>
      </View>

      {/* FOOTER */}
      <View style={styles.footer}>
        <View style={styles.footerItem}>
          <Ionicons
            name="chatbubble-outline"
            size={16}
            color="#6B7280"
          />

          <Text style={styles.footerText}>
            {item.mensagens} mensagens
          </Text>
        </View>

        <View style={styles.separator} />

        <View style={styles.footerItem}>
          <Feather
            name="tag"
            size={15}
            color="#6B7280"
          />

          <Text style={styles.footerText}>
            React Native
          </Text>
        </View>

        {/* BOTÕES */}
        <View style={styles.actions}>
          <TouchableOpacity
            style={styles.editButton}
            onPress={() => editarTopico(item)}
          >
            <Feather
              name="edit-2"
              size={16}
              color="#2563EB"
            />
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.deleteButton}
            onPress={() => excluirTopico(item.id)}
          >
            <MaterialIcons
              name="delete-outline"
              size={18}
              color="#EF4444"
            />
          </TouchableOpacity>
        </View>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Header
        foto={null}
        escolherImagem={null}
        nomeTela={" Título "}
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

      {/* HEADER */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <View style={styles.line} />

          <Text style={styles.headerTitle}>
            Meus títulos
          </Text>

          <View style={styles.badge}>
            <Text style={styles.badgeText}>
              {topicos.length} conversas
            </Text>
          </View>
        </View>
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

      {/* MODAL */}
      <Modal
        transparent
        visible={modalVisible}
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
                onPress={criarOuEditarTopico}
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

  // HEADER

  header: {
    paddingHorizontal: 14,
    marginBottom: 20,
  },

  headerLeft: {
    flexDirection: "row",
    alignItems: "center",
  },

  line: {
    width: 4,
    height: 24,
    borderRadius: 10,
    backgroundColor: "#2563EB",
    marginRight: 12,
  },

  headerTitle: {
    fontSize: 24,
    fontWeight: "700",
    color: "#111827",
  },

  badge: {
    backgroundColor: "#E0E7FF",
    marginLeft: 10,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 999,
  },

  badgeText: {
    color: "#4338CA",
    fontSize: 12,
    fontWeight: "600",
  },

  // CARD

  card: {
    backgroundColor: "#FFF",
    borderRadius: 22,
    padding: 16,
    marginBottom: 18,

    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 4,
    },

    shadowOpacity: 0.08,
    shadowRadius: 10,

    elevation: 4,
  },

  topContent: {
    flexDirection: "row",
  },



 
  onlineDot: {
    width: 14,
    height: 14,
    borderRadius: 999,
    backgroundColor: "#22C55E",
    borderWidth: 2,
    borderColor: "#FFF",
    position: "absolute",
    bottom: 2,
    right: 2,
  },

  infoContainer: {
    flex: 1,
    paddingRight: 10,
  },

  rowBetween: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  title: {
    flex: 1,
    fontSize: 20,
    fontWeight: "700",
    color: "#111827",
    marginRight: 10,
  },

  time: {
    fontSize: 13,
    color: "#6B7280",
  },

  authorRow: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 4,
  },

  author: {
    fontWeight: "600",
    color: "#111827",
  },

  dot: {
    marginHorizontal: 6,
    color: "#9CA3AF",
  },

  onlineText: {
    color: "#22C55E",
    fontSize: 13,
    fontWeight: "500",
  },

  message: {
    marginTop: 6,
    fontSize: 14,
    color: "#6B7280",
    lineHeight: 20,
  },

  messageBadge: {
    backgroundColor: "#2563EB",
    minWidth: 34,
    height: 28,
    borderRadius: 999,
    justifyContent: "center",
    alignItems: "center",
    alignSelf: "flex-start",
  },

  messageBadgeText: {
    color: "#FFF",
    fontWeight: "700",
  },

  // FOOTER

  footer: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 18,
  },

  footerItem: {
    flexDirection: "row",
    alignItems: "center",
  },

  footerText: {
    marginLeft: 6,
    color: "#6B7280",
    fontSize: 13,
  },

  separator: {
    width: 1,
    height: 14,
    backgroundColor: "#E5E7EB",
    marginHorizontal: 16,
  },

  actions: {
    flexDirection: "row",
    marginLeft: "auto",
  },

  editButton: {
    width: 38,
    height: 38,
    borderRadius: 12,
    backgroundColor: "#EEF2FF",
    justifyContent: "center",
    alignItems: "center",
    marginRight: 8,
  },

  deleteButton: {
    width: 38,
    height: 38,
    borderRadius: 12,
    backgroundColor: "#FEE2E2",
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

    shadowColor: "#ff8c00",

    shadowOffset: {
      width: 0,
      height: 6,
    },

    shadowOpacity: 0.3,
    shadowRadius: 8,

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