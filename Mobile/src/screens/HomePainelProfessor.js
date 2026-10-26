import React, { useState, useCallback, useContext } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Image,
} from "react-native";
import Skeleton from "../components/Skeleton";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useFocusEffect } from "@react-navigation/native";
import { Ionicons, Feather, MaterialCommunityIcons } from "@expo/vector-icons";
import { COLORS } from "../components/Cores";
import Header from "../components/Header";
import api from "../services/api";
import { URL_BASE } from "../config/backend";
import { useNotifications } from "../context/NotificationContext";

// Importação do Contexto de Tema (mesmo padrão usado no RepositorioScreen)
import { ThemeContext } from "../context/ThemeContext";

// ==========================================
// FUNÇÕES AUXILIARES DE FORMATAÇÃO
// ==========================================
function formatarHora(horaString) {
  if (!horaString) return "";
  return horaString.toString().slice(0, 5); // "10:00:00" -> "10:00"
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

function obterDataEventoLocal(dataString) {
  if (!dataString) return null;

  const dataTexto = String(dataString).slice(0, 10);
  const partesData = dataTexto.split("-").map(Number);

  if (partesData.length === 3 && partesData.every(Number.isFinite)) {
    return new Date(partesData[0], partesData[1] - 1, partesData[2]);
  }

  const data = new Date(dataString);
  return Number.isNaN(data.getTime()) ? null : data;
}

// Mantém a classificação alinhada ao calendário Web: hoje = amarelo.
function obterCorEvento(dataString) {
  const dataEvento = obterDataEventoLocal(dataString);
  if (!dataEvento) return "#10B981";

  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);
  dataEvento.setHours(0, 0, 0, 0);

  if (dataEvento.getTime() < hoje.getTime()) {
    return "#EF5350"; // Vermelho (Passado)
  } else if (dataEvento.getTime() === hoje.getTime()) {
      return "#FFD700"; // Amarelo (Hoje)
  } else {
    return "#10B981"; // Verde (Futuro)
  }
}

// Extrai Mês e Dia para o badge do calendário
function obterDadosData(dataString) {
  if (!dataString) return { mes: "---", dia: "--" };
  const data = new Date(dataString);
  const meses = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"];
  return {
    mes: meses[data.getUTCMonth()],
    dia: data.getUTCDate(),
  };
}

