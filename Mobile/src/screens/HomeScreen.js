import React, { useState } from "react";
import * as ImagePicker from "expo-image-picker";
import Header from "../components/Header"; 

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
      <Header foto={foto} escolherImagem={escolherImagem} />

      {/* BOAS VINDAS */}
      <View style={styles.topo}>
        <Text style={styles.boasVindas}>👋 Olá, Alcides</Text>
        <Text style={styles.sub}>Pronto pra aprender hoje? 🚀</Text>
      </View>

      {/* DESTAQUE */}
      <View style={styles.cardDestaque}>
        <Text style={styles.tituloDestaque}>🔥 Desafio do dia</Text>
        <Text style={styles.textoDestaque}>
          Crie um app de lista com React Native
        </Text>
      </View>

      {/* AÇÕES RÁPIDAS */}
      <View style={styles.actions}>
        <TouchableOpacity style={styles.btn}>
          <Text>📚</Text>
          <Text>Repo</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.btn}>
          <Text>📅</Text>
          <Text>Eventos</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.btn}>
          <Text>💬</Text>
          <Text>Fórum</Text>
        </TouchableOpacity>
      </View>

      {/* BUSCA */}
      <View style={styles.card}>
        <Text style={styles.titulo}>🔎 Buscar</Text>

        <TextInput
          placeholder="Buscar repositórios, arquivos..."
          style={styles.input}
        />
      </View>

      {/* REPOSITÓRIOS */}
      <View style={styles.card}>
        <Text style={styles.titulo}>📚 Repositórios recentes</Text>

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
    padding: 20,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  logo: {
    width: 60,
    height: 60,
    tintColor: "white",
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
    padding: 20,
  },

  boasVindas: {
    fontSize: 22,
    fontWeight: "bold",
  },

  sub: {
    color: "gray",
  },

  cardDestaque: {
    backgroundColor: "#1459b3",
    margin: 15,
    padding: 20,
    borderRadius: 15,
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
    padding: 15,
    borderRadius: 12,
    alignItems: "center",
    elevation: 3,
  },

  card: {
    backgroundColor: "#fff",
    margin: 15,
    padding: 15,
    borderRadius: 15,
    elevation: 3,
  },

  titulo: {
    fontWeight: "bold",
    marginBottom: 10,
  },

  input: {
    backgroundColor: "#f0f0f0",
    borderRadius: 10,
    padding: 10,
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
