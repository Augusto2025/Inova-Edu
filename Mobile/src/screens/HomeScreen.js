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
  Alert,
  Keyboard
} from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import Header from "../components/Header";
import Skeleton from "../components/Skeleton";
import { COLORS } from "../components/Cores";
import { MaterialCommunityIcons, Feather, Ionicons } from "@expo/vector-icons";
import api, { API_ENDPOINTS } from "../services/api"; // Garanta que importou o API_ENDPOINTS
import { useNotifications } from "../context/NotificationContext";
import HomePainelProfessor from "./HomePainelProfessor";

// Chave usada para guardar o histórico de repositórios recentes no celular,
// separado por usuário (pra não misturar histórico entre contas diferentes no mesmo aparelho).
const RECENTES_KEY_PREFIX = "@InovaEdu:repositoriosRecentes:";

export default function HomeScreen({ navigation }) {
  const primaryColor = COLORS.primary;

  // 🆕 Descobre se o usuário logado é Aluno ou Professor, pra decidir qual Home mostrar
  const [tipoUsuario, setTipoUsuario] = useState(null);
  const [tipoCarregado, setTipoCarregado] = useState(false);

  const [carregando, setCarregando] = useState(true);
  const [busca, setBusca] = useState("");
  const [repoSearchResults, setRepoSearchResults] = useState([]);
  const [repoSearchLoading, setRepoSearchLoading] = useState(false);
  const [repoSearchError, setRepoSearchError] = useState(null);
  const { totalNovas, markAllAsRead } = useNotifications();
  const [homeData, setHomeData] = useState({
    usuario: { nome: "" },
    eventos: [],
    cursos: [],
    forum: [],
    projetos: [],
  });

  // 🆕 Histórico local de repositórios que o usuário realmente entrou
  const [recentRepos, setRecentRepos] = useState([]);
  const [recentReposCarregado, setRecentReposCarregado] = useState(false);

  const pulseAnim = useRef(new Animated.Value(1)).current;

  // 🆕 Carrega o tipo salvo no login (Aluno/Professor) assim que a tela monta
  useEffect(() => {
    (async () => {
      try {
        const tipo = await AsyncStorage.getItem("tipo");
        setTipoUsuario(tipo);
      } catch (e) {
        console.warn("⚠️ Erro ao ler tipo do usuário:", e.message);
      } finally {
        setTipoCarregado(true);
      }
    })();
  }, []);

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.05,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ]),
    ).start();
  }, [pulseAnim]);

  // Função que busca os dados em tempo real da API na nuvem
  async function carregarHome() {
    try {
      setCarregando(true);

      // 🔑 Pega o ID do usuário logado, salvo no AsyncStorage durante o login
      const idSalvo = await AsyncStorage.getItem("idUsuario");

      // Usa o endpoint mapeado (EXPO_PUBLIC_URL_BACKEND/home), agora enviando o usuarioId
      const resposta = await api.get(API_ENDPOINTS.home || "/home", {
        params: { usuarioId: idSalvo },
      });

      if (resposta.data) {
        const dados = resposta.data;

        // Mesmo que sucesso=false, pode ter dados parciais
        setHomeData({
          usuario: dados.usuario || { nome: "Estudante" },
          eventos: Array.isArray(dados.eventos) ? dados.eventos : [],
          cursos: Array.isArray(dados.cursos) ? dados.cursos : [],
          forum: Array.isArray(dados.forum) ? dados.forum : [],
          projetos: Array.isArray(dados.projetos) ? dados.projetos : [],
        });

        // Se retornou com dados parciais, loga o aviso
        if (dados.aviso) {
          console.warn("⚠️ Dados parciais carregados:", dados.aviso);
        }
      }
    } catch (error) {
      const status = error.response?.status;

      // Se a rota /home não existe (404), houve erro de servidor (5xx) ou falha de rede,
      // tenta o fallback para endpoints individuais para manter a Home populada.
      if (status === 404 || !status || status >= 500) {
        console.log(
          "Rota /home indisponível (status:",
          status,
          ") — usando fallback de endpoints individuais",
        );

        try {
          // Faz as requisições uma por uma para identificar qual falha
          let eventosData = [];
          let cursosData = [];
          let forumData = [];
          let projetosData = [];

          try {
            const eventosRes = await api.get(
              API_ENDPOINTS.eventos || "/eventos",
            );
            eventosData = Array.isArray(eventosRes.data) ? eventosRes.data : [];
            console.log("✅ Eventos carregados:", eventosData.length);
          } catch (e) {
            console.warn(
              "⚠️ Erro ao carregar eventos (fallback):",
              e.response?.status,
              e.message,
            );
          }

          try {
            const cursosRes = await api.get(API_ENDPOINTS.cursos || "/cursos");
            cursosData = Array.isArray(cursosRes.data) ? cursosRes.data : [];
            console.log("✅ Cursos carregados:", cursosData.length);
          } catch (e) {
            console.warn(
              "⚠️ Erro ao carregar cursos (fallback):",
              e.response?.status,
              e.message,
            );
          }

          try {
            const forumRes = await api.get(API_ENDPOINTS.forum || "/forum");
            forumData = Array.isArray(forumRes.data) ? forumRes.data : [];
            console.log("✅ Forum carregado:", forumData.length);
          } catch (e) {
            console.warn(
              "⚠️ Erro ao carregar forum (fallback):",
              e.response?.status,
              e.message,
            );
          }

          try {
            const projetosRes = await api.get(
              API_ENDPOINTS.projetos || "/projetos",
            );
            projetosData = Array.isArray(projetosRes.data)
              ? projetosRes.data
              : [];
            console.log("✅ Projetos carregados:", projetosData.length);
          } catch (e) {
            console.warn(
              "⚠️ Erro ao carregar projetos (fallback):",
              e.response?.status,
              e.message,
            );
          }

          // Mesmo no fallback, tenta manter o nome real do usuário se já tivermos algum salvo
          setHomeData((prev) => ({
            usuario: prev.usuario?.nome ? prev.usuario : { nome: "Estudante" },
            eventos: eventosData,
            cursos: cursosData,
            forum: forumData,
            projetos: projetosData,
          }));

          console.log("✅ Fallback completado com dados parciais");
        } catch (fallbackError) {
          console.error(
            "❌ Erro crítico no fallback da Home:",
            fallbackError.message,
          );
          console.error("Status:", fallbackError.response?.status);
          console.error("Dados:", fallbackError.response?.data);
        }
      } else {
        console.log(
          "Erro ao carregar dados da Home:",
          error.message,
          status,
          error.response?.data,
        );
      }
    } finally {
      setCarregando(false);
    }
  }

  // 🆕 Carrega o histórico local de repositórios recentes (por usuário)
  async function carregarRepositoriosRecentes() {
    try {
      const idSalvo = await AsyncStorage.getItem("idUsuario");
      if (!idSalvo) {
        setRecentRepos([]);
        return;
      }
      const raw = await AsyncStorage.getItem(RECENTES_KEY_PREFIX + idSalvo);
      setRecentRepos(raw ? JSON.parse(raw) : []);
    } catch (e) {
      console.warn("⚠️ Erro ao carregar repositórios recentes:", e.message);
    } finally {
      setRecentReposCarregado(true);
    }
  }

  async function salvarRepositoriosRecentes(lista) {
    try {
      const idSalvo = await AsyncStorage.getItem("idUsuario");
      if (!idSalvo) return;
      await AsyncStorage.setItem(
        RECENTES_KEY_PREFIX + idSalvo,
        JSON.stringify(lista),
      );
    } catch (e) {
      console.warn("⚠️ Erro ao salvar repositórios recentes:", e.message);
    }
  }

  // 🆕 Adiciona (ou traz pro topo, se já existia) um repositório no histórico —
  // chamado sempre que o usuário efetivamente entra em um repositório pela busca.
  function adicionarRepositorioRecente(repo) {
    setRecentRepos((atual) => {
      const semDuplicado = atual.filter((item) => item.id !== repo.id);
      const novaLista = [repo, ...semDuplicado].slice(0, 10); // guarda só os 10 mais recentes
      salvarRepositoriosRecentes(novaLista);
      return novaLista;
    });
  }

  // 🆕 Remove um item do histórico (não apaga o projeto de verdade, só tira da lista local)
  function removerRepositorioRecente(id) {
    setRecentRepos((atual) => {
      const novaLista = atual.filter((item) => item.id !== id);
      salvarRepositoriosRecentes(novaLista);
      return novaLista;
    });
  }

  function confirmarRemoverRecente(repo) {
    Alert.alert(
      "Remover dos recentes",
      `Tirar "${repo.nome}" da lista de repositórios recentes?`,
      [
        { text: "Cancelar", style: "cancel" },
        {
          text: "Remover",
          style: "destructive",
          onPress: () => removerRepositorioRecente(repo.id),
        },
      ],
    );
  }

  useEffect(() => {
    carregarHome();
    carregarRepositoriosRecentes();
  }, []);

  // Recarrega a Home sempre que a tela volta a foco (ex.: após criar um evento)
  useEffect(() => {
    const unsubscribe = navigation.addListener("focus", () => {
      carregarHome();
      carregarRepositoriosRecentes();
    });
    return unsubscribe;
  }, [navigation]);

  function getEventStatusColor(data) {
    if (!data) return "#4CAF50";
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    const evento = new Date(data);
    evento.setHours(0, 0, 0, 0);
    if (evento.getTime() === hoje.getTime()) return "#FFD700";
    return evento > hoje ? "#4CAF50" : "#F44336";
  }

  async function buscarRepositorios(termoBusca) {
    if (!termoBusca || termoBusca.trim() === "") {
      setRepoSearchResults([]);
      setRepoSearchLoading(false);
      setRepoSearchError(null);
      return;
    }

    try {
      setRepoSearchLoading(true);
      const resposta = await api.get(API_ENDPOINTS.repositorioSearch, {
        params: { q: termoBusca, page: 1, limit: 20 },
      });
      setRepoSearchResults(resposta.data.resultados || []);
      setRepoSearchError(null);
    } catch (error) {
      const status = error.response?.status;
      if (status === 404) {
        setRepoSearchError("endpoint_not_found");
        console.log("Busca de repositórios: endpoint não encontrado (404)");
      } else if (status >= 500) {
        setRepoSearchError("server_error");
        console.log(
          "Busca de repositórios: erro interno do servidor",
          error.response?.data || error.message,
        );
      } else {
        setRepoSearchError(
          error.response?.data?.mensagem ||
            error.message ||
            "Erro desconhecido",
        );
        console.log(
          "Erro na busca de repositórios:",
          error.response?.data || error.message,
        );
      }
      setRepoSearchResults([]);
    } finally {
      setRepoSearchLoading(false);
    }
  }

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (busca.trim() !== "") {
        buscarRepositorios(busca.trim());
      } else {
        setRepoSearchResults([]);
      }
    }, 350);

    return () => clearTimeout(timeout);
  }, [busca]);

  const estaBuscando = busca.trim() !== "";
  const forumPrincipal = homeData.forum.length > 0 ? homeData.forum[0] : null;

  // 🆕 Enquanto não sabemos o tipo, evita piscar a tela errada
  if (!tipoCarregado) {
    return (
      <View style={[styles.safe, { justifyContent: "center", alignItems: "center" }]}>
        <Text style={{ color: "#fff" }}>Carregando...</Text>
      </View>
    );
  }

  // 🆕 Professor vê o painel dedicado; o restante do arquivo abaixo é a visão do Aluno
  if (tipoUsuario === "Professor") {
    return <HomePainelProfessor navigation={navigation} />;
  }

  return (
    <View style={styles.safe}>
      <Header
        nomeTela={
          carregando
            ? "Carregando..."
            : `Olá, ${homeData.usuario?.nome || "Estudante"} 👋`
        }
        exibirPerfil={true}
        quantidadeNotificacoes={totalNovas}
        aoClicarNoSino={markAllAsRead}
        carregando={carregando}
      />

      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
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
            const meses = [
              "JAN",
              "FEV",
              "MAR",
              "ABR",
              "MAI",
              "JUN",
              "JUL",
              "AGO",
              "SET",
              "OUT",
              "NOV",
              "DEZ",
            ];
            let dia = "•";
            let mes = "EVT";

            // Mapeia tanto propriedades em inglês (antigas) quanto as colunas do PostgreSQL
            const dataOriginal = event.date || event.data_evento || event.data;
            const tituloEvento = event.title || event.titulo || "Sem título";
            const horarioEvento = event.time || event.horario || "Dia todo";
            const localEvento = event.local || event.local_evento || "InovaEdu";

            if (dataOriginal) {
              const dataObj = new Date(dataOriginal);
              dia = dataObj.getUTCDate();
              mes = meses[dataObj.getUTCMonth()];
            }

            const statusColor = getEventStatusColor(dataOriginal);

            return (
              <TouchableOpacity
                key={event.id || event.idevento}
                style={styles.eventCard}
                activeOpacity={0.8}
                onPress={() =>
                  navigation.navigate("Eventos", { selectedDate: dataOriginal })
                }
              >
                <View style={[styles.dateBadge, { borderColor: statusColor }]}>
                  <View
                    style={[
                      styles.dateBadgeTop,
                      { backgroundColor: statusColor },
                    ]}
                  >
                    <Text style={styles.monthText}>{mes}</Text>
                  </View>
                  <View style={styles.dateBadgeBottom}>
                    <Text style={styles.dayText}>{dia}</Text>
                  </View>
                </View>

                <View style={styles.eventInfo}>
                  <Text style={styles.eventTitle} numberOfLines={1}>
                    {tituloEvento}
                  </Text>
                  <Text style={styles.eventTimeInfo} numberOfLines={1}>
                    <Ionicons name="time-outline" size={13} color="#777" />{" "}
                    {horarioEvento}
                    {" • "}
                    {localEvento}
                  </Text>
                </View>

                <View
                  style={[styles.statusDot, { backgroundColor: statusColor }]}
                />
              </TouchableOpacity>
            );
          })
        ) : (
          <Text style={styles.emptyText}>Nenhum evento encontrado.</Text>
        )}

        {/* SEÇÃO: BUSCA DE REPOSITÓRIOS */}
        <View style={styles.searchContainer}>
          <Text style={styles.searchTitle}>Buscar repositórios</Text>
          <View style={styles.searchBox}>
            <Feather
              name="search"
              size={18}
              color="#888"
              style={{ marginRight: 10 }}
            />
            <TextInput
              placeholder="Buscar por curso, turma ou projeto..."
              placeholderTextColor="#888"
              style={styles.searchInput}
              value={busca}
              onChangeText={setBusca}
            />
          </View>

          {estaBuscando && (
            <View style={{ marginTop: 15 }}>
              {repoSearchLoading ? (
                <Text style={styles.emptyText}>Buscando repositórios...</Text>
              ) : repoSearchError ? (
                <Text style={[styles.emptyText, { color: "#c0392b" }]}>
                  {repoSearchError === "endpoint_not_found"
                    ? "Endpoint de busca indisponível."
                    : repoSearchError === "server_error"
                      ? "Erro interno no servidor ao buscar repositórios."
                      : `Erro ao buscar repositórios: ${repoSearchError}`}
                </Text>
              ) : repoSearchResults.length > 0 ? (
                <ScrollView
                  horizontal
                  showsHorizontalScrollIndicator={false}
                  contentContainerStyle={{ gap: 12 }}
                >
                  {repoSearchResults.map((repo) => {
                    // Resultado pode ser um projeto de verdade, ou só uma turma/curso
                    // que ainda não tem nenhum projeto cadastrado (repo.id vem null nesse caso)
                    const temProjeto =
                      repo.tipo_resultado === "projeto" && repo.id;

                    return (
                      <TouchableOpacity
                        key={repo.chave_unica || repo.id}
                        style={styles.repoCard}
                        activeOpacity={0.8}
                        onPress={() => {
                          if (temProjeto) {
                            // 🆕 Só entra no histórico de "recentes" quando o usuário
                            // realmente clica pra entrar em um repositório de verdade.
                            adicionarRepositorioRecente({
                              id: repo.id,
                              nome: repo.nome_projeto,
                              imagem: repo.imagem,
                              subtitulo: repo.nome_turma || repo.nome_curso,
                            });
                            navigation.navigate("Repositorio", {
                              projetoId: repo.id,
                              projetoNome: repo.nome_projeto,
                            });
                          } else {
                            Alert.alert(
                              "Nenhum projeto ainda",
                              `Ainda não existe projeto cadastrado em "${repo.nome_turma || repo.nome_curso}".`,
                            );
                          }
                        }}
                      >
                        {repo.imagem ? (
                          <Image
                            source={{ uri: repo.imagem }}
                            style={styles.repoImg}
                          />
                        ) : (
                          <View
                            style={[
                              styles.repoImg,
                              styles.centerContainer,
                              { backgroundColor: "#f2f2f2" },
                            ]}
                          >
                            <Feather
                              name={temProjeto ? "folder" : "folder-minus"}
                              size={24}
                              color={temProjeto ? COLORS.primary : "#aaa"}
                            />
                          </View>
                        )}
                        <Text numberOfLines={1} style={styles.repoTitle}>
                          {repo.nome_projeto ||
                            (repo.tipo_resultado === "turma"
                              ? repo.nome_turma
                              : repo.nome_curso) ||
                            "Sem projeto"}
                        </Text>
                        <Text
                          numberOfLines={1}
                          style={[
                            styles.emptyText,
                            { marginTop: 4, color: "#555" },
                          ]}
                        >
                          {repo.nome_turma ||
                            repo.nome_curso ||
                            "Sem turma/curso"}
                        </Text>
                      </TouchableOpacity>
                    );
                  })}
                </ScrollView>
              ) : (
                <Text style={styles.emptyText}>
                  Nenhum repositório encontrado.
                </Text>
              )}
            </View>
          )}
        </View>

        {/* SEÇÃO: REPOSITÓRIOS RECENTES — agora vem do histórico local (AsyncStorage),
              só populado quando o usuário busca e entra em um repositório de verdade. */}
        <View style={styles.repoHeaderRow}>
          <Text style={styles.sectionTitle}>Repositórios recentes</Text>
          {recentRepos.length > 0 && (
            <TouchableOpacity
              onPress={() => navigation.navigate("Repositório")}
            >
              <Text
                style={{
                  color: COLORS.primary,
                  fontWeight: "600",
                  marginTop: 20,
                }}
              >
                Ver todos
              </Text>
            </TouchableOpacity>
          )}
        </View>

        {!recentReposCarregado ? (
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={{ gap: 12, paddingBottom: 5 }}
          >
            {[1, 2].map((i) => (
              <View
                key={i}
                style={[styles.newRepoCard, { width: 220, opacity: 0.6 }]}
              />
            ))}
          </ScrollView>
        ) : recentRepos.length > 0 ? (
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            style={{ marginTop: 4, marginBottom: 6 }}
            contentContainerStyle={{ gap: 12, paddingBottom: 5 }}
          >
            {recentRepos.map((repo) => (
              <View key={repo.id} style={styles.newRepoCard}>
                <TouchableOpacity
                  style={{
                    flex: 1,
                    flexDirection: "row",
                    alignItems: "center",
                  }}
                  activeOpacity={0.85}
                  onPress={() =>
                    navigation.navigate("Repositorio", {
                      projetoId: repo.id,
                      projetoNome: repo.nome,
                    })
                  }
                >
                  <View style={styles.repoLeftIconContainer}>
                    {repo.imagem ? (
                      <Image
                        source={{ uri: repo.imagem }}
                        style={{ width: 40, height: 40, borderRadius: 8 }}
                      />
                    ) : (
                      <Feather name="folder" size={20} color={COLORS.primary} />
                    )}
                  </View>

                  <View style={styles.repoTextContainer}>
                    <Text numberOfLines={1} style={styles.newRepoTitle}>
                      {repo.nome || "Projeto"}
                    </Text>
                    {repo.subtitulo ? (
                      <Text
                        numberOfLines={1}
                        style={{ color: "#6b7280", fontSize: 12, marginTop: 6 }}
                      >
                        {repo.subtitulo}
                      </Text>
                    ) : (
                      <View style={styles.repoTag}>
                        <Text style={styles.repoTagText}>Git Repository</Text>
                      </View>
                    )}
                  </View>
                </TouchableOpacity>

                {/* 🆕 Botão de remover este item da lista de recentes */}
                <TouchableOpacity
                  style={styles.removeRecentBtn}
                  hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
                  onPress={() => confirmarRemoverRecente(repo)}
                >
                  <Feather name="x" size={14} color="#94A3B8" />
                </TouchableOpacity>
              </View>
            ))}
          </ScrollView>
        ) : (
          <Text style={styles.emptyText}>
            Busque e entre em um repositório para ele aparecer aqui.
          </Text>
        )}

        {/* SEÇÃO: FÓRUM */}
        <Text style={styles.sectionTitle}>Fórum ativo</Text>

        {forumPrincipal ? (
          <TouchableOpacity
            style={styles.forumContainerCard}
            activeOpacity={0.8}
            onPress={() => {
              if (!forumPrincipal) return;

              navigation.navigate("Titulo", {
                topico: forumPrincipal,
              });
            }}
          >
            <View style={styles.forumHeaderRow}>
              <View style={styles.forumIconCircle}>
                <MaterialCommunityIcons
                  name="comment-text-multiple"
                  size={20}
                  color="#fff"
                />
              </View>
              <View style={styles.forumTitleBlock}>
                <Text style={styles.forumMainTitle} numberOfLines={1}>
                  {forumPrincipal.titulo}
                </Text>
                <Text style={styles.forumTimeAgo}>tópico recente</Text>
              </View>
              <Animated.View
                style={[
                  styles.forumBadgeCount,
                  {
                    backgroundColor: primaryColor,
                    transform: [{ scale: pulseAnim }],
                  },
                ]}
              >
                <Text style={styles.forumBadgeText}>
                  {forumPrincipal.mensagens || 0}
                </Text>
              </Animated.View>
            </View>
            <Text
              style={styles.forumBodyText}
              numberOfLines={2}>
              {forumPrincipal.conteudo || "Nenhuma mensagem ainda."}
          </Text>
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
  container: { flex: 1, backgroundColor:"#ffffff" },
  scrollContent: { paddingHorizontal: 18, paddingBottom: 30, paddingTop: 5 },
  sectionTitle: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#111",
    marginTop: 20,
    marginBottom: 12,
  },
  centerContainer: { justifyContent: "center", alignItems: "center" },
  eventCard: {
    backgroundColor: "#fff",
    borderRadius: 16,
    padding: 12,
    marginBottom: 10,
    flexDirection: "row",
    alignItems: "center",
    elevation: 2,
  },
  dateBadge: {
    width: 50,
    height: 54,
    borderRadius: 8,
    borderWidth: 1,
    overflow: "hidden",
  },
  dateBadgeTop: { height: 18, justifyContent: "center", alignItems: "center" },
  monthText: { color: "#fff", fontSize: 9, fontWeight: "bold" },
  dateBadgeBottom: { flex: 1, justifyContent: "center", alignItems: "center" },
  dayText: { fontSize: 16, fontWeight: "bold" },
  eventInfo: { flex: 1, paddingHorizontal: 12 },
  eventTitle: { fontSize: 15, fontWeight: "bold", color: "#222" },
  eventTimeInfo: { fontSize: 12, color: "#666", marginTop: 2 },
  statusDot: { width: 8, height: 8, borderRadius: 4 },
  searchContainer: {
    backgroundColor: "#fff",
    borderRadius: 20,
    padding: 16,
    marginTop: 15,
    elevation: 3,
  },
  searchTitle: { fontSize: 18, fontWeight: "bold", marginBottom: 12 },
  searchBox: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#f2f2f2",
    borderRadius: 14,
    paddingHorizontal: 12,
    height: 46,
  },
  searchInput: { flex: 1, color: "#111" },
  miniResultCard: {
    width: 110,
    alignItems: "center",
    backgroundColor: "#fff",
    padding: 6,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#f0f0f0",
  },
  miniResultImg: { width: 95, height: 60, borderRadius: 6 },
  miniResultText: {
    fontSize: 11,
    marginTop: 4,
    color: "#333",
    fontWeight: "600",
  },
  forumContainerCard: {
    backgroundColor: "#fff",
    borderRadius: 16,
    padding: 14,
    elevation: 2,
    marginTop: 5,
  },
  forumHeaderRow: { flexDirection: "row", alignItems: "center" },
  forumIconCircle: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "#5360f0",
    justifyContent: "center",
    alignItems: "center",
    marginRight: 10,
  },
  forumTitleBlock: { flex: 1 },
  forumMainTitle: { fontWeight: "bold", fontSize: 15, color: "#111" },
  forumTimeAgo: { fontSize: 11, color: "#888" },
  forumBadgeCount: {
    width: 20,
    height: 20,
    borderRadius: 10,
    justifyContent: "center",
    alignItems: "center",
  },
  forumBadgeText: { color: "#fff", fontSize: 11, fontWeight: "bold" },
  forumBodyText: {
    marginLeft: 50,
    marginTop: 8,
    color: "#555",
    fontSize: 13,
    lineHeight: 18,
  },
  emptyText: {
    textAlign: "center",
    color: "#999",
    marginVertical: 10,
    fontSize: 13,
  },
  repoCard: {
    width: 140,
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 8,
    alignItems: "center",
    elevation: 2,
  },
  repoImg: { width: 120, height: 68, borderRadius: 8, marginBottom: 8 },
  repoTitle: { fontSize: 13, fontWeight: "600", color: "#222" },
  /* Estilos novos / melhorados para Repositórios Recentes */
  repoHeaderRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  newRepoCard: {
    width: 220,
    backgroundColor: "#fff",
    borderRadius: 14,
    padding: 12,
    flexDirection: "row",
    alignItems: "center",
    elevation: 3,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 6,
    borderWidth: 1,
    borderColor: "#F1F5F9",
    position: "relative",
  },
  repoLeftIconContainer: {
    width: 44,
    height: 44,
    borderRadius: 10,
    backgroundColor: "#F8FAFC",
    justifyContent: "center",
    alignItems: "center",
  },
  repoTextContainer: {
    marginLeft: 12,
    flex: 1,
    justifyContent: "center",
  },
  newRepoTitle: { fontSize: 14, fontWeight: "700", color: "#111" },
  repoTag: {
    marginTop: 6,
    alignSelf: "flex-start",
    backgroundColor: "#EEF2FF",
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  repoTagText: { fontSize: 11, fontWeight: "700", color: "#5B21B6" },
  removeRecentBtn: {
    position: "absolute",
    top: 6,
    right: 6,
    width: 22,
    height: 22,
    borderRadius: 11,
    backgroundColor: "#F1F5F9",
    justifyContent: "center",
    alignItems: "center",
  },
});