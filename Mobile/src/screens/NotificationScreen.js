import React, { useState } from "react";

import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from "react-native";

import Header from "../components/Header";

import { Ionicons } from "@expo/vector-icons";

export default function NotificationScreen() {

  const [filtroAtivo, setFiltroAtivo] =
    useState("Todas");

  const notificacoes = [

    {
      id: 1,
      tipo: "Forum",
      titulo: "Carlos respondeu seu tópico",
      descricao: '"Como usar useState?"',
      tempo: "12 min",
      icon: "chatbubble",
      cor: "#5865F2",
      novo: true,
    },

    {
      id: 2,
      tipo: "Eventos",
      titulo: "Novo evento disponível",
      descricao: "React Native Meetup",
      tempo: "1 hora",
      icon: "calendar",
      cor: "#8B5CF6",
      novo: true,
    },

    // {
    // //   id: 3,
    // //   // tipo: "Repos",
    // //   titulo: "Repositório atualizado",
    // //   descricao: "2 novos commits",
    // //   tempo: "Ontem",
    // //   icon: "flash",
    // //   cor: "#0EA5E9",
    // //   novo: false,
    // // },

    {
      id: 4,
      tipo: "Sistema",
      titulo: "Conta verificada",
      descricao: "Seu perfil foi atualizado",
      tempo: "2 dias",
      icon: "shield-checkmark",
      cor: "#F59E0B",
      novo: false,
    },
  ];

  const notificacoesFiltradas =
    filtroAtivo === "Todas"
      ? notificacoes
      : notificacoes.filter(
          (n) => n.tipo === filtroAtivo
        );

  return (
    <View style={styles.container}>

      {/* HEADER */}
      <Header
        nomeTela="Notificações 🔔"
        subtitulo="Atualizações recentes"
      />

      {/* FILTROS */}
      <View style={styles.filterWrapper}>

        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.filterContainer}
        >

          {[
            "Todas",
            "Forum",
            "Eventos",
            // "Repos",
            "Sistema",
          ].map((item) => (

            <TouchableOpacity
              key={item}
              style={[
                styles.filterButton,

                filtroAtivo === item &&
                  styles.filterButtonActive,
              ]}
              onPress={() =>
                setFiltroAtivo(item)
              }
              activeOpacity={0.8}
            >

              <Text
                style={[
                  styles.filterText,

                  filtroAtivo === item &&
                    styles.filterTextActive,
                ]}
              >
                {item}
              </Text>

            </TouchableOpacity>

          ))}

        </ScrollView>

      </View>

      {/* LISTA */}
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >

        {/* TITULO */}
        <Text style={styles.sectionTitle}>
          Hoje
        </Text>

        {/* CARDS */}
        {notificacoesFiltradas.map((item) => (

          <TouchableOpacity
            key={item.id}
            style={styles.card}
            activeOpacity={0.8}
          >

            {/* ÍCONE */}
            <View
              style={[
                styles.iconContainer,
                {
                  backgroundColor: item.cor,
                },
              ]}
            >

              <Ionicons
                name={item.icon}
                size={24}
                color="#fff"
              />

            </View>

            {/* CONTEÚDO */}
            <View style={styles.content}>

              <View style={styles.topRow}>

                <Text style={styles.title}>
                  {item.titulo}
                </Text>

                <Text style={styles.time}>
                  {item.tempo}
                </Text>

              </View>

              <Text style={styles.description}>
                {item.descricao}
              </Text>

              {item.novo && (

                <View style={styles.newBadge}>

                  <Text style={styles.newText}>
                    NOVO
                  </Text>

                </View>

              )}

            </View>

          </TouchableOpacity>

        ))}

      </ScrollView>

    </View>
  );
}

const styles = StyleSheet.create({

  /* CONTAINER */

  container: {
    flex: 1,
    backgroundColor: "#f5f7fb",
  },

  scrollContent: {
    paddingBottom: 120,
  },

  /* FILTROS */

  filterWrapper: {
    maxHeight: 60,
  },

  filterContainer: {
    paddingHorizontal: 18,
  },

  filterButton: {
    backgroundColor: "#eceff5",

    paddingHorizontal: 18,

    height: 42,

    borderRadius: 14,

    marginRight: 10,

    justifyContent: "center",
    alignItems: "center",
  },

  filterButtonActive: {
    backgroundColor: "#2155f3",
  },

  filterText: {
    color: "#555",
    fontWeight: "600",
    fontSize: 14,
  },

  filterTextActive: {
    color: "#fff",
  },

  /* TITULO */

  sectionTitle: {
    fontSize: 22,
    fontWeight: "bold",

    color: "#111",

    marginBottom: 15,
    marginTop: 15,

    paddingHorizontal: 18,
  },

  /* CARD */

  card: {
    backgroundColor: "#fff",

    marginHorizontal: 18,
    marginBottom: 14,

    borderRadius: 24,

    padding: 16,

    flexDirection: "row",

    elevation: 3,
  },

  /* ICON */

  iconContainer: {
    width: 58,
    height: 58,

    borderRadius: 29,

    justifyContent: "center",
    alignItems: "center",

    marginRight: 15,
  },

  /* CONTENT */

  content: {
    flex: 1,
  },

  topRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  title: {
    fontSize: 16,
    fontWeight: "bold",

    color: "#111",

    flex: 1,
    marginRight: 10,
  },

  time: {
    color: "#888",
    fontSize: 12,
  },

  description: {
    color: "#666",
    marginTop: 5,
    fontSize: 14,
  },

  /* BADGE */

  newBadge: {
    marginTop: 10,

    alignSelf: "flex-start",

    backgroundColor: "#2155f3",

    paddingHorizontal: 12,
    paddingVertical: 5,

    borderRadius: 10,
  },

  newText: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 11,
  },

});