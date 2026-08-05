import React, { useCallback, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from "react-native";
import { Feather } from "@expo/vector-icons";
import { useNavigation, useFocusEffect } from "@react-navigation/native";
import { useNotifications } from "../context/NotificationContext";

import Header from "../components/Header";

export default function NotificationsScreen() {
  const navigation = useNavigation();
  const [filtroAtivo, setFiltroAtivo] = useState("Todas");
  const { notifications, totalNovas, markAsRead, loadNotifications } = useNotifications();

  useFocusEffect(
    useCallback(() => {
      loadNotifications();
    }, [loadNotifications])
  );

  const filtros = ["Todas", "Forum", "Eventos", "Sistema"];

  const notificacoesFiltradas = notifications.filter((notif) => {
    if (filtroAtivo === "Todas") return true;
    return notif.tipo === filtroAtivo;
  });

  const lidarComCliqueNotificacao = async (item) => {
    await markAsRead(item.id);

    if (item.telaDestino) {
      try {
        navigation.navigate(item.telaDestino, item.parametros || {});
      } catch (error) {
        console.warn(`Erro ao navegar para a tela ${item.telaDestino}:`, error);
      }
    }
  };

  return (
    <View style={styles.container}>
      <Header
        nomeTela="Notificações"
        temGoBack={true}
        exibirCurva={false}
        quantidadeNotificacoes={totalNovas}
      />

      <View style={styles.filterWrapper}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.filterContainer}>
          {filtros.map((filtro) => (
            <TouchableOpacity
              key={filtro}
              style={[
                styles.filterButton,
                filtroAtivo === filtro && styles.filterButtonActive,
              ]}
              onPress={() => setFiltroAtivo(filtro)}
              activeOpacity={0.7}
            >
              <Text
                style={[
                  styles.filterText,
                  filtroAtivo === filtro && styles.filterTextActive,
                ]}
              >
                {filtro}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      <ScrollView contentContainerStyle={styles.scrollList} showsVerticalScrollIndicator={false}>
        <Text style={styles.sectionTitle}>Hoje</Text>

        {notificacoesFiltradas.length > 0 ? (
          notificacoesFiltradas.map((item) => (
            <TouchableOpacity
              key={item.id}
              style={styles.card}
              onPress={() => lidarComCliqueNotificacao(item)}
              activeOpacity={0.8}
            >
              <View style={[styles.iconContainer, { backgroundColor: item.iconColor || "#4d5dfb" }]}>
                <Feather name={item.icon || "bell"} size={22} color="#fff" />
              </View>

              <View style={styles.contentContainer}>
                <View style={styles.cardHeader}>
                  <Text style={styles.cardTitle} numberOfLines={1}>{item.titulo}</Text>
                  <Text style={styles.cardTime}>{item.createdAt ? new Date(item.createdAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : ""}</Text>
                </View>
                <Text style={styles.cardSubtitle} numberOfLines={2}>{item.subtitulo}</Text>

                {item.isNova && (
                  <View style={styles.newBadge}>
                    <Text style={styles.newBadgeText}>NOVO</Text>
                  </View>
                )}
              </View>
            </TouchableOpacity>
          ))
        ) : (
          <View style={styles.emptyContainer}>
            <Feather name="bell-off" size={40} color="#bbb" />
            <Text style={styles.emptyText}>Nenhuma notificação por aqui.</Text>
          </View>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f8f9fa" },
  filterWrapper: { backgroundColor: "#1459b3", paddingBottom: 15 },
  filterContainer: { paddingHorizontal: 22, gap: 10 },
  filterButton: { backgroundColor: "#ececec", paddingVertical: 10, paddingHorizontal: 20, borderRadius: 16 },
  filterButtonActive: { backgroundColor: "#2b66ff" },
  filterText: { color: "#666", fontSize: 14, fontWeight: "600" },
  filterTextActive: { color: "#fff" },
  scrollList: { paddingHorizontal: 22, paddingTop: 20, paddingBottom: 40 },
  sectionTitle: { fontSize: 22, fontWeight: "bold", color: "#111", marginBottom: 15 },
  card: { backgroundColor: "#fff", borderRadius: 20, padding: 16, flexDirection: "row", alignItems: "center", marginBottom: 14, shadowColor: "#000", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.05, shadowRadius: 8, elevation: 2 },
  iconContainer: { width: 50, height: 50, borderRadius: 25, justifyContent: "center", alignItems: "center", marginRight: 14 },
  contentContainer: { flex: 1 },
  cardHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  cardTitle: { fontSize: 15, fontWeight: "bold", color: "#222", flex: 1, marginRight: 5 },
  cardTime: { fontSize: 12, color: "#888" },
  cardSubtitle: { fontSize: 13, color: "#666", marginTop: 2 },
  newBadge: { backgroundColor: "#2b66ff", alignSelf: "flex-start", paddingHorizontal: 10, paddingVertical: 4, borderRadius: 6, marginTop: 8 },
  newBadgeText: { color: "#fff", fontSize: 10, fontWeight: "bold" },
  emptyContainer: { alignItems: "center", justifyContent: "center", marginTop: 60, gap: 10 },
  emptyText: { textAlign: "center", color: "#999", fontSize: 15, fontWeight: "500" },
});