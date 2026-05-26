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

  async function escolherImagem() {

    const permissao =
      await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (!permissao.granted) {
      alert("Permissão negada!");
      return;
    }

    const resultado =
      await ImagePicker.launchImageLibraryAsync({
        mediaTypes:
          ImagePicker.MediaTypeOptions.Images,
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
        nomeTela="Olá, Alcides 👋"
        subtitulo="Home"
      />

      {/* CONTEÚDO */}
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >

        {/* CARD PERFIL */}
        <TouchableOpacity style={styles.profileCard}>

          <Image
            source={{
              uri: "https://i.pravatar.cc/300",
            }}
            style={styles.profileImage}
          />

          <Text style={styles.profileTitle}>
            Alcides
          </Text>

          <Text style={styles.profileSubtitle}>
            Toque para ver perfil
          </Text>

          <View style={styles.line} />

          <Text style={styles.profileSkill}>
            tec. desenvolvimento de sistema
          </Text>

        </TouchableOpacity>

        {/* REPOSITÓRIOS */}
        <Text style={styles.sectionTitle}>
          Repositórios
        </Text>

        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.repoContainer}
        >

          {/* CARD */}
          <TouchableOpacity style={styles.repoCard}>

            <Image
              source={{
                uri:
                  "https://reactnative.dev/img/tiny_logo.png",
              }}
              style={styles.repoImage}
            />

            <Text style={styles.repoTitle}>
              My App - RN
            </Text>

            <Text style={styles.repoInfo}>
              ↻ 1 commits ⭐ 72
            </Text>

          </TouchableOpacity>

          {/* CARD */}
          <TouchableOpacity style={styles.repoCard}>

            <Image
              source={{
                uri:
                  "https://cdn-icons-png.flaticon.com/512/5968/5968350.png",
              }}
              style={styles.repoImage}
            />

            <Text style={styles.repoTitle}>
              Python Script
            </Text>

            <Text style={styles.repoInfo}>
              ↻ 1 commits ⭐ 32
            </Text>

          </TouchableOpacity>

          {/* CARD */}
          <TouchableOpacity style={styles.repoCard}>

            <Image
              source={{
                uri:
                  "https://cdn-icons-png.flaticon.com/512/5968/5968292.png",
              }}
              style={styles.repoImage}
            />

            <Text style={styles.repoTitle}>
              Web Portal
            </Text>

            <Text style={styles.repoInfo}>
              ↻ 4 commits ⭐ 20
            </Text>

          </TouchableOpacity>

        </ScrollView>

        {/* SEARCH + TAGS */}
        <View style={styles.searchContainer}>

          <Text style={styles.searchTitle}>
            Seus Repositórios
          </Text>

          {/* BUSCA */}
          <View style={styles.searchBox}>
            <TextInput
              placeholder="buscar repositórios..."
              style={styles.searchInput}
            />
          </View>

          {/* TAGS */}
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            style={styles.tagsContainer}
          >

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
        <Text style={styles.sectionTitle}>
          Próximos eventos
        </Text>

        <TouchableOpacity style={styles.eventCard}>

          <View style={styles.eventBar} />

          <View>

            <Text style={styles.eventTitle}>
              Semana Tech
            </Text>

            <Text style={styles.eventDate}>
              Amanhã às 10h
            </Text>

          </View>

        </TouchableOpacity>

        <TouchableOpacity style={styles.eventCard}>

          <View style={styles.eventBar} />

          <View>

            <Text style={styles.eventTitle}>
              React Native Meetup
            </Text>

            <Text style={styles.eventDate}>
              25 Mai, 19h
            </Text>

          </View>

        </TouchableOpacity>

        {/* FORUM */}
        <View style={styles.forumCard}>

          <Text style={styles.sectionTitle}>
            Fórum ativo
          </Text>

          <Text style={styles.forumSubtitle}>
            3 novas respostas
          </Text>

          <View style={styles.forumTopic}>

            <Text style={styles.forumText}>
              Python optimization tips
            </Text>

            <Text style={styles.hash}>
              #Python
            </Text>

          </View>

        </View>

      </ScrollView>

    </View>
  );
}

const styles = StyleSheet.create({

  safe: {
    flex: 1,
    backgroundColor: "#2155f3",
  },

  container: {
    flex: 1,
    backgroundColor: "#f5f7fb",
  },

  scrollContent: {
    paddingHorizontal: 18,
    paddingBottom: 120,
  },

  /* PERFIL */

  profileCard: {
    backgroundColor: "#fff",
    marginTop: 15,
    borderRadius: 28,
    padding: 22,
    alignItems: "center",
    elevation: 5,
    marginBottom: 25,
  },

  profileImage: {
    width: 95,
    height: 95,
    borderRadius: 50,
    marginBottom: 12,
  },

  profileTitle: {
    fontSize: 30,
    fontWeight: "bold",
  },

  profileSubtitle: {
    color: "#777",
    marginBottom: 15,
  },

  line: {
    width: "100%",
    height: 1,
    backgroundColor: "#ddd",
    marginBottom: 12,
  },

  profileSkill: {
    fontSize: 16,
  },

  /* TITULOS */

  sectionTitle: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 15,
    color: "#111",
  },

  /* REPO */

  repoContainer: {
    marginBottom: 22,
  },

  repoCard: {
    width: 180,
    backgroundColor: "#fff",
    borderRadius: 20,
    overflow: "hidden",
    marginRight: 15,
    elevation: 1,
  },

  repoImage: {
    width: "100%",
    height: 100,
    resizeMode: "cover",
  },

  repoTitle: {
    fontWeight: "bold",
    paddingHorizontal: 12,
    paddingTop: 12,
    fontSize: 16,
  },

  repoInfo: {
    paddingHorizontal: 12,
    paddingBottom: 15,
    color: "#666",
    fontSize: 12,
  },

  /* SEARCH */

  searchContainer: {
    backgroundColor: "#fff",
    borderRadius: 24,
    padding: 18,
    marginBottom: 25,
    elevation: 4,
  },

  searchTitle: {
    fontWeight: "bold",
    fontSize: 22,
    marginBottom: 15,
  },

  searchBox: {
    backgroundColor: "#f1f1f1",
    borderRadius: 18,
    paddingHorizontal: 15,
  },

  searchInput: {
    height: 50,
    fontSize: 15,
  },

  /* TAGS */

  tagsContainer: {
    marginTop: 15,
  },

  tag: {
    backgroundColor: "#ececec",
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 14,
    marginRight: 10,
  },

  /* EVENTOS */

  eventCard: {
    backgroundColor: "#fff",
    borderRadius: 22,
    padding: 16,
    marginBottom: 14,
    flexDirection: "row",
    alignItems: "center",
    elevation: 3,
  },

  eventBar: {
    width: 5,
    height: "100%",
    backgroundColor: "#2155f3",
    borderRadius: 10,
    marginRight: 15,
  },

  eventTitle: {
    fontWeight: "bold",
    fontSize: 18,
  },

  eventDate: {
    color: "#666",
    marginTop: 2,
  },

  /* FORUM */

  forumCard: {
    marginTop: 10,
    marginBottom: 20,
  },

  forumSubtitle: {
    marginBottom: 12,
    color: "#666",
  },

  forumTopic: {
    backgroundColor: "#fff",
    padding: 18,
    borderRadius: 20,
    flexDirection: "row",
    justifyContent: "space-between",
    elevation: 3,
  },

  forumText: {
    fontWeight: "bold",
    fontSize: 15,
  },

  hash: {
    color: "#666",
  },

});