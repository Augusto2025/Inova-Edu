import React, { useState } from "react";

import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  ScrollView,
  Modal,
} from "react-native";

import {
  Ionicons,
  Feather,
  MaterialIcons,
} from "@expo/vector-icons";

import Header from "../components/Header";

export default function ConversaScreen({
  navigation,
  route,
}) {
  // IDENTIFICAÇÃO
  const forum = route.params?.forum || "React Native modulos e pacotes";

  const titulo =
    route.params?.topico ||
    "React Native é difícil?";

  // MENU
  const [menuVisible, setMenuVisible] =
    useState(false);

  // MODAL EDITAR
  const [editarVisible, setEditarVisible] =
    useState(false);

  // TEXTO EDITANDO
  const [textoEditando, setTextoEditando] =
    useState("");

  // MENSAGEM SELECIONADA
  const [mensagemSelecionada, setMensagemSelecionada] =
    useState(null);

  // MENSAGENS
  const [mensagens, setMensagens] = useState([
    {
      id: 1,
      nome: "Ana",
      hora: "12:30",
      texto:
        "Gente, estou começando no React Native e estou achando um pouco desafiador...\n\nAlguém também sentiu isso no início?",
      
    },

    {
      id: 2,
      nome: "Carlos",
      hora: "12:32",
      texto:
        "Senti sim! No começo parece muita coisa, mas conforme você prática, as coisas começam a fazer sentido.",
      destaque: true,
    },

    {
      id: 3,
      nome: "Mariana",
      hora: "12:34",
      texto:
        "Tenta focar nos conceitos primeiro (estado, props, componentes) e depois partir pra navegação, api, etc.",
    },

    {
      id: 4,
      nome: "João",
      hora: "12:36",
      texto:
        "Concordo! E o melhor é construir projetos pequenos pra fixar o conteúdo.",
    },
  ]);

  // ABRIR MENU
  const abrirMenu = (item) => {
    setMensagemSelecionada(item);

    setMenuVisible(true);
  };

  // EXCLUIR
  const excluirMensagem = () => {
    const novasMensagens =
      mensagens.filter(
        (item) =>
          item.id !==
          mensagemSelecionada.id
      );

    setMensagens(novasMensagens);

    setMenuVisible(false);
  };

  // ABRIR EDITAR
  const abrirEditar = () => {
    setTextoEditando(
      mensagemSelecionada.texto
    );

    setMenuVisible(false);

    setEditarVisible(true);
  };

  // SALVAR EDIÇÃO
  const salvarEdicao = () => {
    const novasMensagens =
      mensagens.map((item) => {
        if (
          item.id ===
          mensagemSelecionada.id
        ) {
          return {
            ...item,
            texto: textoEditando,
          };
        }

        return item;
      });

    setMensagens(novasMensagens);

    setEditarVisible(false);
  };

  return (
    <View style={styles.container}>
      <Header
        nomeTela={"Conversa"}
        temGoBack={true}
        telaDestino={"Titulo"}
      />

      {/* CAMINHO */}
      <View style={styles.pathContainer}>
        <Text style={styles.pathText}>
          {forum}
        </Text>

        <Ionicons
          name="chevron-forward"
          size={14}
          color="#777"
        />

        <Text style={styles.pathText}>
          {titulo}
        </Text>

        <Ionicons
          name="chevron-forward"
          size={14}
          color="#777"
        />

        <Text style={styles.pathActive}>
          Conversa
        </Text>
      </View>

      {/* CHAT */}
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{
          paddingBottom: 100,
        }}
      >
        {mensagens.map((item) => (
          <View
            key={item.id}
            style={[
              styles.messageCard,

              item.destaque &&
                styles.highlightCard,
            ]}
          >
            {/* TOPO */}
            <View style={styles.topRow}>
              {/* PERFIL */}
              <View style={styles.avatar}>
                <Ionicons
                  name="person"
                  size={20}
                  color="#fff"
                />
              </View>

              {/* INFO */}
              <View style={styles.userInfo}>
                <View style={styles.nameRow}>
                  <Text style={styles.name}>
                    {item.nome}
                  </Text>

                  {item.online && (
                    <>
                      <View
                        style={styles.onlineDot}
                      />

                      <Text
                        style={
                          styles.onlineText
                        }
                      >
                        Online
                      </Text>
                    </>
                  )}
                </View>

                {/* TEXTO */}
                <Text style={styles.message}>
                  {item.texto}
                </Text>
              </View>

              {/* HORA */}
              <Text style={styles.time}>
                {item.hora}
              </Text>
            </View>

            {/* FOOTER */}
            <View style={styles.footer}>
              {/* LIKE */}
              <View style={styles.likeContainer}>

                <Text style={styles.likeText}>
                  {item.likes}
                </Text>
              </View>

              {/* MENU */}
              <TouchableOpacity
                onPress={() =>
                  abrirMenu(item)
                }
              >
                <Feather
                  name="more-vertical"
                  size={18}
                  color="#777"
                />
              </TouchableOpacity>
            </View>
          </View>
        ))}
      </ScrollView>

      {/* INPUT */}
      <View style={styles.inputContainer}>
        <TouchableOpacity
          style={styles.clipButton}
        >
          <Feather
            name="paperclip"
            size={18}
            color="#666"
          />
        </TouchableOpacity>

        <TextInput
          placeholder="Escreva sua mensagem..."
          placeholderTextColor="#999"
          style={styles.input}
        />

        <TouchableOpacity
          style={styles.sendButton}
        >
          <Ionicons
            name="send"
            size={18}
            color="#fff"
          />
        </TouchableOpacity>
      </View>

      {/* MENU */}
      <Modal
        visible={menuVisible}
        transparent
        animationType="fade"
      >
        <TouchableOpacity
          style={styles.overlay}
          activeOpacity={1}
          onPress={() =>
            setMenuVisible(false)
          }
        >
          <View style={styles.menuContainer}>
            {/* EDITAR */}
            <TouchableOpacity
              style={styles.menuItem}
              onPress={abrirEditar}
            >
              <Feather
                name="edit-2"
                size={18}
                color="#2563EB"
              />

              <Text style={styles.menuText}>
                Editar
              </Text>
            </TouchableOpacity>

            {/* EXCLUIR */}
            <TouchableOpacity
              style={styles.menuItem}
              onPress={excluirMensagem}
            >
              <MaterialIcons
                name="delete-outline"
                size={20}
                color="#EF4444"
              />

              <Text
                style={[
                  styles.menuText,
                  {
                    color: "#EF4444",
                  },
                ]}
              >
                Excluir
              </Text>
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      </Modal>

      {/* MODAL EDITAR */}
      <Modal
        visible={editarVisible}
        transparent
        animationType="fade"
      >
        <View style={styles.overlay}>
          <View style={styles.editModal}>
            <Text style={styles.editTitle}>
              Editar mensagem
            </Text>

            <TextInput
              value={textoEditando}
              onChangeText={
                setTextoEditando
              }
              multiline
              style={styles.editInput}
            />

            <View style={styles.editButtons}>
              {/* CANCELAR */}
              <TouchableOpacity
                style={styles.cancelButton}
                onPress={() =>
                  setEditarVisible(false)
                }
              >
                <Text
                  style={
                    styles.cancelText
                  }
                >
                  Cancelar
                </Text>
              </TouchableOpacity>

              {/* SALVAR */}
              <TouchableOpacity
                style={styles.saveButton}
                onPress={salvarEdicao}
              >
                <Text
                  style={styles.saveText}
                >
                  Salvar
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
  },

  // CAMINHO
  pathContainer: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 15,
    marginTop: 12,
    marginBottom: 10,
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
  messageCard: {
    backgroundColor: "#fff",
    marginHorizontal: 10,
    marginBottom: 10,
    borderRadius: 16,
    padding: 12,
  },

  highlightCard: {
    backgroundColor: "#EEF2FF",
  },

  topRow: {
    flexDirection: "row",
  },

  avatar: {
    width: 38,
    height: 38,
    borderRadius: 19,

    backgroundColor: "#2563EB",

    justifyContent: "center",
    alignItems: "center",

    marginRight: 10,
  },

  userInfo: {
    flex: 1,
  },

  nameRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 6,
  },

  name: {
    fontSize: 14,
    fontWeight: "700",
    color: "#222",
  },

  onlineDot: {
    width: 7,
    height: 7,
    borderRadius: 4,
    backgroundColor: "#22C55E",
    marginLeft: 8,
    marginRight: 4,
  },

  onlineText: {
    color: "#22C55E",
    fontSize: 11,
  },

  message: {
    fontSize: 13,
    color: "#333",
    lineHeight: 20,
    marginTop: 2,
  },

  time: {
    fontSize: 11,
    color: "#888",
  },

  // FOOTER
  footer: {
    marginTop: 10,

    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  likeContainer: {
    flexDirection: "row",
    alignItems: "center",
  },

  likeText: {
    marginLeft: 5,
    color: "#666",
    fontSize: 13,
  },

  // INPUT
  inputContainer: {
    position: "absolute",
    bottom: 15,
    left: 10,
    right: 10,

    backgroundColor: "#fff",

    borderRadius: 18,

    flexDirection: "row",
    alignItems: "center",

    paddingHorizontal: 10,
    height: 55,

    elevation: 3,
  },

  clipButton: {
    marginRight: 8,
  },

  input: {
    flex: 1,
    fontSize: 14,
  },

  sendButton: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: "#2563EB",

    justifyContent: "center",
    alignItems: "center",
  },

  // MENU
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.2)",
    justifyContent: "center",
    alignItems: "center",
  },

  menuContainer: {
    width: 180,
    backgroundColor: "#fff",
    borderRadius: 16,
    paddingVertical: 10,

    elevation: 6,
  },

  menuItem: {
    flexDirection: "row",
    alignItems: "center",

    paddingVertical: 14,
    paddingHorizontal: 16,
  },

  menuText: {
    marginLeft: 12,
    fontSize: 14,
    color: "#333",
    fontWeight: "600",
  },

  // EDITAR
  editModal: {
    width: "85%",
    backgroundColor: "#fff",
    borderRadius: 20,
    padding: 20,
  },

  editTitle: {
    fontSize: 18,
    fontWeight: "700",
    color: "#2563EB",
    marginBottom: 15,
    textAlign: "center",
  },

  editInput: {
    minHeight: 120,

    borderWidth: 1,
    borderColor: "#E5E7EB",

    borderRadius: 14,

    padding: 12,

    textAlignVertical: "top",
  },

  editButtons: {
    flexDirection: "row",
    justifyContent: "space-between",

    marginTop: 20,
  },

  cancelButton: {
    borderWidth: 1,
    borderColor: "#D1D5DB",

    paddingVertical: 10,
    paddingHorizontal: 20,

    borderRadius: 12,
  },

  cancelText: {
    color: "#777",
    fontWeight: "600",
  },

  saveButton: {
    backgroundColor: "#2563EB",

    paddingVertical: 10,
    paddingHorizontal: 22,

    borderRadius: 12,
  },

  saveText: {
    color: "#fff",
    fontWeight: "700",
  },
});