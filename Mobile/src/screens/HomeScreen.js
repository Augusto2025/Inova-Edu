import React from "react";

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

        {/* PERFIL */}
        <TouchableOpacity
          style={styles.profileCard}
          activeOpacity={0.8}
        >

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
            Tec. Desenvolvimento de Sistemas
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
          decelerationRate="fast"
          snapToAlignment="start"
        >

          {/* CARD */}
          <TouchableOpacity
            style={styles.repoCard}
            activeOpacity={0.8}
          >

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
          <TouchableOpacity
            style={styles.repoCard}
            activeOpacity={0.8}
          >

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
          <TouchableOpacity
            style={styles.repoCard}
            activeOpacity={0.8}
          >

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
              placeholder="Buscar repositórios..."
              placeholderTextColor="#888"
              style={styles.searchInput}
            />

          </View>

          {/* TAGS */}
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={styles.tagsContainer}
          >

            <TouchableOpacity
              style={styles.tag}
              activeOpacity={0.8}
            >

              <Text style={styles.tagText}>
                React Native
              </Text>

            </TouchableOpacity>

            <TouchableOpacity
              style={styles.tag}
              activeOpacity={0.8}
            >

              <Text style={styles.tagText}>
                Python
              </Text>

            </TouchableOpacity>

            <TouchableOpacity
              style={styles.tag}
              activeOpacity={0.8}
            >

              <Text style={styles.tagText}>
                JavaScript
              </Text>

            </TouchableOpacity>

          </ScrollView>

        </View>

        {/* EVENTOS */}
        <Text style={styles.sectionTitle}>
          Próximos eventos
        </Text>

        <TouchableOpacity
          style={styles.eventCard}
          activeOpacity={0.8}
        >

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

        <TouchableOpacity
          style={styles.eventCard}
          activeOpacity={0.8}
        >

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

          <TouchableOpacity
            style={styles.forumTopic}
            activeOpacity={0.8}
          >

            <Text style={styles.forumText}>
              Python optimization tips
            </Text>

            <Text style={styles.hash}>
              #Python
            </Text>

          </TouchableOpacity>

        </View>

      </ScrollView>

    </View>
  );
}

const styles = StyleSheet.create({

  /* CONTAINER */

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
    marginBottom: 25,

    borderRadius: 28,

    padding: 22,

    alignItems: "center",

    elevation: 5,

    shadowColor: "#000",

    shadowOffset: {
      width: 0,
      height: 2,
    },

    shadowOpacity: 0.1,

    shadowRadius: 4,
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
    color: "#111",
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
    color: "#444",
  },

  /* TITULOS */

  sectionTitle: {
    fontSize: 20,
    fontWeight: "bold",

    marginBottom: 15,

    color: "#111",
  },

  /* REPOSITÓRIOS */

  repoContainer: {
    marginBottom: 22,
  },

  repoCard: {
    width: 180,

    backgroundColor: "#fff",

    borderRadius: 20,

    overflow: "hidden",

    marginRight: 15,

    elevation: 2,

    shadowColor: "#000",

    shadowOffset: {
      width: 0,
      height: 2,
    },

    shadowOpacity: 0.08,

    shadowRadius: 4,
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

    color: "#111",
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

    shadowColor: "#000",

    shadowOffset: {
      width: 0,
      height: 2,
    },

    shadowOpacity: 0.08,

    shadowRadius: 4,
  },

  searchTitle: {
    fontWeight: "bold",

    fontSize: 22,

    marginBottom: 15,

    color: "#111",
  },

  searchBox: {
    backgroundColor: "#f1f1f1",

    borderRadius: 18,

    paddingHorizontal: 15,
  },

  searchInput: {
    height: 50,
    fontSize: 15,
    color: "#111",
  },

  /* TAGS */

  tagsContainer: {
    paddingTop: 15,
  },

  tag: {
    backgroundColor: "#ececec",

    paddingHorizontal: 16,
    paddingVertical: 10,

    borderRadius: 14,

    marginRight: 10,
  },

  tagText: {
    color: "#333",
    fontWeight: "500",
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

    shadowColor: "#000",

    shadowOffset: {
      width: 0,
      height: 2,
    },

    shadowOpacity: 0.08,

    shadowRadius: 4,
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

    color: "#111",
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

    shadowColor: "#000",

    shadowOffset: {
      width: 0,
      height: 2,
    },

    shadowOpacity: 0.08,

    shadowRadius: 4,
  },

  forumText: {
    fontWeight: "bold",
    fontSize: 15,

    color: "#111",
  },

  hash: {
    color: "#666",
  },

});