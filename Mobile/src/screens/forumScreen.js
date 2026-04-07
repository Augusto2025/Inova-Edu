import React, { useState } from "react";
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Image, Modal } from "react-native";
import { Ionicons } from "@expo/vector-icons";



export default function ForumScreen() {
  const [modalVisible, setModalVisible] = useState(false);
  const [novoTopico, setNovoTopico] = useState("");

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity>
          <Ionicons name="arrow-back" top={20} size={24} color="#fff" />
        </TouchableOpacity>

        <Text style={styles.title}>Forum</Text>

        <Image
          source={{ uri: "https://i.pravatar.cc/100" }}
          style={styles.avatar}
        />
      </View>

      {/* Busca */}
      <View style={styles.searchWrapper}>
        <View style={styles.searchContainer}>
          <Ionicons name="search" size={20} color="#1e4f8a" />

          <TextInput
            placeholder="Pesquisar Tópicos... "
            style={styles.input}
          />
        </View>
      </View>


      {/* Botões de criar tópico e meus tópicos */}
      {/* <View style={styles.buttonsCriar}>
        <TouchableOpacity style={styles.buttonCriar}>
          <Text style={styles.texto}>Criar tópico</Text>
        </TouchableOpacity>
      </View> */}


      {/* Mostra na tela os topicos criados */}


      <View style={styles.containerTopicos}>
        <Text style={styles.textoTopicos}>Tópicos Criados</Text>
        <View style={styles.linha} />
      </View>

      {/* card de tópico criado */}

      <View>
        {/* Card 1 */}
        <View style={styles.card}>
          <Text style={styles.nomeTopico}>Meu primeiro tópico</Text>

          <View style={styles.acoes}>
            <TouchableOpacity>
              <Ionicons name="create-outline" size={20} color="#1e4f8a" />
            </TouchableOpacity>

            <TouchableOpacity style={{ marginLeft: 15 }}>
              <Ionicons name="trash-outline" size={20} color="#ff0000" />
            </TouchableOpacity>
          </View>
        </View>

        {/* Card 2 */}
        <View style={styles.card}>
          <Text style={styles.nomeTopico}>Meu segundo tópico</Text>

          <View style={styles.acoes}>
            <TouchableOpacity>
              <Ionicons name="create-outline" size={20} color="#1e4f8a" />
            </TouchableOpacity>

            <TouchableOpacity style={{ marginLeft: 15 }}>
              <Ionicons name="trash-outline" size={20} color="#ff0000" />
            </TouchableOpacity>
          </View>
        </View>

        {/* Card 3 */}
        <View style={styles.card}>
          <Text style={styles.nomeTopico}>Meu terceiro tópico</Text>

          <View style={styles.acoes}>
            <TouchableOpacity>
              <Ionicons name="create-outline" size={20} color="#1e4f8a" />
            </TouchableOpacity>

            <TouchableOpacity style={{ marginLeft: 15 }}>
              <Ionicons name="trash-outline" size={20} color="#ff0000" />
            </TouchableOpacity>
          </View>
        </View>
      </View>


      {/* BOTÃO FLUTUANTE PARA CRIAR NOVO TÓPICO */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => setModalVisible(true)}
      >
        <Ionicons name="add" size={28} color="#fff" />
      </TouchableOpacity>

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
                  console.log(novoTopico);
                  setModalVisible(false);
                  setNovoTopico("");
                }}
              >
                <Text style={styles.bottomCriar}> Criar </Text>
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
    backgroundColor: "#f2f2f2", // cor de fundo clara para destacar os elementos
  },

  header: {
    backgroundColor: "#1e4f8a",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    padding: 50,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,

  },

  title: {
    color: "#fff",
    fontSize: 20,
    fontWeight: "bold",
    top: 20,
  },

  avatar: {
    width: 35,
    height: 35,
    borderRadius: 20,
    top: 20,
  },

  // busca
  searchWrapper: {
    marginHorizontal: 20,

    marginTop: 30,
    // height: 10,

    borderBottomWidth: 2,
    borderBottomColor: "#ff8c00",
    borderBottomLeftRadius: 15,
    borderBottomRightRadius: 15,

    overflow: "hidden", // 🔥 ESSENCIAL
  },

  searchContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#f2f2f2",
    // height: 40,
    paddingHorizontal: 12,
    paddingVertical: 6,

    borderBottomLeftRadius: 15, // mantém alinhado com o wrapper
    borderBottomRightRadius: 15, // mantém alinhado com o wrapper
  },

  input: {
    flex: 1,
    marginLeft: 10,
    fontSize: 14,
    height: 40,
  },



  //  Botões de criar tópico 
  // buttonsCriar: {
  //   flexDirection: "row-reverse",
  //   marginTop: 20, // Deixar o botao mais próximo do campo de busca
  //   marginHorizontal: 20,

  // },

  // buttonCriar: {
  //   flex: 1,
  //   backgroundColor: "#1e4f8a",
  //   padding: 12,
  //   margin: 5,
  //   borderRadius: 10,
  //   alignItems: "center",
  // },

  // texto: {
  //   fontSize: 16,
  //   color: "#fff",
  //   fontWeight: "bold",
  // },

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
    bottom: 100,
    right: 20,
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
