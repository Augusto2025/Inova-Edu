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

import { MaterialCommunityIcons, Feather, Ionicons } from "@expo/vector-icons";

export default function HomeScreen({ navigation }) {
  const primaryColor = "#2155f3";
  const alertColor = "#ff4d67";

  // INTEGRADO: Seus cursos reais vindos da tela de Cursos com projetos vinculados!
  const categoriasCursos = [
    {
      id: "1",
      nomeCurso: "Informática Básica", // Seu curso 1
      projetos: [
        {
          id: "p1",
          titulo: "Sistema de Gestão",
          imagem: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=400",
        },
        {
          id: "p2",
          titulo: "Planilha de Controle",
          imagem: "https://images.unsplash.com/photo-1627398242454-45a1465c2020?q=80&w=400",
        },
      ],
    },
    {
      id: "2",
      nomeCurso: "Excel Avançado", // Seu curso 2
      projetos: [
        {
          id: "p3",
          titulo: "Dashboard Automatizado",
          imagem: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=400",
        },
        {
          id: "p4",
          titulo: "Análise de Dados Macro",
          imagem: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=400",
        },
      ],
    },
    {
      id: "3",
      nomeCurso: "Desenvolvimento Web Full Stack", // Seu curso 3
      projetos: [
        {
          id: "p5",
          titulo: "My App - RN",
          imagem: "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?q=80&w=400",
        },
        {
          id: "p6",
          titulo: "Web Portal E-commerce",
          imagem: "https://images.unsplash.com/photo-161474111887-7a4ee193a5fa?q=80&w=400",
        },
        {
          id: "p7",
          titulo: "API Restful Node",
          imagem: "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?q=80&w=400",
        },
      ],
    },
  ];

  return (
    <View style={styles.safe}>
      {/* HEADER (Com a curva ativa integrada por padrão) */}
      <Header nomeTela="Olá, Alcides 👋" exibirPerfil={true} />

      {/* CONTEÚDO */}
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* 1. PRÓXIMOS EVENTOS */}
        <Text style={styles.sectionTitle}>Próximos eventos</Text>

        <TouchableOpacity style={styles.eventCard} activeOpacity={0.8}>
          <View style={[styles.dateBadge, { borderColor: primaryColor }]}>
            <View style={[styles.dateBadgeTop, { backgroundColor: primaryColor }]}>
              <Text style={styles.monthText}>MAI</Text>
            </View>
            <View style={styles.dateBadgeBottom}>
              <Text style={[styles.dayText, { color: '#333' }]}>24</Text>
            </View>
          </View>
          <View style={styles.eventInfo}>
            <Text style={styles.eventTitle}>Semana Tech</Text>
            <Text style={styles.eventTimeInfo}>
              <Ionicons name="time-outline" size={13} color="#777" /> 10:00 • Auditório Central
            </Text>
          </View>
          <View style={[styles.statusDot, { backgroundColor: primaryColor }]} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.eventCard} activeOpacity={0.8}>
          <View style={[styles.dateBadge, { borderColor: alertColor }]}>
            <View style={[styles.dateBadgeTop, { backgroundColor: alertColor }]}>
              <Text style={styles.monthText}>MAI</Text>
            </View>
            <View style={styles.dateBadgeBottom}>
              <Text style={[styles.dayText, { color: '#333' }]}>25</Text>
            </View>
          </View>
          <View style={styles.eventInfo}>
            <Text style={styles.eventTitle}>React Native Meetup</Text>
            <Text style={styles.eventTimeInfo}>
              <Ionicons name="time-outline" size={13} color="#777" /> 19:00 • Lab 04
            </Text>
          </View>
          <View style={[styles.statusDot, { backgroundColor: alertColor }]} />
        </TouchableOpacity>

        {/* 2. SEUS REPOSITÓRIOS (BUSCA + TAGS) */}
        <View style={styles.searchContainer}>
          <Text style={styles.searchTitle}>Seus Repositórios</Text>
          <View style={styles.searchBox}>
            <TextInput
              placeholder="Buscar repositórios..."
              placeholderTextColor="#888"
              style={styles.searchInput}
            />
          </View>
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={styles.tagsContainer}
          >
            <TouchableOpacity style={styles.tag} activeOpacity={0.8}>
              <Text style={styles.tagText}>React Native</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.tag} activeOpacity={0.8}>
              <Text style={styles.tagText}>Python</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.tag} activeOpacity={0.8}>
              <Text style={styles.tagText}>JavaScript</Text>
            </TouchableOpacity>
          </ScrollView>
        </View>

        {/* 3. FÓRUM ATIVO */}
        <Text style={styles.sectionTitle}>Fórum ativo</Text>
        <View style={styles.forumContainerCard}>
          <View style={styles.forumHeaderRow}>
            <View style={styles.forumIconCircle}>
              <MaterialCommunityIcons name="comment-text-multiple" size={20} color="#fff" />
            </View>
            <View style={styles.forumTitleBlock}>
              <Text style={styles.forumMainTitle}>Meu primeiro tópico</Text>
              <Text style={styles.forumTimeAgo}>há 2 min</Text>
            </View>
            <View style={styles.forumBadgeCount}>
              <Text style={styles.forumBadgeText}>3</Text>
            </View>
          </View>
          <Text style={styles.forumPublishDate}>Publicado em 10/05/2024</Text>
          <Text style={styles.forumBodyText} numberOfLines={2}>
            Estou tendo dificuldade para entender o useEffect no React Native...
          </Text>
          <View style={styles.forumFooterRow}>
            <View style={styles.forumMetaDetails}>
              <View style={styles.forumMetaItem}>
                <Feather name="message-square" size={14} color="#777" style={{ marginRight: 4 }} />
                <Text style={styles.forumMetaText}>12 mensagens</Text>
              </View>
              <View style={styles.forumMetaItem}>
                <Feather name="tag" size={14} color="#777" style={{ marginRight: 4 }} />
                <Text style={styles.forumMetaText}>React Native</Text>
              </View>
            </View>
            <View style={styles.forumActions}>
              <TouchableOpacity style={styles.actionButtonEdit}>
                <Feather name="edit-2" size={14} color="#5360f0" />
              </TouchableOpacity>
              <TouchableOpacity style={styles.actionButtonDelete}>
                <Feather name="trash-2" size={14} color="#ff4d67" />
              </TouchableOpacity>
            </View>
          </View>
        </View>

        {/* 4. REPOSITÓRIOS RECENTES DINÂMICOS COM SEUS CURSOS */}
        <Text style={styles.sectionTitle}>Repositórios Recentes</Text>
        
        {categoriasCursos.map((curso) => (
          <View key={curso.id} style={styles.cursoSectionContainer}>
            {/* Tema do Curso Real */}
            <Text style={styles.sectioncategoria}>{curso.nomeCurso}</Text>
            
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={styles.horizontalRepoContainer}
            >
              {curso.projetos.map((projeto) => (
                <TouchableOpacity 
                  key={projeto.id}
                  style={styles.repoSquareCard} 
                  activeOpacity={0.7}
                  onPress={() => navigation.navigate("Repositorio", { projetoId: projeto.id })} 
                >
                  <View style={styles.imageWrapper}>
                    <Image
                      source={{ uri: projeto.imagem }}
                      style={styles.repoCoverImage}
                    />
                  </View>
                  <View style={styles.repoContentArea}>
                    <Text style={styles.repoMainTitle} numberOfLines={2}>
                      {projeto.titulo}
                    </Text>
                  </View>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        ))}

      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#1459b3" },
  container: { flex: 1, backgroundColor: "#f5f7fb" },
  scrollContent: { paddingHorizontal: 18, paddingBottom: 40, paddingTop: 15 },
  sectionTitle: { fontSize: 20, fontWeight: "bold", marginBottom: 15, color: "#111" },
  eventCard: { backgroundColor: "#fff", borderRadius: 18, padding: 14, marginBottom: 12, flexDirection: "row", alignItems: "center", elevation: 3, shadowColor: "#000", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.06, shadowRadius: 4 },
  dateBadge: { width: 52, height: 56, borderRadius: 10, borderWidth: 1, overflow: "hidden", alignItems: "center" },
  dateBadgeTop: { width: "100%", height: 20, justifyContent: "center", alignItems: "center" },
  monthText: { color: "#fff", fontSize: 10, fontWeight: "bold" },
  dateBadgeBottom: { flex: 1, width: "100%", backgroundColor: "#fff", justifyContent: "center", alignItems: "center" },
  dayText: { fontSize: 18, fontWeight: "bold" },
  eventInfo: { flex: 1, paddingHorizontal: 14 },
  eventTitle: { fontSize: 16, fontWeight: "bold", color: "#111", marginBottom: 4 },
  eventTimeInfo: { fontSize: 13, color: "#666", flexDirection: "row", alignItems: "center" },
  statusDot: { width: 8, height: 8, borderRadius: 4, marginRight: 6 },
  
  cursoSectionContainer: { marginBottom: 10 },
  sectioncategoria: { fontSize: 16, fontWeight: "600", color: "#444", marginBottom: 10 },
  horizontalRepoContainer: { paddingBottom: 15, flexDirection: "row", gap: 14 },
  repoSquareCard: { backgroundColor: "#fff", borderRadius: 20, overflow: "hidden", elevation: 3, shadowColor: "#000", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.08, shadowRadius: 4, width: 140 },
  imageWrapper: { width: "100%", height: 100, backgroundColor: "#ececec" },
  repoCoverImage: { width: "100%", height: "100%", resizeMode: "cover" },
  repoContentArea: { padding: 12, justifyContent: "center", minHeight: 45 },
  repoMainTitle: { fontSize: 14, fontWeight: "bold", color: "#111", textAlign: "center" },
  
  searchContainer: { backgroundColor: "#fff", borderRadius: 24, padding: 18, marginTop: 10, marginBottom: 25, elevation: 4, shadowColor: "#000", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.08, shadowRadius: 4 },
  searchTitle: { fontWeight: "bold", fontSize: 22, marginBottom: 15, color: "#111" },
  searchBox: { backgroundColor: "#f1f1f1", borderRadius: 18, paddingHorizontal: 15 },
  searchInput: { height: 50, fontSize: 15, color: "#111" },
  tagsContainer: { paddingTop: 15 },
  tag: { backgroundColor: "#ececec", paddingHorizontal: 16, paddingVertical: 10, borderRadius: 14, marginRight: 10 },
  tagText: { color: "#333", fontWeight: "500" },
  forumContainerCard: { backgroundColor: "#fff", borderRadius: 20, padding: 16, marginBottom: 25, elevation: 3, shadowColor: "#000", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.08, shadowRadius: 4 },
  forumHeaderRow: { flexDirection: "row", alignItems: "center" },
  forumIconCircle: { width: 44, height: 44, borderRadius: 22, backgroundColor: "#5360f0", justifyContent: "center", alignItems: "center", marginRight: 12 },
  forumTitleBlock: { flex: 1 },
  forumMainTitle: { fontSize: 16, fontWeight: "bold", color: "#111" },
  forumTimeAgo: { fontSize: 12, color: "#888", position: "absolute", right: 35, top: 2 },
  forumBadgeCount: { backgroundColor: "#5360f0", width: 22, height: 22, borderRadius: 11, justifyContent: "center", alignItems: "center" },
  forumBadgeText: { color: "#fff", fontSize: 12, fontWeight: "bold" },
  forumPublishDate: { fontSize: 13, color: "#999", marginLeft: 56, marginTop: -4, marginBottom: 10 },
  forumBodyText: { fontSize: 14, color: "#555", marginLeft: 56, marginBottom: 15, lineHeight: 20 },
  forumFooterRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginLeft: 56 },
  forumMetaDetails: { flexDirection: "row", alignItems: "center", gap: 12 },
  forumMetaItem: { flexDirection: "row", alignItems: "center" },
  forumMetaText: { fontSize: 12, color: "#777" },
  forumActions: { flexDirection: "row", gap: 8 },
  actionButtonEdit: { backgroundColor: "#f0f2ff", padding: 8, borderRadius: 12 },
  actionButtonDelete: { backgroundColor: "#fff0f2", padding: 8, borderRadius: 12 },
});