function normalizarImagemProjeto(valor) {
  if (typeof valor !== "string" || !valor.trim() || valor.trim().toLowerCase() === "null") {
    return null;
  }

  const imagem = valor.trim();
  if (/^https?:\/\//i.test(imagem)) return imagem;
  if (/^\/\//.test(imagem)) return `https:${imagem}`;
  if (/^\//.test(imagem)) return `${URL_BASE}${imagem}`;
  return `https://res.cloudinary.com/dw0pxfap3/${imagem}`;
}

function ImagemProjeto({ imagem, fontSizeScale }) {
  const imagemUrl = normalizarImagemProjeto(imagem);

  if (imagemUrl) {
    return <Image source={{ uri: imagemUrl }} style={styles.projetoImagem} />;
  }

  return (
    <View style={[styles.pendenciaIconWrap, { backgroundColor: "#D1FAE5" }]}>
      <Feather name="folder" size={16 * fontSizeScale} color="#059669" />
    </View>
  );
}

// ==========================================
// COMPONENTE PRINCIPAL
// ==========================================
export default function HomePainelProfessor({ navigation }) {
  // AQUI ESTÁ A CORREÇÃO! Puxando as configurações visuais do app (mesmo padrão do RepositorioScreen).
  const context = useContext(ThemeContext);
  const theme = context?.theme || {
    background: "#FFFFFF",
    card: "#F8FAFC",
    text: "#000000",
    border: "#E2E8F0",
    dark: false,
  };
  const fontSizeScale = context?.fontSizeScale || 1;

  const { totalNovas, markAllAsRead } = useNotifications();
  const [carregando, setCarregando] = useState(true);
  const [painel, setPainel] = useState({
    professor: { nome: "", sobrenome: "" },
    totais: { turmas: 0, alunos: 0, projetos: 0, topicos: 0, eventosHoje: 0 },
    turmas: [],
    eventosProximos: [],
    topicosComMensagens: [],
    totalMensagensNovas: 0,
    ultimosForuns: [],
    ultimosProjetos: [],
  });

  const carregarPainel = useCallback(async (silencioso = false) => {
    try {
      if (!silencioso) setCarregando(true);
      const idSalvo = await AsyncStorage.getItem("idUsuario");
      if (!idSalvo) return;

      const resposta = await api.get("/professor/painel", {
        params: { professorId: idSalvo },
      });

      if (resposta.data?.sucesso) {
        setPainel((prev) => ({
          professor: resposta.data.professor || prev.professor,
          totais: resposta.data.totais || prev.totais,
          turmas: resposta.data.turmas || [],
          eventosProximos: resposta.data.eventosProximos || [],
          topicosComMensagens: resposta.data.topicosComMensagens || [],
          totalMensagensNovas: resposta.data.totalMensagensNovas || 0,
          ultimosForuns: resposta.data.ultimosForuns || [],
          ultimosProjetos: resposta.data.ultimosProjetos || [],
        }));
      }
    } catch (error) {
      console.warn("⚠️ Erro ao carregar painel do professor:", error.message);
    } finally {
      if (!silencioso) setCarregando(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      carregarPainel();

      const intervaloAtualizacao = setInterval(() => {
        carregarPainel(true);
      }, 6000);

      return () => clearInterval(intervaloAtualizacao);
    }, [carregarPainel])
  );

  const abrirTopico = (topico) => {
    try {
      navigation.navigate("Conversa", {
        forum: topico.forum_nome || "Fórum",
        topico: {
          id: topico.id,
          titulo: topico.titulo,
          forumId: topico.forum_id,
        },
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
    painel.topicosComMensagens.length > 0 ? painel.topicosComMensagens[0] : null;

  if (carregando && painel.turmas.length === 0) {
    return (
      <View style={[styles.safe, styles.center, { backgroundColor: theme.dark ? theme.background : "#1459b3" }]}>
        <View style={{ width: "100%", padding: 20 }}>
          {[1, 2, 3].map((item) => (
            <Skeleton key={item} width="100%" height={120} borderRadius={22} style={{ marginBottom: 16, backgroundColor: '#fff' }} />
          ))}
        </View>
      </View>
    );
  }

  return (
    <View style={[styles.safe, { backgroundColor: theme.dark ? theme.background : "#1459b3" }]}>
      <Header
        nomeTela={
          carregando
            ? "Carregando..."
            : `Olá,  ${painel.professor.nome} 👋`
        }
        exibirPerfil={true}
        subtitulo="Professor"
        quantidadeNotificacoes={totalNovas}
        aoClicarNoSino={markAllAsRead}
        carregando={carregando}
      />

      <ScrollView
        style={[styles.container, { backgroundColor: theme.background }]}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        

        <Text style={[styles.sectionTitle, { color: theme.text, fontSize: 18 * fontSizeScale }]}>
          Painel do Professor
        </Text>

        {/* CARDS DE TOTAIS */}
        <View style={styles.statsGrid}>
          <View style={[styles.statCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
            <View style={[styles.statIconWrap, { backgroundColor: "#DBEAFE" }]}>
              <Ionicons name="people" size={20 * fontSizeScale} color="#2563EB" />
            </View>
            <Text style={[styles.statNumber, { color: theme.text, fontSize: 24 * fontSizeScale }]}>
              {painel.totais.turmas}
            </Text>
            <Text style={[styles.statLabel, { color: theme.text, fontSize: 13 * fontSizeScale }]}>Turmas</Text>
            <Text style={[styles.statSubLabel, { color: theme.text, opacity: 0.55, fontSize: 11 * fontSizeScale }]}>
              {painel.totais.alunos} alunos
            </Text>
          </View>

          <View style={[styles.statCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
            <View style={[styles.statIconWrap, { backgroundColor: "#D1FAE5" }]}>
              <Feather name="folder" size={20 * fontSizeScale} color="#059669" />
            </View>
            <Text style={[styles.statNumber, { color: theme.text, fontSize: 24 * fontSizeScale }]}>
              {painel.totais.projetos}
            </Text>
            <Text style={[styles.statLabel, { color: theme.text, fontSize: 13 * fontSizeScale }]}>Projetos</Text>
            <Text style={[styles.statSubLabel, { color: theme.text, opacity: 0.55, fontSize: 11 * fontSizeScale }]}>
              ativos
            </Text>
          </View>

          <View style={[styles.statCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
            <View style={[styles.statIconWrap, { backgroundColor: "#EDE9FE" }]}>
              <MaterialCommunityIcons name="comment-text-multiple" size={20 * fontSizeScale} color="#7C3AED" />
            </View>
            <Text style={[styles.statNumber, { color: theme.text, fontSize: 24 * fontSizeScale }]}>
              {painel.totais.topicos}
            </Text>
            <Text style={[styles.statLabel, { color: theme.text, fontSize: 13 * fontSizeScale }]}>Tópicos</Text>
            <Text style={[styles.statSubLabel, { color: theme.text, opacity: 0.55, fontSize: 11 * fontSizeScale }]}>
              no fórum
            </Text>
          </View>

          <View style={[styles.statCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
            <View style={[styles.statIconWrap, { backgroundColor: "#FEF3C7" }]}>
              <Ionicons name="calendar" size={20 * fontSizeScale} color="#D97706" />
            </View>
            <Text style={[styles.statNumber, { color: theme.text, fontSize: 24 * fontSizeScale }]}>
              {painel.totais.eventosHoje}
            </Text>
            <Text style={[styles.statLabel, { color: theme.text, fontSize: 13 * fontSizeScale }]}>Eventos</Text>
            <Text style={[styles.statSubLabel, { color: theme.text, opacity: 0.55, fontSize: 11 * fontSizeScale }]}>
              hoje
            </Text>
          </View>
        </View>

        {/* PENDÊNCIAS */}
        <View style={styles.sectionHeaderRow}>
          <Text style={[styles.sectionTitle, { color: theme.text, fontSize: 18 * fontSizeScale }]}>Pendências</Text>
        </View>

        <View style={[styles.card, { backgroundColor: theme.card, borderColor: theme.border }]}>
          <TouchableOpacity
            style={styles.pendenciaRow}
            activeOpacity={0.7}
            onPress={() => {
              if (primeiroTopicoPendente) {
                abrirTopico(primeiroTopicoPendente);
              } else {
                navigation.navigate("Fórum");
              }
            }}
          >
            <View style={[styles.pendenciaIconWrap, { backgroundColor: "#EDE9FE" }]}>
              <MaterialCommunityIcons name="comment-question-outline" size={20 * fontSizeScale} color="#7C3AED" />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={[styles.pendenciaTitulo, { color: theme.text, fontSize: 14 * fontSizeScale }]}>
                Novas mensagens
              </Text>
              <Text style={[styles.pendenciaSub, { color: theme.text, opacity: 0.6, fontSize: 12 * fontSizeScale }]}>
                {painel.totalMensagensNovas} mensagem(ns) nos seus fóruns
              </Text>
            </View>
            <View style={styles.pendenciaBadge}>
              <Text style={[styles.pendenciaBadgeText, { fontSize: 13 * fontSizeScale }]}>
                {painel.totalMensagensNovas}
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={18} color={theme.text} style={{ opacity: 0.5 }} />
          </TouchableOpacity>
        </View>

        {/* MINHAS TURMAS */}
        <View style={styles.sectionHeaderRow}>
          <Text style={[styles.sectionTitle, { color: theme.text, fontSize: 18 * fontSizeScale }]}>Minhas turmas</Text>
          <TouchableOpacity onPress={() => { try { navigation.navigate("Turmas"); } catch (e) {} }}>
            <Text style={[styles.verTodos, { fontSize: 13 * fontSizeScale }]}>Ver todas</Text>
          </TouchableOpacity>
        </View>

        {painel.turmas.length > 0 ? (
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={{ gap: 12, paddingBottom: 5 }}
          >
            {painel.turmas.map((turma) => (
              <View key={turma.id} style={[styles.turmaCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
                <View style={styles.turmaIconWrap}>
                  <Ionicons name="school" size={20 * fontSizeScale} color="#fff" />
                </View>
                <Text style={[styles.turmaNome, { color: theme.text, fontSize: 15 * fontSizeScale }]} numberOfLines={2}>
                  {turma.nome}
                </Text>
                <Text style={[styles.turmaAlunos, { color: theme.text, opacity: 0.6, fontSize: 12 * fontSizeScale }]}>
                  {turma.alunos} alunos
                </Text>

                <View style={styles.turmaStatsRow}>
                  <View style={styles.turmaStatItem}>
                    <Feather name="folder" size={13 * fontSizeScale} color={theme.text} style={{ opacity: 0.7 }} />
                    <Text style={[styles.turmaStatText, { color: theme.text, opacity: 0.7, fontSize: 12 * fontSizeScale }]}>
                      {turma.projetos}
                    </Text>
                  </View>
                </View>

                <TouchableOpacity style={styles.acessarBtn} onPress={() => abrirTurma(turma)}>
                  <Text style={[styles.acessarBtnText, { fontSize: 13 * fontSizeScale }]}>Acessar</Text>
                </TouchableOpacity>
              </View>
            ))}
          </ScrollView>
        ) : (
          <Text style={[styles.emptyText, { color: theme.text, opacity: 0.5, fontSize: 13 * fontSizeScale }]}>
            Nenhuma turma vinculada a você ainda.
          </Text>
        )}

        {/* PRÓXIMOS EVENTOS COM CORES DINÂMICAS */}
        <View style={styles.sectionHeaderRow}>
          <Text style={[styles.sectionTitle, { color: theme.text, fontSize: 18 * fontSizeScale }]}>Próximos eventos</Text>
          <TouchableOpacity onPress={() => { try { navigation.navigate("Eventos"); } catch (e) {} }}>
            <Text style={[styles.verTodos, { fontSize: 13 * fontSizeScale }]}>Ver agenda</Text>
          </TouchableOpacity>
        </View>

        {painel.eventosProximos.length > 0 ? (
          <View style={styles.eventosList}>
            {painel.eventosProximos.map((evento) => {
              const { mes, dia } = obterDadosData(evento.data);
              const corTema = obterCorEvento(evento.data);

              return (
                <TouchableOpacity
                  key={evento.id}
                  style={[styles.eventoCard, { backgroundColor: theme.card, borderColor: theme.border }]}
                  activeOpacity={0.8}
                  onPress={() => navigation.navigate("Eventos", { selectedDate: evento.data })}
                >
                  {/* Ícone Estilo Folhinha de Calendário */}
                  <View style={[styles.calendarIcon, { borderColor: corTema }]}>
                    <View style={[styles.calendarHeader, { backgroundColor: corTema }]}>
                      <Text style={styles.calendarMonthText}>{mes}</Text>
                    </View>
                    <View style={[styles.calendarBody, { backgroundColor: theme.card }]}>
                      <Text style={[styles.calendarDayText, { color: theme.text }]}>{dia}</Text>
                    </View>
                  </View>

                  {/* Informações do Evento */}
                  <View style={{ flex: 1, justifyContent: "center" }}>
                    <Text style={[styles.eventoTitulo, { color: theme.text, fontSize: 15 * fontSizeScale }]} numberOfLines={1}>
                      {evento.titulo}
                    </Text>
                    <View style={styles.eventoMetaRow}>
                      <Feather name="clock" size={12 * fontSizeScale} color={theme.text} style={{ opacity: 0.6, marginRight: 4 }} />
                      <Text style={[styles.eventoMetaText, { color: theme.text, opacity: 0.6, fontSize: 12 * fontSizeScale }]}>
                        {formatarHora(evento.hora)} {evento.local ? `• ${evento.local}` : ""}
                      </Text>
                    </View>
                  </View>

                  {/* Ponto Indicador na Direita */}
                  <View style={[styles.statusDot, { backgroundColor: corTema }]} />
                </TouchableOpacity>
              );
            })}
          </View>
        ) : (
          <Text style={[styles.emptyText, { color: theme.text, opacity: 0.5, fontSize: 13 * fontSizeScale }]}>
            Nenhum evento próximo cadastrado.
          </Text>
        )}

        {/* ÚLTIMOS FÓRUNS CRIADOS + ÚLTIMOS PROJETOS ENVIADOS */}
        <View style={{ marginTop: 10 }}>
          <View style={styles.sectionHeaderRow}>
            <Text style={[styles.sectionTitle, { color: theme.text, fontSize: 18 * fontSizeScale }]}>Últimos fóruns criados</Text>
            <TouchableOpacity onPress={() => { try { navigation.navigate("Fórum"); } catch (e) {} }}>
              <Text style={[styles.verTodos, { fontSize: 13 * fontSizeScale }]}>Ver todos</Text>
            </TouchableOpacity>
          </View>

          {painel.ultimosForuns.length > 0 ? (
            <View style={[styles.card, { backgroundColor: theme.card, borderColor: theme.border }]}>
              {painel.ultimosForuns.map((forum, index) => (
                <TouchableOpacity
                  key={forum.id}
                  style={[
                    styles.forumPendenteRow,
                    index < painel.ultimosForuns.length - 1 && [styles.eventoRowBorda, { borderBottomColor: theme.border }],
                  ]}
                  activeOpacity={0.7}
                  onPress={() => {
                    try { navigation.navigate("Fórum", { forumId: forum.id }); } catch (e) {}
                  }}
                >
                  <View style={styles.forumIconCircle}>
                    <MaterialCommunityIcons name="comment-text-multiple" size={18 * fontSizeScale} color="#fff" />
                  </View>
                  <View style={{ flex: 1 }}>
                    <Text style={[styles.forumPendenteTitulo, { color: theme.text, fontSize: 14 * fontSizeScale }]} numberOfLines={1}>
                      {forum.nome}
                    </Text>
                    <Text style={[styles.forumPendenteSub, { color: theme.text, opacity: 0.6, fontSize: 12 * fontSizeScale }]}>
                      por {forum.autor || "Alguém"} • {forum.total_topicos} tópico(s) • {formatarTempoRelativo(forum.data_criacao)}
                    </Text>
                  </View>
                  <Ionicons name="chevron-forward" size={18} color={theme.text} style={{ opacity: 0.5 }} />
                </TouchableOpacity>
              ))}
            </View>
          ) : (
            <Text style={[styles.emptyText, { color: theme.text, opacity: 0.5, fontSize: 13 * fontSizeScale }]}>
              Nenhum fórum criado ainda.
            </Text>
          )}

          <View style={styles.sectionHeaderRow}>
            <Text style={[styles.sectionTitle, { color: theme.text, fontSize: 18 * fontSizeScale }]}>Últimos projetos enviados</Text>
          </View>

          {painel.ultimosProjetos.length > 0 ? (
            <View style={[styles.card, { backgroundColor: theme.card, borderColor: theme.border }]}>
              {painel.ultimosProjetos.map((proj, index) => (
                <TouchableOpacity
                  key={proj.id}
                  style={[
                    styles.projetoRow,
                    index < painel.ultimosProjetos.length - 1 && [styles.eventoRowBorda, { borderBottomColor: theme.border }],
                  ]}
                  activeOpacity={0.8}
                  onPress={() => navigation.navigate("Repositorio", { projetoId: proj.id, projetoNome: proj.nome })}
                >
                  <ImagemProjeto imagem={proj.imagem} fontSizeScale={fontSizeScale} />
                  <View style={{ flex: 1 }}>
                    <Text style={[styles.projetoNome, { color: theme.text, fontSize: 14 * fontSizeScale }]} numberOfLines={1}>
                      {proj.nome}
                    </Text>
                    <Text style={[styles.projetoTurma, { color: theme.text, opacity: 0.6, fontSize: 12 * fontSizeScale }]}>
                      {proj.turma}
                    </Text>
                  </View>
                </TouchableOpacity>
              ))}
            </View>
          ) : (
            <Text style={[styles.emptyText, { color: theme.text, opacity: 0.5, fontSize: 13 * fontSizeScale }]}>
              Nenhum projeto enviado ainda.
            </Text>
          )}
        </View>
      </ScrollView>
    </View>
  );
}

// ==========================================
// ESTILOS (valores estáticos de layout; cores/tema aplicados inline acima)
// ==========================================
const styles = StyleSheet.create({
  safe: { flex: 1 },
  center: { justifyContent: "center", alignItems: "center" },
  container: { flex: 1 },
  scrollContent: { paddingHorizontal: 18, paddingBottom: 30, paddingTop: 0 },

  resumoTurmas: { fontWeight: "600", marginBottom: 4 },

  sectionTitle: { fontWeight: "bold" },
  sectionHeaderRow: {
    flexDirection: "row", justifyContent: "space-between", alignItems: "center",
    marginTop: 22, marginBottom: 12,
  },
  verTodos: { color: COLORS.primary, fontWeight: "600" },

  statsGrid: { flexDirection: "row", flexWrap: "wrap", gap: 10, marginTop: 14, justifyContent: 'space-between' },
  statCard: {
    flexBasis: "48%",
    maxWidth: "48%",
    minWidth: 150,
    borderRadius: 16,
    padding: 14,
    borderWidth: 1,
    elevation: 2,
  },
  statIconWrap: {
    width: 36, height: 36, borderRadius: 10,
    justifyContent: "center", alignItems: "center", marginBottom: 10,
  },
  statNumber: { fontWeight: "bold" },
  statLabel: { fontWeight: "700", marginTop: 2 },
  statSubLabel: {},

  card: {
    borderRadius: 16, borderWidth: 1,
    elevation: 2, padding: 6,
  },
  pendenciaRow: { flexDirection: "row", alignItems: "center", padding: 10, gap: 10 },
  pendenciaIconWrap: {
    width: 36, height: 36, borderRadius: 10,
    justifyContent: "center", alignItems: "center",
  },
  pendenciaTitulo: { fontWeight: "700" },
  pendenciaSub: { marginTop: 2 },
  projetoImagem: {
    width: 36, height: 36, borderRadius: 10,
    resizeMode: "cover",
  },
  pendenciaBadge: {
    backgroundColor: "#EDE9FE", borderRadius: 12, paddingHorizontal: 10, paddingVertical: 4,
    marginRight: 6,
  },
  pendenciaBadgeText: { color: "#7C3AED", fontWeight: "bold" },

  turmaCard: {
    width: 180,
    flexGrow: 0,
    flexShrink: 0,
    borderRadius: 16,
    padding: 14,
    borderWidth: 1,
    elevation: 2,
  },
  turmaIconWrap: {
    width: 38, height: 38, borderRadius: 10, backgroundColor: COLORS.primary,
    justifyContent: "center", alignItems: "center", marginBottom: 8,
  },
  turmaNome: { fontWeight: "bold" },
  turmaAlunos: { marginTop: 2 },
  turmaStatsRow: { flexDirection: "row", gap: 12, marginTop: 10 },
  turmaStatItem: { flexDirection: "row", alignItems: "center", gap: 4 },
  turmaStatText: { fontWeight: "600" },
  acessarBtn: {
    marginTop: 12, backgroundColor: "#EEF2FF", borderRadius: 10,
    minHeight: 40, paddingHorizontal: 10, paddingVertical: 8,
    width: "100%", alignItems: "center", justifyContent: "center",
  },
  acessarBtnText: { color: COLORS.primary, fontWeight: "700" },

  // ESTILOS DO CALENDÁRIO
  eventosList: {
    gap: 12,
  },
  eventoCard: {
    borderRadius: 18,
    paddingHorizontal: 14,
    paddingVertical: 12,
    flexDirection: "row",
    alignItems: "center",
    gap: 14,
    borderWidth: 1,
    elevation: 2,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 6,
  },
  calendarIcon: {
    width: 52,
    height: 52,
    borderRadius: 12,
    borderWidth: 1,
    overflow: "hidden",
    alignItems: "center",
  },
  calendarHeader: {
    width: "100%",
    paddingVertical: 3,
    alignItems: "center",
  },
  calendarMonthText: {
    color: "#fff",
    fontSize: 10,
    fontWeight: "bold",
    textTransform: "uppercase",
  },
  calendarBody: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  calendarDayText: {
    fontSize: 18,
    fontWeight: "bold",
  },
  eventoTitulo: {
    fontWeight: "bold",
    marginBottom: 4,
  },
  eventoMetaRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  eventoMetaText: {},
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginLeft: 6,
  },

  forumPendenteRow: { flexDirection: "row", alignItems: "center", padding: 12, gap: 10 },
  eventoRowBorda: { borderBottomWidth: 1 },
  forumIconCircle: {
    width: 36, height: 36, borderRadius: 18, backgroundColor: "#5360f0",
    justifyContent: "center", alignItems: "center",
  },
  forumPendenteTitulo: { fontWeight: "700" },
  forumPendenteSub: { marginTop: 2 },

  projetoRow: { flexDirection: "row", alignItems: "center", padding: 10, gap: 10 },
  projetoNome: { fontWeight: "700" },
  projetoTurma: { marginTop: 2 },

  emptyText: { textAlign: "center", marginVertical: 10 },
});
