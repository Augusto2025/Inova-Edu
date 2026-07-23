import React, { useState, useCallback } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useFocusEffect } from "@react-navigation/native";
import { Ionicons, Feather, MaterialCommunityIcons } from "@expo/vector-icons";
import { COLORS } from "../components/Cores";
import Header from "../components/Header";
import api from "../services/api";
import { useNotifications } from "../context/NotificationContext";

function formatarHora(horaString) {
  if (!horaString) return "";
  // "10:00:00" -> "10:00"
  return horaString.toString().slice(0, 5);
}

function formatarTempoRelativo(dataString) {
  if (!dataString) return "";
  const data = new Date(dataString);
  const agora = new Date();
  const diffMs = agora - data;
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 60) return diffMin <= 1 ? "Agora mesmo" : `Há ${diffMin} min`;
  const diffHoras = Math.floor(diffMin / 60);
  if (diffHoras < 24) return `Há ${diffHoras}h`;
  const diffDias = Math.floor(diffHoras / 24);
  return `Há ${diffDias} dia${diffDias > 1 ? "s" : ""}`;
}

function obterRotuloEvento(dataString) {
  if (!dataString) return "";
  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);
  const dataEvento = new Date(dataString);
  dataEvento.setHours(0, 0, 0, 0);
  const diffDias = Math.round((dataEvento - hoje) / 86400000);

  if (diffDias === 0) return "Hoje";
  if (diffDias === 1) return "Amanhã";
  const meses = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"];
  return `${dataEvento.getUTCDate()} ${meses[dataEvento.getUTCMonth()]}`;
}

