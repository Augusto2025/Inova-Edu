import React, { useState, useCallback } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from "react-native";
import { Feather } from "@expo/vector-icons";
import { useNavigation, useFocusEffect } from "@react-navigation/native";

// Importando o seu Header customizado
import Header from "../components/Header"; 

export default function NotificationsScreen() {
  const navigation = useNavigation();
  const [filtroAtivo, setFiltroAtivo] = useState("Todas");

  // LISTA DE NOTIFICAÇÕES (O estado inicial define o que aparece ao resetar/iniciar o app)
  const [notificacoes, setNotificacoes] = useState([
    {
      id: "1",
      tipo: "Forum",
      titulo: "Carlos respondeu seu tópico",
      subtitulo: '"Como usar useState?"',
      tempo: "12 min",
      isNova: true, // Começa como Novo ao iniciar o app
      icon: "message-square",
      iconColor: "#4d5dfb",
      telaDestino: "Conversa",
      parametros: { topicoId: "useState-id", titulo: "Como usar useState?" },
    },
    {
      id: "2",
      tipo: "Eventos",
      titulo: "Novo evento disponível",
      subtitulo: "React Native Meetup",
      tempo: "1 hora",
      isNova: true, // Começa como Novo ao iniciar o app
      icon: "calendar",
      iconColor: "#a855f7",
      telaDestino: "Eventos",
      parametros: {},
    },
    {
      id: "3",
      tipo: "Sistema",
      titulo: "Conta verificada",
      subtitulo: "Seu perfil foi atualizado",
      tempo: "2 dias",
      isNova: false, 
      icon: "shield",
      iconColor: "#f59e0b",
      telaDestino: "Profile",
      parametros: {},
    },
  ]);

  // REMOVIDO o reset forçado no useFocusEffect para permitir que a tag suma ao clicar!
  useFocusEffect(
    useCallback(() => {
      // Mantemos o hook aqui caso queira adicionar alguma lógica de foco no futuro,
      // mas ele não vai mais sobrescrever o clique do usuário.
    }, [])
  );

  const filtros = ["Todas", "Forum", "Eventos", "Sistema"];

  // Filtra os itens com base na aba selecionada
  const notificacoesFiltradas = notificacoes.filter((notif) => {
    if (filtroAtivo === "Todas") return true;
    return notif.tipo === filtroAtivo;
  });

  // Conta quantas notificações ainda têm a tag "NOVO" ativa
  const totalNovas = notificacoes.filter((notif) => notif.isNova).length;

  // CORRIGIDO: Agora marca o item específico como lido e remove o "NOVO" antes de navegar
  const lidarComCliqueNotificacao = (item) => {
    // 1. Atualiza o estado para mudar o isNova deste item para false
    setNotificacoes((listaAntiga) =>
      listaAntiga.map((notif) =>
        notif.id === item.id ? { ...notif, isNova: false } : notif
      )
    );

    // 2. Navega para a tela de destino correspondente
    if (item.telaDestino) {
      try {
        navigation.navigate(item.telaDestino, item.parametros);
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
        quantidadeNotificacoes={totalNovas} // Mostra a contagem real baseada nos "NOVOS" restantes
      />

      {/* BOTÕES DE FILTRO */}
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

      {/* CORPO DE NOTIFICAÇÕES */}
      <ScrollView contentContainerStyle={styles.scrollList} showsVerticalScrollIndicator={false}>
        <Text style={styles.sectionTitle}>Hoje</Text>

        {notificacoesFiltradas.length > 0 ? (
          notificacoesFiltradas.map((item) => (
            <TouchableOpacity
              key={item.id}
              style={styles.card}
              onPress={() => lidarComCliqueNotificacao(item)} // Dispara a função corrigida
              activeOpacity={0.8}
            >
              <View style={[styles.iconContainer, { backgroundColor: item.iconColor }]}>
                <Feather name={item.icon} size={22} color="#fff" />
              </View>

              <View style={styles.contentContainer}>
                <View style={styles.cardHeader}>
                  <Text style={styles.cardTitle} numberOfLines={1}>{item.titulo}</Text>
                  <Text style={styles.cardTime}>{item.tempo}</Text>
                </View>
                <Text style={styles.cardSubtitle} numberOfLines={1}>{item.subtitulo}</Text>

                {/* Tag "NOVO" controlada dinamicamente */}
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