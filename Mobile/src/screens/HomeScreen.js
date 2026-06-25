import React, { useState, useEffect, useRef } from "react";
import Header from "../components/Header";
import Skeleton from "../components/Skeleton"; 
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

  const [quantidadeNotif, setQuantidadeNotif] = useState(3);
  const [busca, setBusca] = useState("");
  const [totalMensagensForum, setTotalMensagensForum] = useState(3);

  // ESTADOS CONECTADOS AO BACKEND
  const [carregando, setCarregando] = useState(true);
  const [events, setEvents] = useState([]);
  const [categoriasCursos, setCategoriasCursos] = useState([]);
  const [recentesAcessados, setRecentesAcessados] = useState([]);

  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.15, duration: 800, useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 800, useNativeDriver: true }),
      ])
    ).start();
  }, [pulseAnim]);

  // BUSCA DOS DADOS NO BACKEND
  useEffect(() => {
    async function puxarDadosDoServidor() {
      try {
        setCarregando(true);
        
        const ipBackend = process.env.EXPO_PUBLIC_URL_BACKEND || 'http://10.0.60.213:3000';
        const urlLimpa = ipBackend.replace('/login', '');
        
        const [resEventos, resCursos] = await Promise.all([
          fetch(`${urlLimpa}/eventos`),
          fetch(`${urlLimpa}/cursos`)
        ]);

        if (!resEventos.ok) console.warn(`Rota /eventos retornou status: ${resEventos.status}`);
        if (!resCursos.ok) console.warn(`Rota /cursos retornou status: ${resCursos.status}`);

        const dadosEventos = resEventos.ok ? await resEventos.json() : [];
        const dadosCursos = resCursos.ok ? await resCursos.json() : [];
        
        console.log("👉 ESTRUTURA RECEBIDA DE /CURSOS:", JSON.stringify(dadosCursos, null, 2));

        setEvents(dadosEventos);
        setCategoriasCursos(dadosCursos);
        setRecentesAcessados([]);
        
      } catch (error) {
        console.error("❌ Erro ao buscar dados da Home com Fetch local:", error.message);
      } finally {
        setCarregando(false); 
      }
    }

    puxarDadosDoServidor();
  }, []);

  const getEventStatusColor = (eventDate) => {
    if (!eventDate) return '#4CAF50';
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const evDate = new Date(eventDate);
    evDate.setHours(0, 0, 0, 0);

    if (evDate.getTime() === today.getTime()) return '#FFD700';
    return evDate > today ? '#4CAF50' : '#F44336';
  };

  const irParaRepositorio = (projeto) => {
    const idDoProjeto = projeto.idprojeto || projeto.id;
    const nomeDoProjeto = projeto.nome_projeto || projeto.titulo;

    setRecentesAcessados((listaAntiga) => {
      const listaFiltrada = listaAntiga.filter((item) => (item.idprojeto || item.id) !== idDoProjeto);
      return [projeto, ...listaFiltrada];
    });

    navigation.navigate("Repositorio", { 
      projetoId: idDoProjeto, 
      projetoNome: nomeDoProjeto 
    });
  };

  const removerDosRecentes = (id) => {
    setRecentesAcessados((listaAntiga) => listaAntiga.filter((item) => (item.idprojeto || item.id) !== id));
  };

  // 🌟 FILTRO ULTRA-FLEXÍVEL: Busca profunda por Curso, Turma ou Projeto
  const filtrarResultados = () => {
    if (!busca || busca.trim() === "") {
      return [];
    }

    let resultados = [];
    if (!categoriasCursos || !Array.isArray(categoriasCursos)) return [];

    const termo = busca.toLowerCase().trim();

    categoriasCursos.forEach(item => {
      // Captura possíveis variações de nomes para Curso e Turma no objeto principal
      const nomeDoCurso = (item.nomeCurso || item.nome_curso || item.nome || item.curso || "").toLowerCase();
      const nomeDaTurma = (item.turma || item.nome_turma || item.sigla_turma || item.turma_nome || "").toLowerCase();
      
      // Captura a lista interna de sub-projetos
      const listaDeProjetos = item.projetos || item.Projetos || item.repositorios || item.Repositorios || item.projeto || item.Projeto;

      if (Array.isArray(listaDeProjetos) && listaDeProjetos.length > 0) {
        // CASO A: Estrutura aninhada clássica (Curso/Turma -> [Projetos])
        listaDeProjetos.forEach(p => {
          if (!p) return;

          const nomeDoProjeto = (p.nome_projeto || p.titulo || p.nome || p.nomeProjeto || "").toLowerCase();

          // Regra: Se o termo bate com o Curso OU com a Turma OU com o Projeto, empurra o PROJETO estruturado
          if (
            nomeDoProjeto.includes(termo) || 
            nomeDoCurso.includes(termo) || 
            nomeDaTurma.includes(termo)
          ) {
            resultados.push({
              ...p,
              idprojeto: p.idprojeto || p.id || String(Math.random()),
              nome_projeto: p.nome_projeto || p.titulo || p.nome || p.nomeProjeto || "Projeto sem título",
              imagem: p.imagem || p.capa || p.url_imagem || null,
              origem: item.nomeCurso || item.nome || item.nome_curso || "Curso"
            });
          }
        });
      } else if (!listaDeProjetos) {
        // CASO B: O item principal da raiz já é o próprio projeto isolado
        const nomeDoProjeto = (item.nome_projeto || item.titulo || item.nome || item.nomeProjeto || "").toLowerCase();
        
        if (
          nomeDoProjeto.includes(termo) || 
          nomeDoCurso.includes(termo) || 
          nomeDaTurma.includes(termo)
        ) {
          resultados.push({
            ...item,
            idprojeto: item.idprojeto || item.id || String(Math.random()),
            nome_projeto: item.nome_projeto || item.titulo || item.nome || item.nomeProjeto || "Projeto sem título",
            imagem: item.imagem || item.capa || item.url_imagem || null,
            origem: item.nomeCurso || item.nome || "Repositório"
          });
        }
      }
    });

    return resultados;
  };

  const resultadosDaBusca = filtrarResultados();

  return (
    <View style={styles.safe}>
      <Header 
        nomeTela="Olá, Alcides 👋" 
        exibirPerfil={true} 
        quantidadeNotificacoes={quantidadeNotif}
        aoClicarNoSino={() => setQuantidadeNotif(0)}
        carregando={carregando} 
      />

      <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        
        {/* 1. PRÓXIMOS EVENTOS */}
        <Text style={styles.sectionTitle}>Próximos eventos</Text>

        {carregando ? (
          [1, 2, 3].map((key) => (
            <View key={key} style={[styles.eventCard, { gap: 14 }]}>
              <Skeleton width={52} height={56} borderRadius={10} />
              <View style={{ flex: 1, gap: 8 }}>
                <Skeleton width="75%" height={16} borderRadius={4} />
                <Skeleton width="45%" height={12} borderRadius={4} />
              </View>
            </View>
          ))
        ) : events.length > 0 ? (
          events.map((event) => {
            const dataBanco = event.data || event.date;
            const mesesAbv = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"];
            
            let diaExibicao = "•";
            let mesExibicao = "EVT";

            if (dataBanco) {
              const dataObj = new Date(dataBanco);
              diaExibicao = dataObj.getUTCDate();
              mesExibicao = mesesAbv[dataObj.getUTCMonth()];
            }

            const statusColor = getEventStatusColor(dataBanco);

            return (
              <TouchableOpacity 
                key={event.id || event.idevento} 
                style={styles.eventCard} 
                activeOpacity={0.8}
                onPress={() => navigation.navigate("Eventos", { selectedDate: dataBanco })}
              >
                <View style={[styles.dateBadge, { borderColor: statusColor }]}>
                  <View style={[styles.dateBadgeTop, { backgroundColor: statusColor }]}>
                    <Text style={styles.monthText}>{mesExibicao}</Text>
                  </View>
                  <View style={styles.dateBadgeBottom}>
                    <Text style={[styles.dayText, { color: '#333' }]}>{diaExibicao}</Text>
                  </View>
                </View>
                
                <View style={styles.eventInfo}>
                  <Text style={styles.eventTitle}>{event.titulo || event.title || "Sem título"}</Text>
                  <Text style={styles.eventTimeInfo}>
                    <Ionicons name="time-outline" size={13} color="#777" /> {event.horario || event.time || "Dia todo"} • {event.local || "InovaEdu"}
                  </Text>
                </View>
                <View style={[styles.statusDot, { backgroundColor: statusColor }]} />
              </TouchableOpacity>
            );
          })
        ) : (
          <Text style={styles.emptyText}>Nenhum evento agendado no banco.</Text>
        )}

        {/* 2. MEUS REPOSITÓRIOS COM BUSCADOR INTEGRADO */}
        {carregando ? (
          <View style={styles.searchContainer}>
            <Skeleton width={160} height={22} borderRadius={4} style={{ marginBottom: 15 }} />
            <Skeleton width="100%" height={50} borderRadius={18} />
          </View>
        ) : (
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

            <View style={{ marginTop: 15 }}>
              <Text style={{ fontSize: 12, color: '#888', marginBottom: 8 }}>
                {busca.trim() !== "" ? `${resultadosDaBusca.length} encontrados:` : "Digite para buscar um repositório:"}
              </Text>
              <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 12, paddingBottom: 5 }}>
                {resultadosDaBusca.length > 0 ? (
                  resultadosDaBusca.map((item) => (
                    <TouchableOpacity 
                      key={item.idprojeto || item.id} 
                      style={styles.miniResultCard}
                      onPress={() => irParaRepositorio(item)}
                    >
                      {item.imagem || item.capa ? (
                        <Image source={{ uri: item.imagem || item.capa }} style={styles.miniResultImg} />
                      ) : (
                        <View style={[styles.miniResultImg, { backgroundColor: '#eee', justifyContent: 'center', alignItems: 'center' }]}>
                          <Feather name="folder" size={20} color={COLORS.primary} />
                        </View>
                      )}
                      <Text numberOfLines={1} style={styles.miniResultText}>{item.nome_projeto || item.titulo || "Projeto"}</Text>
                      <View style={styles.miniBadge}><Text style={styles.miniBadgeText}>{item.origem}</Text></View>
                    </TouchableOpacity>
                  ))
                ) : busca.trim() !== "" ? (
                  <Text style={{ color: '#999', fontSize: 13, fontStyle: 'italic' }}>Nenhum repositório encontrado para "{busca}"</Text>
                ) : null}
              </ScrollView>
            </View>
          </View>
        )}

        {/* 3. FÓRUM ATIVO */}
        <Text style={styles.sectionTitle}>Fórum ativo</Text>
        <TouchableOpacity style={styles.forumContainerCard} activeOpacity={0.8} onPress={() => navigation.navigate("Forum")}>
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
        
        {carregando ? (
          <View style={{ flexDirection: 'row', gap: 14, paddingBottom: 15 }}>
            {[1, 2].map((key) => (
              <View key={key} style={{ gap: 8 }}>
                <Skeleton width={140} height={100} borderRadius={20} />
                <Skeleton width={100} height={14} borderRadius={4} style={{ alignSelf: 'center' }} />
              </View>
            ))}
          </View>
        ) : recentesAcessados && recentesAcessados.length > 0 ? (
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.horizontalRepoContainer}>
            {recentesAcessados.map((projeto) => {
              const idProj = projeto.idprojeto || projeto.id;
              return (
                <TouchableOpacity 
                  key={idProj}
                  style={styles.repoSquareCard} 
                  activeOpacity={0.8}
                  onPress={() => irParaRepositorio(projeto)} 
                >
                  <View style={styles.imageWrapper}>
                    {projeto?.imagem || projeto?.capa ? (
                      <Image source={{ uri: projeto?.imagem || projeto?.capa }} style={styles.repoCoverImage} />
                    ) : (
                      <View style={[styles.repoCoverImage, { backgroundColor: '#ececec', justifyContent: 'center', alignItems: 'center' }]}>
                        <Feather name="folder" size={24} color={COLORS.primary} />
                      </View>
                    )}
                    <TouchableOpacity 
                      style={styles.removeButton} 
                      activeOpacity={0.7}
                      onPress={() => removerDosRecentes(idProj)}
                    >
                      <Ionicons name="close" size={14} color="#FFF" />
                    </TouchableOpacity>
                  </View>
                  <View style={styles.repoContentArea}>
                    <Text style={styles.repoMainTitle} numberOfLines={2}>{projeto.nome_projeto || projeto.titulo}</Text>
                  </View>
                </TouchableOpacity>
              );
            })}
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

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#1459b3" },
  container: { flex: 1, backgroundColor: '#FFFFFF' },
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
  emptyRecentsText: { color: '#888', fontSize: 12, fontWeight: '500' },
  emptyText: { color: '#888', fontStyle: 'italic', marginVertical: 10, textAlign: 'center' }
});