export default function HomePainelProfessor({ navigation }) {
  const { totalNovas, markAllAsRead } = useNotifications();
  const [carregando, setCarregando] = useState(true);
  const [painel, setPainel] = useState({
    professor: { nome: "Professor", sobrenome: "" },
    totais: { turmas: 0, alunos: 0, projetos: 0, topicos: 0, eventosHoje: 0 },
    turmas: [],
    eventosProximos: [],
    topicosSemResposta: [],
    ultimosForuns: [],
    ultimosProjetos: [],
  });

  const carregarPainel = useCallback(async () => {
    try {
      setCarregando(true);
      const idSalvo = await AsyncStorage.getItem("idUsuario");
      if (!idSalvo) return;

      const resposta = await api.get("/professor/painel", {
        params: { professorId: idSalvo },
      });

      if (resposta.data?.sucesso) {
        // 🛡️ Mescla com os valores padrão em vez de substituir tudo —
        // assim, se o backend ainda não tiver algum campo novo (ex: backend
        // desatualizado no Render), a tela não quebra, só mostra vazio.
        setPainel((prev) => ({
          professor: resposta.data.professor || prev.professor,
          totais: resposta.data.totais || prev.totais,
          turmas: resposta.data.turmas || [],
          eventosProximos: resposta.data.eventosProximos || [],
          topicosSemResposta: resposta.data.topicosSemResposta || [],
          ultimosForuns: resposta.data.ultimosForuns || [],
          ultimosProjetos: resposta.data.ultimosProjetos || [],
        }));
      }
    } catch (error) {
      console.warn("⚠️ Erro ao carregar painel do professor:", error.message);
    } finally {
      setCarregando(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      carregarPainel();
    }, [carregarPainel])
  );

  const abrirTopico = (topico) => {
    try {
      navigation.navigate("Titulo", {
        topico: { id: topico.id, titulo: topico.titulo, forum: topico.forum_nome },
      });
    } catch (e) {
      console.warn("Erro ao navegar para o tópico:", e.message);
    }
  };

  const abrirTurma = (turma) => {
    try {
      navigation.navigate("Projetos", { turmaId: turma.id, turmaNome: turma.nome });
    } catch (e) {
      console.warn("Erro ao navegar para a turma:", e.message);
    }
  };

  const primeiroTopicoPendente =
    painel.topicosSemResposta.length > 0 ? painel.topicosSemResposta[0] : null;

  if (carregando && painel.turmas.length === 0) {
    return (
      <View style={[styles.safe, styles.center]}>
        <ActivityIndicator size="large" color="#fff" />
      </View>
    );
  }

  return (
    <View style={styles.safe}>
      <Header
        nomeTela={
          carregando
            ? "Carregando..."
            : `Olá, Professor ${painel.professor.nome} 👋`
        }
        exibirPerfil={true}
        subtitulo="Professor"
        quantidadeNotificacoes={totalNovas}
        aoClicarNoSino={markAllAsRead}
        carregando={carregando}
      />

      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.resumoTurmas}>
          {painel.totais.turmas} turmas • {painel.totais.alunos} alunos
        </Text>

        <Text style={styles.sectionTitle}>Painel do Professor</Text>

        {/* CARDS DE TOTAIS */}
        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <View style={[styles.statIconWrap, { backgroundColor: "#DBEAFE" }]}>
              <Ionicons name="people" size={20} color="#2563EB" />
            </View>
            <Text style={styles.statNumber}>{painel.totais.turmas}</Text>
            <Text style={styles.statLabel}>Turmas</Text>
            <Text style={styles.statSubLabel}>{painel.totais.alunos} alunos</Text>
          </View>

          <View style={styles.statCard}>
            <View style={[styles.statIconWrap, { backgroundColor: "#D1FAE5" }]}>
              <Feather name="folder" size={20} color="#059669" />
            </View>
            <Text style={styles.statNumber}>{painel.totais.projetos}</Text>
            <Text style={styles.statLabel}>Projetos</Text>
            <Text style={styles.statSubLabel}>ativos</Text>
          </View>

          <View style={styles.statCard}>
            <View style={[styles.statIconWrap, { backgroundColor: "#EDE9FE" }]}>
              <MaterialCommunityIcons name="comment-text-multiple" size={20} color="#7C3AED" />
            </View>
            <Text style={styles.statNumber}>{painel.totais.topicos}</Text>
            <Text style={styles.statLabel}>Tópicos</Text>
            <Text style={styles.statSubLabel}>no fórum</Text>
          </View>

          <View style={styles.statCard}>
            <View style={[styles.statIconWrap, { backgroundColor: "#FEF3C7" }]}>
              <Ionicons name="calendar" size={20} color="#D97706" />
            </View>
            <Text style={styles.statNumber}>{painel.totais.eventosHoje}</Text>
            <Text style={styles.statLabel}>Eventos</Text>
            <Text style={styles.statSubLabel}>hoje</Text>
          </View>
        </View>

        {/* PENDÊNCIAS — só o que dá pra calcular de verdade hoje: tópicos sem resposta */}
        <View style={styles.sectionHeaderRow}>
          <Text style={styles.sectionTitle}>Pendências</Text>
        </View>

        <View style={styles.card}>
          <TouchableOpacity
            style={styles.pendenciaRow}
            activeOpacity={0.7}
            onPress={() => {
              if (primeiroTopicoPendente) abrirTopico(primeiroTopicoPendente);
            }}
          >
            <View style={[styles.pendenciaIconWrap, { backgroundColor: "#EDE9FE" }]}>
              <MaterialCommunityIcons name="comment-question-outline" size={20} color="#7C3AED" />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.pendenciaTitulo}>Tópicos sem resposta</Text>
              <Text style={styles.pendenciaSub}>
                {painel.topicosSemResposta.length} tópico(s) no fórum precisam de você
              </Text>
            </View>
            <View style={styles.pendenciaBadge}>
              <Text style={styles.pendenciaBadgeText}>{painel.topicosSemResposta.length}</Text>
            </View>
            <Ionicons name="chevron-forward" size={18} color="#999" />
          </TouchableOpacity>
        </View>

        {/* MINHAS TURMAS */}
        <View style={styles.sectionHeaderRow}>
          <Text style={styles.sectionTitle}>Minhas turmas</Text>
          <TouchableOpacity onPress={() => {
            try { navigation.navigate("Turmas"); } catch (e) {}
          }}>
            <Text style={styles.verTodos}>Ver todas</Text>
          </TouchableOpacity>
        </View>

        {painel.turmas.length > 0 ? (
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={{ gap: 12, paddingBottom: 5 }}
          >
            {painel.turmas.map((turma) => (
              <View key={turma.id} style={styles.turmaCard}>
                <View style={styles.turmaIconWrap}>
                  <Ionicons name="school" size={20} color="#fff" />
                </View>
                <Text style={styles.turmaNome} numberOfLines={1}>{turma.nome}</Text>
                <Text style={styles.turmaAlunos}>{turma.alunos} alunos</Text>

                <View style={styles.turmaStatsRow}>
                  <View style={styles.turmaStatItem}>
                    <Feather name="folder" size={13} color="#666" />
                    <Text style={styles.turmaStatText}>{turma.projetos}</Text>
                  </View>
                </View>

                <TouchableOpacity style={styles.acessarBtn} onPress={() => abrirTurma(turma)}>
                  <Text style={styles.acessarBtnText}>Acessar</Text>
                </TouchableOpacity>
              </View>
            ))}
          </ScrollView>
        ) : (
          <Text style={styles.emptyText}>Nenhuma turma vinculada a você ainda.</Text>
        )}

        {/* PRÓXIMOS EVENTOS (hoje + futuros) */}
        <View style={styles.sectionHeaderRow}>
          <Text style={styles.sectionTitle}>Próximos eventos</Text>
          <TouchableOpacity onPress={() => {
            try { navigation.navigate("Eventos"); } catch (e) {}
          }}>
            <Text style={styles.verTodos}>Ver agenda</Text>
          </TouchableOpacity>
        </View>

        {painel.eventosProximos.length > 0 ? (
          <View style={styles.card}>
            {painel.eventosProximos.map((evento, index) => (
              <View
                key={evento.id}
                style={[
                  styles.eventoRow,
                  index < painel.eventosProximos.length - 1 && styles.eventoRowBorda,
                ]}
              >
                <View style={styles.eventoBarra} />
                <View style={{ flex: 1 }}>
                  <Text style={styles.eventoHora}>{formatarHora(evento.hora)}</Text>
                  <Text style={styles.eventoTitulo}>{evento.titulo}</Text>
                  {evento.local ? <Text style={styles.eventoLocal}>{evento.local}</Text> : null}
                </View>
                <View style={styles.eventoTag}>
                  <Text style={styles.eventoTagText}>{obterRotuloEvento(evento.data)}</Text>
                </View>
              </View>
            ))}
          </View>
        ) : (
          <Text style={styles.emptyText}>Nenhum evento próximo cadastrado.</Text>
        )}

        {/* ÚLTIMOS FÓRUNS CRIADOS + ÚLTIMOS PROJETOS ENVIADOS */}
        <View style={{ marginTop: 10 }}>
          <View style={styles.sectionHeaderRow}>
            <Text style={styles.sectionTitle}>Últimos fóruns criados</Text>
            <TouchableOpacity onPress={() => {
              try { navigation.navigate("Fórum"); } catch (e) {}
            }}>
              <Text style={styles.verTodos}>Ver todos</Text>
            </TouchableOpacity>
          </View>

          {painel.ultimosForuns.length > 0 ? (
            <View style={styles.card}>
              {painel.ultimosForuns.map((forum, index) => (
                <TouchableOpacity
                  key={forum.id}
                  style={[
                    styles.forumPendenteRow,
                    index < painel.ultimosForuns.length - 1 && styles.eventoRowBorda,
                  ]}
                  activeOpacity={0.7}
                  onPress={() => {
                    try { navigation.navigate("Fórum", { forumId: forum.id }); } catch (e) {}
                  }}
                >
                  <View style={styles.forumIconCircle}>
                    <MaterialCommunityIcons name="comment-text-multiple" size={18} color="#fff" />
                  </View>
                  <View style={{ flex: 1 }}>
                    <Text style={styles.forumPendenteTitulo} numberOfLines={1}>
                      {forum.nome}
                    </Text>
                    <Text style={styles.forumPendenteSub}>
                      por {forum.autor || "Alguém"} • {forum.total_topicos} tópico(s) • {formatarTempoRelativo(forum.data_criacao)}
                    </Text>
                  </View>
                  <Ionicons name="chevron-forward" size={18} color="#999" />
                </TouchableOpacity>
              ))}
            </View>
          ) : (
            <Text style={styles.emptyText}>Nenhum fórum criado ainda.</Text>
          )}

          <View style={styles.sectionHeaderRow}>
            <Text style={styles.sectionTitle}>Últimos projetos enviados</Text>
          </View>

          {painel.ultimosProjetos.length > 0 ? (
            <View style={styles.card}>
              {painel.ultimosProjetos.map((proj, index) => (
                <View
                  key={proj.id}
                  style={[
                    styles.projetoRow,
                    index < painel.ultimosProjetos.length - 1 && styles.eventoRowBorda,
                  ]}
                >
                  <View style={[styles.pendenciaIconWrap, { backgroundColor: "#D1FAE5" }]}>
                    <Feather name="folder" size={16} color="#059669" />
                  </View>
                  <View style={{ flex: 1 }}>
                    <Text style={styles.projetoNome} numberOfLines={1}>{proj.nome}</Text>
                    <Text style={styles.projetoTurma}>{proj.turma}</Text>
                  </View>
                </View>
              ))}
            </View>
          ) : (
            <Text style={styles.emptyText}>Nenhum projeto enviado ainda.</Text>
          )}
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#1459b3" },
  center: { justifyContent: "center", alignItems: "center" },
  container: { flex: 1, backgroundColor: "#fff" },
  scrollContent: { paddingHorizontal: 18, paddingBottom: 30, paddingTop: 15 },

  resumoTurmas: { color: "#777", fontSize: 13, fontWeight: "600", marginBottom: 4 },

  sectionTitle: { fontSize: 18, fontWeight: "bold", color: "#111" },
  sectionHeaderRow: {
    flexDirection: "row", justifyContent: "space-between", alignItems: "center",
    marginTop: 22, marginBottom: 12,
  },
  verTodos: { color: COLORS.primary, fontWeight: "600", fontSize: 13 },

  statsGrid: { flexDirection: "row", flexWrap: "wrap", gap: 10, marginTop: 14 },
  statCard: {
    width: "47%", backgroundColor: "#fff", borderRadius: 16, padding: 14,
    borderWidth: 1, borderColor: "#F1F5F9", elevation: 2,
  },
  statIconWrap: {
    width: 36, height: 36, borderRadius: 10,
    justifyContent: "center", alignItems: "center", marginBottom: 10,
  },
  statNumber: { fontSize: 24, fontWeight: "bold", color: "#111" },
  statLabel: { fontSize: 13, fontWeight: "700", color: "#333", marginTop: 2 },
  statSubLabel: { fontSize: 11, color: "#999" },

  card: {
    backgroundColor: "#fff", borderRadius: 16, borderWidth: 1, borderColor: "#F1F5F9",
    elevation: 2, padding: 6,
  },
  pendenciaRow: { flexDirection: "row", alignItems: "center", padding: 10, gap: 10 },
  pendenciaIconWrap: {
    width: 36, height: 36, borderRadius: 10,
    justifyContent: "center", alignItems: "center",
  },
  pendenciaTitulo: { fontWeight: "700", fontSize: 14, color: "#111" },
  pendenciaSub: { fontSize: 12, color: "#777", marginTop: 2 },
  pendenciaBadge: {
    backgroundColor: "#EDE9FE", borderRadius: 12, paddingHorizontal: 10, paddingVertical: 4,
    marginRight: 6,
  },
  pendenciaBadgeText: { color: "#7C3AED", fontWeight: "bold", fontSize: 13 },

  turmaCard: {
    width: 170, backgroundColor: "#fff", borderRadius: 16, padding: 14,
    borderWidth: 1, borderColor: "#F1F5F9", elevation: 2,
  },
  turmaIconWrap: {
    width: 38, height: 38, borderRadius: 10, backgroundColor: COLORS.primary,
    justifyContent: "center", alignItems: "center", marginBottom: 8,
  },
  turmaNome: { fontWeight: "bold", fontSize: 15, color: "#111" },
  turmaAlunos: { fontSize: 12, color: "#777", marginTop: 2 },
  turmaStatsRow: { flexDirection: "row", gap: 12, marginTop: 10 },
  turmaStatItem: { flexDirection: "row", alignItems: "center", gap: 4 },
  turmaStatText: { fontSize: 12, color: "#555", fontWeight: "600" },
  acessarBtn: {
    marginTop: 12, backgroundColor: "#EEF2FF", borderRadius: 10,
    paddingVertical: 8, alignItems: "center",
  },
  acessarBtnText: { color: COLORS.primary, fontWeight: "700", fontSize: 13 },

  eventoRow: { flexDirection: "row", alignItems: "center", padding: 12, gap: 10 },
  eventoRowBorda: { borderBottomWidth: 1, borderBottomColor: "#F1F5F9" },
  eventoBarra: { width: 4, height: 34, borderRadius: 2, backgroundColor: COLORS.primary },
  eventoHora: { fontSize: 12, color: COLORS.primary, fontWeight: "700" },
  eventoTitulo: { fontSize: 14, fontWeight: "700", color: "#111", marginTop: 2 },
  eventoLocal: { fontSize: 12, color: "#888", marginTop: 2 },
  eventoTag: { backgroundColor: "#EEF2FF", borderRadius: 10, paddingHorizontal: 10, paddingVertical: 4 },
  eventoTagText: { color: COLORS.primary, fontSize: 11, fontWeight: "700" },

  forumPendenteRow: { flexDirection: "row", alignItems: "center", padding: 12, gap: 10 },
  forumIconCircle: {
    width: 36, height: 36, borderRadius: 18, backgroundColor: "#5360f0",
    justifyContent: "center", alignItems: "center",
  },
  forumPendenteTitulo: { fontWeight: "700", fontSize: 14, color: "#111" },
  forumPendenteSub: { fontSize: 12, color: "#888", marginTop: 2 },
  responderBtn: {
    backgroundColor: "#EDE9FE", marginHorizontal: 12, marginBottom: 12, borderRadius: 12,
    paddingVertical: 10, alignItems: "center",
  },
  responderBtnText: { color: "#7C3AED", fontWeight: "700", fontSize: 13 },

  projetoRow: { flexDirection: "row", alignItems: "center", padding: 10, gap: 10 },
  projetoNome: { fontWeight: "700", fontSize: 14, color: "#111" },
  projetoTurma: { fontSize: 12, color: "#888", marginTop: 2 },

  emptyText: { textAlign: "center", color: "#999", marginVertical: 10, fontSize: 13 },
});