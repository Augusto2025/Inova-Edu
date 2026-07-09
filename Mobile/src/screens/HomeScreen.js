import React, { useState, useEffect, useRef } from "react";
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  ScrollView,
  TouchableOpacity,
  Image,
  Animated,
} from "react-native";
import Header from "../components/Header";
import Skeleton from "../components/Skeleton";
import { COLORS } from "../components/Cores";
import { MaterialCommunityIcons, Feather, Ionicons } from "@expo/vector-icons";
import api from "../services/api";

export default function HomeScreen({ navigation }) {
  const primaryColor = COLORS.primary;

  const [carregando, setCarregando] = useState(true);
  const [quantidadeNotif, setQuantidadeNotif] = useState(3);
  const [busca, setBusca] = useState("");
  const [homeData, setHomeData] = useState({
    usuario: { nome: "" },
    eventos: [],
    cursos: [],
    forum: []
  });

  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.05, duration: 1000, useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 1000, useNativeDriver: true })
      ])
    ).start();
  }, [pulseAnim]);

  // Função que busca os dados em tempo real
  async function carregarHome() {
    try {
      setCarregando(true);
      const resposta = await api.get("/home");

      if (resposta.data && resposta.data.sucesso) {
        setHomeData({
          usuario: resposta.data.usuario || { nome: "Estudante" },
          eventos: Array.isArray(resposta.data.eventos) ? resposta.data.eventos : [],
          cursos: Array.isArray(resposta.data.cursos) ? resposta.data.cursos : [],
          forum: Array.isArray(resposta.data.forum) ? resposta.data.forum : []
        });
      }
    } catch (error) {
      console.log("Erro ao carregar dados da Home:", error.message);
    } finally {
      setCarregando(false);
    }
  }

  useEffect(() => {
    carregarHome();
  }, []);

  function getEventStatusColor(data) {
    if (!data) return "#4CAF50";
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    const evento = new Date(data);
    evento.setHours(0, 0, 0, 0);
    if (evento.getTime() === hoje.getTime()) return "#FFD700";
    return evento > hoje ? "#4CAF50" : "#F44336";
  }

  // Filtro puramente local (não toca no banco de dados)
  function filtrarCursos() {
    if (busca.trim() === "") return [];
    const termo = busca.toLowerCase().trim();
    return homeData.cursos.filter((curso) => 
      (curso.nome_curso || "").toLowerCase().includes(termo)
    );
  }

  const resultadosBusca = filtrarCursos();
  const estaBuscando = busca.trim() !== "";
  const forumPrincipal = homeData.forum.length > 0 ? homeData.forum[0] : null;

  return (
    <View style={styles.safe}>
      <Header
        nomeTela={carregando ? "Carregando..." : `Olá, ${homeData.usuario?.nome || "Estudante"} 👋`}
        exibirPerfil={true}
        quantidadeNotificacoes={quantidadeNotif}
        aoClicarNoSino={() => setQuantidadeNotif(0)}
        carregando={carregando}
      />

      <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        
        {/* SEÇÃO: EVENTOS */}
        <Text style={styles.sectionTitle}>Próximos eventos</Text>

        {carregando ? (
          [1, 2].map((item) => (
            <View key={item} style={[styles.eventCard, { gap: 14 }]}>
              <Skeleton width={52} height={56} borderRadius={10} />
              <View style={{ flex: 1, gap: 8 }}>
                <Skeleton width="70%" height={16} borderRadius={4} />
                <Skeleton width="40%" height={12} borderRadius={4} />
              </View>
            </View>
          ))
        ) : homeData.eventos.length > 0 ? (
          homeData.eventos.map((event) => {
            const meses = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"];
            let dia = "•";
            let mes = "EVT";

            if (event.date) {
              const dataObj = new Date(event.date);
              dia = dataObj.getUTCDate();
              mes = meses[dataObj.getUTCMonth()];
            }

            const statusColor = getEventStatusColor(event.date);

            return (
              <TouchableOpacity
                key={event.id}
                style={styles.eventCard}
                activeOpacity={0.8}
                onPress={() => navigation.navigate("Eventos", { selectedDate: event.date })}
              >
                <View style={[styles.dateBadge, { borderColor: statusColor }]}>
                  <View style={[styles.dateBadgeTop, { backgroundColor: statusColor }]}>
                    <Text style={styles.monthText}>{mes}</Text>
                  </View>
                  <View style={styles.dateBadgeBottom}>
                    <Text style={styles.dayText}>{dia}</Text>
                  </View>
                </View>

                <View style={styles.eventInfo}>
                  <Text style={styles.eventTitle} numberOfLines={1}>
                    {event.title || "Sem título"}
                  </Text>
                  <Text style={styles.eventTimeInfo} numberOfLines={1}>
                    <Ionicons name="time-outline" size={13} color="#777" />{" "}
                    {event.time || "Dia todo"}{" • "}{event.local || "InovaEdu"}
                  </Text>
                </View>

                <View style={[styles.statusDot, { backgroundColor: statusColor }]} />
              </TouchableOpacity>
            );
          })
        ) : (
          <Text style={styles.emptyText}>Nenhum evento encontrado.</Text>
        )}

        {/* SEÇÃO: BUSCA DE CURSOS */}
        <View style={styles.searchContainer}>
          <Text style={styles.searchTitle}>Buscar Cursos</Text>
          <View style={styles.searchBox}>
            <Feather name="search" size={18} color="#888" style={{ marginRight: 10 }} />
            <TextInput
              placeholder="Buscar curso..."
              placeholderTextColor="#888"
              style={styles.searchInput}
              value={busca}
              onChangeText={setBusca}
            />
          </View>

          {estaBuscando && (
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginTop: 15 }} contentContainerStyle={{ gap: 12 }}>
              {resultadosBusca.map((curso) => (
                <TouchableOpacity key={curso.idcurso} style={styles.miniResultCard} onPress={() => navigation.navigate("CursoDetalhes", { cursoId: curso.idcurso, cursoNome: curso.nome_curso })}>
                  {curso.imagem ? (
                    <Image source={{ uri: curso.imagem }} style={styles.miniResultImg} />
                  ) : (
                    <View style={[styles.miniResultImg, styles.centerContainer, { backgroundColor: "#eee" }]}>
                      <Feather name="book-open" size={20} color={primaryColor} />
                    </View>
                  )}
                  <Text numberOfLines={1} style={styles.miniResultText}>{curso.nome_curso}</Text>
                </TouchableOpacity>
              ))}
              {resultadosBusca.length === 0 && (
                <Text style={styles.emptyText}>Nenhum curso encontrado.</Text>
              )}
            </ScrollView>
          )}
        </View>

        {/* SEÇÃO: FÓRUM */}
        <Text style={styles.sectionTitle}>Fórum ativo</Text>

        {forumPrincipal ? (
          <TouchableOpacity style={styles.forumContainerCard} activeOpacity={0.8} onPress={() => navigation.navigate("Forum")}>
            <View style={styles.forumHeaderRow}>
              <View style={styles.forumIconCircle}>
                <MaterialCommunityIcons name="comment-text-multiple" size={20} color="#fff" />
              </View>
              <View style={styles.forumTitleBlock}>
                <Text style={styles.forumMainTitle} numberOfLines={1}>{forumPrincipal.titulo}</Text>
                <Text style={styles.forumTimeAgo}>tópico recente</Text>
              </View>
              <Animated.View style={[styles.forumBadgeCount, { backgroundColor: primaryColor, transform: [{ scale: pulseAnim }] }]}>
                <Text style={styles.forumBadgeText}>{forumPrincipal.mensagens || 0}</Text>
              </Animated.View>
            </View>
            <Text style={styles.forumBodyText} numberOfLines={2}>{forumPrincipal.descricao}</Text>
          </TouchableOpacity>
        ) : (
          <Text style={styles.emptyText}>Nenhum fórum ativo.</Text>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#1459b3" },
  container: { flex: 1, backgroundColor: "#fff" },
  scrollContent: { paddingHorizontal: 18, paddingBottom: 30, paddingTop: 5 },
  sectionTitle: { fontSize: 20, fontWeight: "bold", color: "#111", marginTop: 20, marginBottom: 12 },
  centerContainer: { justifyContent: "center", alignItems: "center" },
  eventCard: { backgroundColor: "#fff", borderRadius: 16, padding: 12, marginBottom: 10, flexDirection: "row", alignItems: "center", elevation: 2 },
  dateBadge: { width: 50, height: 54, borderRadius: 8, borderWidth: 1, overflow: "hidden" },
  dateBadgeTop: { height: 18, justifyContent: "center", alignItems: "center" },
  monthText: { color: "#fff", fontSize: 9, fontWeight: "bold" },
  dateBadgeBottom: { flex: 1, justifyContent: "center", alignItems: "center" },
  dayText: { fontSize: 16, fontWeight: "bold" },
  eventInfo: { flex: 1, paddingHorizontal: 12 },
  eventTitle: { fontSize: 15, fontWeight: "bold", color: "#222" },
  eventTimeInfo: { fontSize: 12, color: "#666", marginTop: 2 },
  statusDot: { width: 8, height: 8, borderRadius: 4 },
  searchContainer: { backgroundColor: "#fff", borderRadius: 20, padding: 16, marginTop: 15, elevation: 3 },
  searchTitle: { fontSize: 18, fontWeight: "bold", marginBottom: 12 },
  searchBox: { flexDirection: "row", alignItems: "center", backgroundColor: "#f2f2f2", borderRadius: 14, paddingHorizontal: 12, height: 46 },
  searchInput: { flex: 1, color: "#111" },
  miniResultCard: { width: 110, alignItems: "center", backgroundColor: "#fff", padding: 6, borderRadius: 12, borderWidth: 1, borderColor: "#f0f0f0" },
  miniResultImg: { width: 95, height: 60, borderRadius: 6 },
  miniResultText: { fontSize: 11, marginTop: 4, color: "#333", fontWeight: "600" },
  forumContainerCard: { backgroundColor: "#fff", borderRadius: 16, padding: 14, elevation: 2, marginTop: 5 },
  forumHeaderRow: { flexDirection: "row", alignItems: "center" },
  forumIconCircle: { width: 40, height: 40, borderRadius: 20, backgroundColor: "#5360f0", justifyContent: "center", alignItems: "center", marginRight: 10 },
  forumTitleBlock: { flex: 1 },
  forumMainTitle: { fontWeight: "bold", fontSize: 15, color: "#111" },
  forumTimeAgo: { fontSize: 11, color: "#888" },
  forumBadgeCount: { width: 20, height: 20, borderRadius: 10, justifyContent: "center", alignItems: "center" },
  forumBadgeText: { color: "#fff", fontSize: 11, fontWeight: "bold" },
  forumBodyText: { marginLeft: 50, marginTop: 8, color: "#555", fontSize: 13, lineHeight: 18 },
  emptyText: { textAlign: "center", color: "#999", marginVertical: 10, fontSize: 13 }
});