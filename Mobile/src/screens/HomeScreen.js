import React, { useState, useEffect, useRef } from "react";
import Header from "../components/Header";
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
import { COLORS } from "../components/Cores";
import { MaterialCommunityIcons, Feather, Ionicons } from "@expo/vector-icons";

export default function HomeScreen({ navigation }) {
  const primaryColor = COLORS.primary;
  const alertColor = COLORS.alert;

  // CORRIGIDO: O estado quantidadeNotif foi movido para DENTRO do componente
  const [quantidadeNotif, setQuantidadeNotif] = useState(3);
  const [busca, setBusca] = useState("");
  
  // Quantidade de mensagens no fórum ativo
  const [totalMensagensForum, setTotalMensagensForum] = useState(3);

  // ESTADO PARA ARMAZENAR OS REPOSITÓRIOS REALMENTE ACESSADOS
  const [recentesAcessados, setRecentesAcessados] = useState([]);

  // CONFIGURAÇÃO DA ANIMAÇÃO DE PULSAR
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.15,
          duration: 800,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 800,
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, [pulseAnim]);

  // DADOS DOS EVENTOS
  const events = [
    { id: 1, title: 'Reunião de Pais', date: '2026-04-01', day: '01', month: 'ABR', time: '08:30', local: 'Sala 05', description: 'Alinhamento semestral com os responsáveis sobre o desempenho dos alunos.' },
    { id: 2, title: 'Palestra: Inovação', date: '2026-04-10', day: '10', month: 'ABR', time: '19:00', local: 'Auditório Central', description: 'Uma palestra incrível sobre as novas tecnologias no setor educacional.' },
    { id: 3, title: 'Entrega de Notas', date: '2026-03-25', day: '25', month: 'MAR', time: '14:00', local: 'Online', description: 'Publicação oficial das notas no portal do aluno.' },
  ];

  const categoriasCursos = [
    {
      id: "1",
      nomeCurso: "Informática Básica",
      turma: "Turma A",
      projetos: [
        { id: "p1", titulo: "Sistema de Gestão", imagem: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=400" },
        { id: "p2", titulo: "Planilha de Controle", imagem: "https://images.unsplash.com/photo-1627398242454-45a1465c2020?q=80&w=400" },
      ],
    },
    {
      id: "2",
      nomeCurso: "Excel Avançado",
      turma: "Turma B",
      projetos: [
        { id: "p3", titulo: "Dashboard Automatizado", imagem: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=400" },
        { id: "p4", titulo: "Análise de Dados Macro", imagem: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=400" },
      ],
    },
    {
      id: "3",
      nomeCurso: "Desenvolvimento Web Full Stack",
      turma: "Turma C",
      projetos: [
        { id: "p5", titulo: "My App - RN", imagem: "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?q=80&w=400" },
        { id: "p6", titulo: "Web Portal E-commerce", imagem: "https://images.unsplash.com/photo-161474111887-7a4ee193a5fa?q=80&w=400" },
        { id: "p7", titulo: "API Restful Node", imagem: "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?q=80&w=400" },
      ],
    },
  ];

  const getEventStatusColor = (eventDate) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const evDate = new Date(eventDate);
    evDate.setHours(0, 0, 0, 0);

    if (evDate.getTime() === today.getTime()) return '#FFD700';
    return evDate > today ? '#4CAF50' : '#F44336';
  };

  const irParaRepositorio = (projeto) => {
    setRecentesAcessados((listaAntiga) => {
      const listaFiltrada = listaAntiga.filter((item) => item.id !== projeto.id);
      return [projeto, ...listaFiltrada];
    });
    navigation.navigate("Repositorio", { projetoId: projeto.id });
  };

  const removerDosRecentes = (id) => {
    setRecentesAcessados((listaAntiga) => listaAntiga.filter((item) => item.id !== id));
  };

  const filtrarResultados = () => {
    if (!busca) return [];
    let resultados = [];
    const termo = busca.toLowerCase();

    categoriasCursos.forEach(curso => {
      const combinaCursoOuTurma = 
        curso.nomeCurso.toLowerCase().includes(termo) || 
        curso.turma.toLowerCase().includes(termo);

      if (combinaCursoOuTurma) {
        resultados.push(...curso.projetos.map(p => ({ ...p, origem: curso.nomeCurso })));
      } else {
        const projetosMatch = curso.projetos.filter(p => 
          p.titulo.toLowerCase().includes(termo)
        );
        resultados.push(...projetosMatch.map(p => ({ ...p, origem: "Repositório" })));
      }
    });

    return Array.from(new Set(resultados.map(a => a.id))).map(id => resultados.find(a => a.id === id));
  };

  const resultadosDaBusca = filtrarResultados();

  return (
    <View style={styles.safe}>
      {/* CORRIGIDO: Passando a quantidade de notificações e a função para zerar */}
      <Header 
        nomeTela="Olá, Alcides 👋" 
        exibirPerfil={true} 
        quantidadeNotificacoes={quantidadeNotif}
        aoClicarNoSino={() => setQuantidadeNotif(0)}
      />

      <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        
        {/* 1. PRÓXIMOS EVENTOS */}
        <Text style={styles.sectionTitle}>Próximos eventos</Text>
        {events.map((event) => {
          const statusColor = getEventStatusColor(event.date);
          return (
            <TouchableOpacity 
              key={event.id} 
              style={styles.eventCard} 
              activeOpacity={0.8}
              onPress={() => navigation.navigate("Eventos", { selectedDate: event.date })}
            >
              <View style={[styles.dateBadge, { borderColor: statusColor }]}>
                <View style={[styles.dateBadgeTop, { backgroundColor: statusColor }]}><Text style={styles.monthText}>{event.month}</Text></View>
                <View style={styles.dateBadgeBottom}><Text style={[styles.dayText, { color: '#333' }]}>{event.day}</Text></View>
              </View>
              <View style={styles.eventInfo}>
                <Text style={styles.eventTitle}>{event.title}</Text>
                <Text style={styles.eventTimeInfo}>
                  <Ionicons name="time-outline" size={13} color="#777" /> {event.time} • {event.local}
                </Text>
              </View>
              <View style={[styles.statusDot, { backgroundColor: statusColor }]} />
            </TouchableOpacity>
          );
        })}

        {/* 2. MEUS REPOSITÓRIOS COM BUSCADOR */}
        <View style={styles.searchContainer}>
          <Text style={styles.searchTitle}>Meus Repositórios</Text>
          <View style={styles.searchBox}>
            <Feather name="search" size={18} color="#888" style={{ marginRight: 10 }} />
            <TextInput
              placeholder="Buscar por curso, turma ou repositório..."
              placeholderTextColor="#888"
              style={styles.searchInput}
              value={busca}
              onChangeText={setBusca}
            />
            {busca !== "" && (
              <TouchableOpacity onPress={() => setBusca("")}>
                <Ionicons name="close-circle" size={18} color="#999" />
              </TouchableOpacity>
            )}
          </View>

          {busca !== "" && (
            <View style={{ marginTop: 15 }}>
              <Text style={{ fontSize: 12, color: '#888', marginBottom: 5 }}>{resultadosDaBusca.length} encontrados:</Text>
              <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 12 }}>
                {resultadosDaBusca.length > 0 ? (
                  resultadosDaBusca.map((item) => (
                    <TouchableOpacity 
                      key={item.id} 
                      style={styles.miniResultCard}
                      onPress={() => irParaRepositorio(item)}
                    >
                      <Image source={{ uri: item.imagem }} style={styles.miniResultImg} />
                      <Text numberOfLines={1} style={styles.miniResultText}>{item.titulo}</Text>
                      <View style={styles.miniBadge}><Text style={styles.miniBadgeText}>{item.origem}</Text></View>
                    </TouchableOpacity>
                  ))
                ) : (
                  <Text style={{ color: '#999', fontSize: 13, fontStyle: 'italic' }}>Nenhum resultado para "{busca}"</Text>
                )}
              </ScrollView>
            </View>
          )}
        </View>

        {/* 3. FÓRUM ATIVO */}
        <Text style={styles.sectionTitle}>Fórum ativo</Text>
        <TouchableOpacity style={styles.forumContainerCard} activeOpacity={0.8} onPress={() => navigation.navigate("Fórum")}>
          <View style={styles.forumHeaderRow}>
            <View style={styles.forumIconCircle}><MaterialCommunityIcons name="comment-text-multiple" size={20} color="#fff" /></View>
            <View style={styles.forumTitleBlock}>
              <Text style={styles.forumMainTitle}>Meu primeiro tópico</Text>
              <Text style={styles.forumTimeAgo}>há 2 min</Text>
            </View>
            <Animated.View style={[
              styles.forumBadgeCount, 
              { backgroundColor: primaryColor, transform: [{ scale: pulseAnim }] }
            ]}>
              <Text style={styles.forumBadgeText}>{totalMensagensForum}</Text>
            </Animated.View>
          </View>
          <Text style={styles.forumPublishDate}>Publicado em 10/05/2024</Text>
          <Text style={styles.forumBodyText} numberOfLines={2}>Estou tendo dificuldade para entender o useEffect no React Native...</Text>
        </TouchableOpacity>

        {/* 4. REPOSITÓRIOS RECENTES */}
        <Text style={styles.sectionTitle}>Repositórios Recentes</Text>
        {recentesAcessados.length > 0 ? (
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.horizontalRepoContainer}>
            {recentesAcessados.map((projeto) => (
              <TouchableOpacity 
                key={projeto.id}
                style={styles.repoSquareCard} 
                activeOpacity={0.8}
                onPress={() => irParaRepositorio(projeto)} 
              >
                <View style={styles.imageWrapper}>
                  <Image source={{ uri: project.imagem || projeto.imagem }} style={styles.repoCoverImage} />
                  <TouchableOpacity 
                    style={styles.removeButton} 
                    activeOpacity={0.7}
                    onPress={() => removerDosRecentes(projeto.id)}
                  >
                    <Ionicons name="close" size={14} color="#FFF" />
                  </TouchableOpacity>
                </View>
                <View style={styles.repoContentArea}>
                  <Text style={styles.repoMainTitle} numberOfLines={2}>{projeto.titulo}</Text>
                </View>
              </TouchableOpacity>
            ))}
          </ScrollView>
        ) : (
          <View style={styles.emptyRecentsBox}>
            <MaterialCommunityIcons name="folder-clock-outline" size={24} color="#aaa" />
            <Text style={styles.emptyRecentsText}>Os repositórios que você visitar aparecerão aqui.</Text>
          </View>
        )}
      </ScrollView>
    </View>
  );
}

