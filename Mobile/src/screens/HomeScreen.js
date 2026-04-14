import React, { useState } from "react";
import { SafeAreaView } from 'react-native-safe-area-context';
import * as ImagePicker from "expo-image-picker";

import {
  View,
  Text,
  StyleSheet,
  TextInput,
  ScrollView,
  TouchableOpacity,
  Image,
} from "react-native";

export default function HomeScreen() {
  const [foto, setFoto] = useState(null);
  const logo = require("../../assets/LOGOBRANCO.png");

  async function escolherImagem() {
    const permissao = await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (!permissao.granted) {
      alert("Permissão negada!");
      return;
    }

    const resultado = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 1,
    });

    if (!resultado.canceled) {
      setFoto(resultado.assets[0].uri);
    }
  }

  return (
    <ScrollView style={styles.container}>
      {/* HEADER */}
      <View style={styles.header}>
        <Text style={styles.boasVindas}>👋 Olá, Alcides</Text>

        <View style={styles.user}>
          <TouchableOpacity onPress={escolherImagem}>
            {foto ? (
              <Image source={{ uri: foto }} style={styles.avatar} />
            ) : (
              <View style={styles.avatarFallback}>
                <Text style={styles.letra}>A</Text>
              </View>
            )}
          </TouchableOpacity>
        </View>
      </View>

      {/* BOAS VINDAS */}
      <View style={styles.topo}>
      </View>

      {/* REPOSITÓRIOS + BUSCA */}
      <View style={styles.card}>
        <Text style={styles.titulo}>📚 Repositórios</Text>

        {/* 🔎 BUSCA DENTRO */}
        <View style={styles.searchBox}>
          <Text>🔎</Text>
          <TextInput
            placeholder="Buscar repositórios..."
            style={styles.searchInput}
          />
        </View>

        {/* LISTA */}
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          <TouchableOpacity style={styles.tag}>
            <Text>React Native</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.tag}>
            <Text>Python</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.tag}>
            <Text>JavaScript</Text>
          </TouchableOpacity>
        </ScrollView>
      </View>

      {/* EVENTOS */}
      <View style={styles.card}>
        <Text style={styles.titulo}>📅 Próximos eventos</Text>
        <Text>Semana Tech</Text>
        <Text style={styles.subText}>Amanhã às 10h</Text>
      </View>

      {/* FORUM */}
      <View style={styles.card}>
        <Text style={styles.titulo}>💬 Fórum ativo</Text>
        <Text>3 novas respostas</Text>
        <Text style={styles.subText}>#ReactNative</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f7fb",
  },

 header: {
  backgroundColor: "#1459b3",
  paddingTop: 40, // 👈 AQUI
  padding: 4, // 👈 AQUI
  flexDirection: "row",
  justifyContent: "space-between",
  alignItems: "center",
},


  user: {
    alignItems: "center",
  },

  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    borderWidth: 2,
    borderColor: "#fff",
  },

  avatarFallback: {
    
    top: -5,
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: "#6c63ff",
    justifyContent: "center",
    alignItems: "center",
  },

  letra: {
    color: "#fff",
    fontWeight: "bold",
  },

  nome: {
    color: "#fff",
    marginTop: 5,
  },

  topo: {
    padding: 10,
  },

  boasVindas: {
    paddingTop: 20,
    paddingBottom: 30,
    fontSize: 22,
    color: "#fff",
    fontWeight: "bold",
    

  },

  sub: {
    color: "gray",
  },

  cardDestaque: {
    backgroundColor: "#1459b3",
    margin: 15,
    marginTop: -20,
    padding: 20,
    borderRadius: 20,
  },

  tituloDestaque: {
    color: "#fff",
    fontWeight: "bold",
    marginBottom: 5,
  },

  textoDestaque: {
    color: "#fff",
  },

  actions: {
    flexDirection: "row",
    justifyContent: "space-around",
    marginVertical: 10,
  },

  btn: {
    backgroundColor: "#fff",
    padding: 18,
    borderRadius: 15,
    alignItems: "center",
    width: 90,
    elevation: 4,
  },

  card: {
    backgroundColor: "#fff",
    margin: 15,
    padding: 15,
    borderRadius: 15,
    elevation: 4,
  },

  titulo: {
    fontWeight: "bold",
    marginBottom: 10,
  },

  // 🔥 BUSCA BONITA
  searchBox: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#f0f0f0",
    borderRadius: 12,
    padding: 10,
    marginBottom: 10,
  },

  searchInput: {
    flex: 1,
    marginLeft: 10,
  },

  tag: {
    backgroundColor: "#e0e0e0",
    padding: 10,
    borderRadius: 10,
    marginRight: 10,
  },

  subText: {
    color: "gray",
    fontSize: 12,
  },
});
