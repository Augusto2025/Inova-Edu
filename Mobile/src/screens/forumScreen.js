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
import HeaderForum from "../components/HeaderForum";
import FooterForum from "../components/FooterForum";

export default function ForumScreen() {
  const [modalVisible, setModalVisible] = useState(false);

  const [topicos, setTopicos] = useState([
    "Meu primeiro tópico",
    "Meu segundo tópico",
    "Meu terceiro tópico",
    "Meu terceiro tópico",
    "Meu terceiro tópico",
    "Meu terceiro tópico",
    
    
  ]);

  const [novoTopico, setNovoTopico] = useState("");
  const [isExemplo, setIsExemplo] = useState(true);

  return (
    <View style={styles.container}>
      <HeaderForum onBack={() => console.log("Voltar")} />


      {/* Busca */}
      <View style={styles.searchWrapper}>
        <View style={styles.searchContainer}>
          <Ionicons name="search" size={20} color="#1e4f8a" />
          <TextInput
            placeholder="Pesquisar Tópicos..."
            placeholderTextColor="#999"
            style={styles.input}
          />
        </View>
      </View>

      {/* Título */}
      <View style={styles.containerTopicos}>
        <Text style={styles.textoTopicos}>Tópicos Criados</Text>
        <View style={styles.linha} />
      </View>

      {/* Lista de tópicos */}
      
      {isExemplo ? (
        <View>
          {topicos.map((item, index) => (
            <View key={index} style={styles.card}>
              <Text style={[styles.nomeTopico, styles.nomeExemplo]}>
                {item}
              </Text>
            </View>
          ))}
        </View>
      ) : (
        // 🔥 TÓPICOS REAIS (COM SCROLL + LIMITE)
        <ScrollView style={{ maxHeight: 440, marginBottom: 100 }}>
          {topicos.map((item, index) => (
            <View key={index} style={styles.card}>
              <Text style={styles.nomeTopico}>{item}</Text>

              <View style={styles.acoes}>
                <TouchableOpacity>
                  <Ionicons name="create-outline" size={20} color="#1e4f8a" />
                </TouchableOpacity>

                <TouchableOpacity
                  style={{ marginLeft: 15 }}
                  onPress={() => {
                    const novos = topicos.filter((_, i) => i !== index);
                    setTopicos(novos);
                  }}
                >
                  <Ionicons name="trash-outline" size={20} color="#ff0000" />
                </TouchableOpacity>
              </View>
            </View>
          ))}
        </ScrollView>
      )}

      {/* Botão flutuante */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => setModalVisible(true)}
      >
        <Ionicons name="add" size={28} color="#fff" />
      </TouchableOpacity>

      {/* Modal */}
      <Modal visible={modalVisible} transparent animationType="fade">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContainer}>
            <View style={{ alignItems: "center" }}>
              <Text style={styles.modalTitle}>Criar Tópico</Text>
              <View style={styles.linhaModal} />
            </View>

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

              <TouchableOpacity
                onPress={() => {
                  if (novoTopico.trim() !== "") {
                    if (isExemplo) {
                      setTopicos([novoTopico]);
                      setIsExemplo(false);
                    } else {
                      setTopicos([...topicos, novoTopico]);
                    }

                    setModalVisible(false);
                    setNovoTopico("");
                  }
                }}
              >
                <Text style={styles.bottomCriar}>Criar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>




      <FooterForum />

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f2f2f2", // cor de fundo clara para destacar os elementos
  },

  // busca
  searchWrapper: {
    paddingHorizontal: 20,
    marginTop: 15,
    paddingHorizontal: 10,
    paddingBottom: 10,
  },

  searchContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#fff",
    borderRadius: 25, // bem arredondado (WhatsApp)
    paddingHorizontal: 12,
    height: 40,
  },

  input: {
    flex: 1,
    marginLeft: 8,
    fontSize: 14,
    color: "#000",
  },


  // Tópicos criados
  containerTopicos: {
    alignItems: "center",
    marginTop: 10,
  },

  textoTopicos: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#1e4f8a",
  },

  linha: {
    width: 150, // 🔥 controla o tamanho da linha
    height: 3,
    backgroundColor: "#ff8c00",
    marginTop: 5,
    borderRadius: 2,
  },

  //CARDS TOPICOS CRIADOS
  nomeExemplo: {
    color: "#ccc",
    fontStyle: "italic",
    opacity: 0.6,
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
    elevation: 2, // sombra Android
  },

  nomeTopico: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#333",
  },

  acoes: {
    flexDirection: "row",
    alignItems: "center",
  },

  //BOTÃO FLUTUANTE
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
    elevation: 5,
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
    borderBottomWidth: 2,
    borderBottomColor: "#ff8c00",
    paddingBottom: 6,
    marginBottom: 15,
  },

  bottomCriar: {
    backgroundColor: "#ff8c00",
    color: "#fff",
    fontWeight: "bold",
    textAlign: "center",
    paddingVertical: 8,
    paddingHorizontal: 20,
    borderRadius: 8,
  },

  bottomCancelar: {
    color: "#999",
    fontWeight: "bold",
    textAlign: "center",

    paddingVertical: 8,
    paddingHorizontal: 8,

    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#ccc",
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





















});