// ... Mantive os mesmos estilos abaixo
const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#1459b3" },
  container: { flex: 1, backgroundColor: '#FFFFFF', },
  scrollContent: { paddingHorizontal: 18, paddingBottom: 40, paddingTop: 5 },
  sectionTitle: { fontSize: 20, fontWeight: "bold", marginBottom: 15, color: "#111" },
  eventCard: { backgroundColor: "#fff", borderRadius: 18, padding: 14, marginBottom: 12, flexDirection: "row", alignItems: "center", elevation: 3 },
  dateBadge: { width: 52, height: 56, borderRadius: 10, borderWidth: 1, overflow: "hidden", alignItems: "center" },
  dateBadgeTop: { width: "100%", height: 20, justifyContent: "center", alignItems: "center" },
  monthText: { color: "#fff", fontSize: 10, fontWeight: "bold" },
  dateBadgeBottom: { flex: 1, width: "100%", backgroundColor: "#fff", justifyContent: "center", alignItems: "center" },
  dayText: { fontSize: 18, fontWeight: "bold" },
  eventInfo: { flex: 1, paddingHorizontal: 14 },
  eventTitle: { fontSize: 16, fontWeight: "bold", color: "#111", marginBottom: 4 },
  eventTimeInfo: { fontSize: 13, color: "#666" },
  statusDot: { width: 8, height: 8, borderRadius: 4, marginRight: 6 },
  searchContainer: { backgroundColor: "#fff", borderRadius: 24, padding: 18, marginTop: 10, marginBottom: 25, elevation: 4 },
  searchTitle: { fontWeight: "bold", fontSize: 22, marginBottom: 15, color: "#111" },
  searchBox: { flexDirection: 'row', alignItems: 'center', backgroundColor: "#f1f1f1", borderRadius: 18, paddingHorizontal: 15 },
  searchInput: { height: 50, fontSize: 15, color: "#111", flex: 1 },
  miniResultCard: { width: 115, alignItems: 'center', backgroundColor: '#fdfdfd', padding: 8, borderRadius: 14, borderWidth: 1, borderColor: '#eee' },
  miniResultImg: { width: 98, height: 62, borderRadius: 8, resizeMode: 'cover' },
  miniResultText: { fontSize: 11, fontWeight: 'bold', color: '#222', marginTop: 5, textAlign: 'center' },
  miniBadge: { backgroundColor: '#5360f0', paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4, marginTop: 4 },
  miniBadgeText: { color: '#fff', fontSize: 8, fontWeight: 'bold' },
  forumContainerCard: { backgroundColor: '#FFFFFF', borderRadius: 20, padding: 16, marginBottom: 25, elevation: 3 },
  forumHeaderRow: { flexDirection: "row", alignItems: "center" },
  forumIconCircle: { width: 44, height: 44, borderRadius: 22, backgroundColor: "#5360f0", justifyContent: "center", alignItems: "center", marginRight: 12 },
  forumTitleBlock: { flex: 1 },
  forumMainTitle: { fontSize: 16, fontWeight: "bold", color: "#111" },
  forumTimeAgo: { fontSize: 12, color: "#888", position: "absolute", right: 35, top: 2 },
  forumBadgeCount: { width: 22, height: 22, borderRadius: 11, justifyContent: "center", alignItems: "center" },
  forumBadgeText: { color: "#fff", fontSize: 12, fontWeight: "bold" },
  forumPublishDate: { fontSize: 13, color: "#999", marginLeft: 56, marginTop: -4, marginBottom: 10 },
  forumBodyText: { fontSize: 14, color: "#555", marginLeft: 56, marginBottom: 15, lineHeight: 20 },
  horizontalRepoContainer: { paddingBottom: 15, flexDirection: "row", gap: 14 },
  repoSquareCard: { backgroundColor: "#fff", borderRadius: 20, overflow: "hidden", elevation: 3, width: 140, position: 'relative' },
  imageWrapper: { width: "100%", height: 100, backgroundColor: "#ececec", position: 'relative' },
  repoCoverImage: { width: "100%", height: "100%", resizeMode: "cover" },
  repoContentArea: { padding: 12, justifyContent: "center", minHeight: 45 },
  repoMainTitle: { fontSize: 14, fontWeight: "bold", color: "#111", textAlign: "center" },
  removeButton: { position: 'absolute', top: 6, right: 6, backgroundColor: 'rgba(0, 0, 0, 0.6)', width: 22, height: 22, borderRadius: 11, justifyContent: 'center', alignItems: 'center', zIndex: 10 },
  emptyRecentsBox: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#f5f5f5', padding: 15, borderRadius: 16, gap: 10, justifyContent: 'center' },
  emptyRecentsText: { color: '#888', fontSize: 12, fontWeight: '500' }
});