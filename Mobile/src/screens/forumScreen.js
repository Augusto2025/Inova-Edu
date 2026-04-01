import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Image,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";

export default function ForumScreen() {
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
      <View style={styles.searchContainer}>
        <Ionicons name="search" size={20} color="#999" />
        <TextInput placeholder="...Buscar tópicos" style={styles.input} />
        <TouchableOpacity style={styles.searchButton}>
          <Text style={{ color: "#fff" }}>Buscar</Text>
        </TouchableOpacity>
      </View>


        {/* Botões de criar tópico e meus tópicos */}
      <View styles={styles.buttonsCriar}>
        <TouchableOpacity style={styles.buttonCriar}>
          <Text style={{ color: "#fff" }}>Criar tópico</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.buttonCriar}>
          <Text style={{ color: "#fff" }}>Meus tópicos</Text>
        </TouchableOpacity>
      </View>

      
      
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f2f2f2",
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
  searchContainer: {
  flexDirection: "row",
  alignItems: "center",
  backgroundColor: "#fff",
  borderRadius: 30, // 🔥 bem arredondado
  paddingHorizontal: 15,
  paddingVertical: 10,
  marginHorizontal: 15,
  marginTop: 20,
  elevation: 3, // sombra leve
  },

  input: {
    flex: 1,
    marginLeft: 10,
    fontSize: 14,
  },

  searchButton: {
    backgroundColor: "#ff8c00",
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20, // botão arredondado
  },

 




  //  Botões de criar tópico 
  buttonsCriar: {
  flexDirection: "row-reverse", // 🔥 ESSA LINHA faz ficar lado a lado
  },

  buttonCriar: {
    flex: 1, // divide espaço igualmente
    backgroundColor: "#1e4f8a",
    padding: 12,
    margin: 5,
    borderRadius: 10,
    alignItems: "center",
    // width: "50%",
    
  },

  texto: {
    color: "#fff",
    fontWeight: "bold",
  },
});
