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
import { Ionicons, Feather, MaterialIcons } from "@expo/vector-icons";
import Header from "../components/Header";
import BarraPesquisa from "../components/BarraPesquisa";

export default function ForumScreen({ navigation }) {
  const [modalVisible, setModalVisible] = useState(false);
  const [modalEditarVisible, setModalEditarVisible] = useState(false);

  const [topicos, setTopicos] = useState([
    {
      titulo: "Meu primeiro tópico",
      descricao:
        "Estou tendo dificuldade para entender o useEffect no React Native...",
      categoria: "React Native",
      mensagens: 12,
      tempo: "há 2 min",
      cor: "#0e68d6",
    },
    {
      titulo: "Meu segundo tópico",
      descricao:
        "Alguém pode me ajudar com o useState? Não estou entendendo...",
      categoria: "JavaScript",
      mensagens: 8,
      tempo: "Ontem",
      cor: "#0e68d6",
    },
    {
      titulo: "Meu terceiro tópico",
      descricao: "Qual a melhor forma de organizar componentes em pastas?",
      categoria: "React Native",
      mensagens: 5,
      tempo: "2 dias atrás",
      cor: "#0e68d6",
    },
  ]);

  const [novoTopico, setNovoTopico] = useState("");
  const [topicoEditando, setTopicoEditando] = useState("");
  const [indexEditando, setIndexEditando] = useState(null);

  const abrirTopico = (topico) => {
    navigation.navigate("Titulo", { topico });
  };

  const criarTopico = () => {
    if (novoTopico.trim() === "") return;

    const novo = {
      titulo: novoTopico,
      descricao: "Novo tópico criado...",
      categoria: "React Native",
      mensagens: 0,
      tempo: "Agora",
      cor: "#0e68d6",
    };

    setTopicos([...topicos, novo]);

    setNovoTopico("");
    setModalVisible(false);
  };

  const abrirEditar = (item, index) => {
    setTopicoEditando(item.titulo);
    setIndexEditando(index);
    setModalEditarVisible(true);
  };

  const salvarEdicao = () => {
    if (topicoEditando.trim() === "") return;

    const novos = [...topicos];

    novos[indexEditando].titulo = topicoEditando;

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
      <Header nomeTela={"Forum"}/>

      {/* BUSCA */}
      <BarraPesquisa />

      {/* LISTA DE TÓPICOS */}
      <ScrollView showsVerticalScrollIndicator={false}>
        {topicos.map((item, index) => (
          <TouchableOpacity
            key={index}
            style={styles.card}
            onPress={() => abrirTopico(item)}
          >
            {/* ÍCONE */}
            <View
              style={[
                styles.iconBox,
                { backgroundColor: item.cor },
              ]}
            >
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
                  <Text style={styles.time}>{item.tempo}</Text>

                 
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
                {item.descricao}
              </Text>

              {/* RODAPÉ */}
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
                      {item.categoria}
                    </Text>
                  </View>
                </View>

                {/* BOTÕES */}
                <View style={styles.actions}>
                  <TouchableOpacity
                    style={styles.editButton}
                    onPress={() => abrirEditar(item, index)}
                  >
                    <Feather
                      name="edit-2"
                      size={18}
                      color="#5B5EF7"
                    />
                  </TouchableOpacity>

                  <TouchableOpacity
                    style={styles.deleteButton}
                    onPress={() => excluirTopico(index)}
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

            <View style={styles.linha} />

            <TextInput
              placeholder="Digite o título..."
              value={novoTopico}
              onChangeText={setNovoTopico}
              style={styles.modalInput}
            />

            <View style={styles.modalButtons}>
              <TouchableOpacity
                onPress={() => setModalVisible(false)}
              >
                <Text style={styles.bottomCancelar}>
                  Cancelar
                </Text>
              </TouchableOpacity>

              <TouchableOpacity onPress={criarTopico}>
                <Text style={styles.bottomCriar}>Criar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

      {/* MODAL EDITAR */}
      <Modal
        visible={modalEditarVisible}
        transparent
        animationType="fade"
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContainer}>
            <Text style={styles.modalTitle}>Editar Tópico</Text>
            <View style={styles.titleUnderline} />

            <TextInput
              value={topicoEditando}
              onChangeText={setTopicoEditando}
              style={styles.modalInput}
            />

            <View style={styles.modalButtons}>
              <TouchableOpacity
                onPress={() => setModalEditarVisible(false)}
              >
                <Text style={styles.bottomCancelar}>
                  Cancelar
                </Text>
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

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f6f6fb",
  },
  
  titleUnderline: {
    width: 120,
    height: 3,
    backgroundColor: "#ff8c00",
    alignSelf: "center",
    marginBottom: 20,
    borderRadius: 10,
  },


  // CARD
  card: {
    backgroundColor: "#fff",
    marginHorizontal: 12,
    marginBottom: 14,
    borderRadius: 22,
    padding: 16,
    flexDirection: "row",
    elevation: 2,
  },

  iconBox: {
    width: 46,
    height: 46,
    borderRadius: 23,
    justifyContent: "center",
    alignItems: "center",
    marginRight: 14,
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

  // BOTÃO FLUTUANTE
  fab: {
    position: "absolute",
    bottom: 25,
    right: 20,
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: "#ff8c00",
    justifyContent: "center",
    alignItems: "center",
    elevation: 5,
  },

  // MODAL
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

  linha: {
    height: 1,
    backgroundColor: "#ddd",
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
    paddingVertical: 10,
    paddingHorizontal: 18,
    borderRadius: 8,
    overflow: "hidden",
  },

  bottomCancelar: {
    color: "#999",
    borderWidth: 1,
    borderColor: "#ddd",
    paddingVertical: 10,
    paddingHorizontal: 18,
    borderRadius: 8,
    overflow: "hidden",
  },
});