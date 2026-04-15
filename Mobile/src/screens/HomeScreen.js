import React, { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
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
    <View style={styles.safe}>
      
      {/* HEADER */}
      <Header
        foto={foto}
        escolherImagem={escolherImagem}
        nomeTela="Home"
      />

      {/* CONTEÚDO */}
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.scrollContent}
      >

        {/* REPOSITÓRIOS */}
        <View style={[styles.card, styles.cardTop]}>
          <Text style={styles.titulo}>📚 Repositórios</Text>

          <View style={styles.searchBox}>
            <Text>🔎</Text>
            <TextInput
              placeholder="Buscar repositórios..."
              style={styles.searchInput}
            />
          </View>

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

        {/* FÓRUM */}
        <View style={styles.card}>
          <Text style={styles.titulo}>💬 Fórum ativo</Text>
          <Text>3 novas respostas</Text>
          <Text style={styles.subText}>#ReactNative</Text>
        </View>

      </ScrollView>
      </View>
    
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: "#fff",
  },

  container: {
    flex: 1,
    backgroundColor: "#f5f7fb",
  },

  scrollContent: {
    paddingBottom: 120, // espaço pro menu
    paddingTop: 80,
  },

  card: {
    backgroundColor: "#fff",
    marginHorizontal: 15,
    marginBottom: 15,
    padding: 15,
    borderRadius: 20,
    elevation: 5,
  },

  // 🔥 só o primeiro card sobe
  cardTop: {
    marginTop: 40,
  },

  titulo: {
    fontWeight: "bold",
    marginBottom: 10,
    fontSize: 16,
  },

  // 🔍 busca
  searchBox: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#f1f3f6",
    borderRadius: 15,
    padding: 12,
    marginBottom: 12,
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