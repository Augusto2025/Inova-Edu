import React, { useState, useEffect, useRef } from "react";
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Modal, ScrollView, TouchableWithoutFeedback, ActivityIndicator, Alert } from "react-native";
import { Ionicons, Feather, MaterialIcons } from "@expo/vector-icons";
import Header from "../components/Header";
import Skeleton from '../components/Skeleton';
import BarraPesquisa from '../components/BarraPesquisa';
import { COLORS } from "../components/Cores";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { URL_BASE } from '../config/backend';

// Importação do hook
import { useTheme } from '../context/ThemeContext';

const URL_FORUM = `${URL_BASE}/forum`;
  
export default function ForumScreen({ navigation }) {
  // Consumindo o contexto
  const { theme, fontSizeScale } = useTheme();

  const [topicos, setTopicos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [modal, setModal] = useState({ visible: false, modo: "Criar", titulo: "", id: null });
  const [usuarioLogadoId, setUsuarioLogadoId] = useState(null);
  // 🆕 Sabe se quem está logado é Professor, pra liberar editar/apagar de qualquer fórum (moderação)
  const [ehModerador, setEhModerador] = useState(false);
  const [search, setSearch] = useState('');

  // 🆕 Modo de seleção múltipla, pra marcar vários fóruns e apagar de uma vez
  const [modoSelecao, setModoSelecao] = useState(false);
  const [selecionados, setSelecionados] = useState([]);
  const [apagandoSelecionados, setApagandoSelecionados] = useState(false);
  const [salvando, setSalvando] = useState(false);
  const salvandoRef = useRef(false);

  // 🆕 Filtro para mostrar só os fóruns que o usuário logado criou
  const [filtro, setFiltro] = useState('todos'); // 'todos' | 'meus'

  // ==========================================
  // 1. CARREGAR DADOS INICIAIS (GETS)
  // ==========================================
  const carregarTopicos = async () => {
    try {
      setCarregando(true);
      const response = await fetch(URL_FORUM); 
      
      if (!response.ok) {
        const textoErro = await response.text();
        throw new Error(`Status ${response.status}: ${textoErro || "Erro no servidor"}`);
      }
      
      const dados = await response.json();
      setTopicos(dados);
    } catch (error) {
      console.error("Erro ao carregar fórum:", error);
      Alert.alert("Erro de Conexão", `Não foi possível carregar o fórum.\n\nDetalhe: ${error.message}`);
    } finally {
      setCarregando(false);
    }
  };

  const obterUsuarioLogado = async () => {
    try {
      const idSalvo = await AsyncStorage.getItem('idUsuario'); 
      if (idSalvo !== null) {
        setUsuarioLogadoId(parseInt(idSalvo)); // 🌟 Define o ID real no estado do componente
      }

      // 🆕 Verifica o tipo salvo no login pra saber se é Professor (moderador)
      const tipo = await AsyncStorage.getItem('tipo');
      if (tipo) {
        setEhModerador(tipo.toLowerCase() === 'professor');
      }
    } catch (error) {
      console.error("Erro ao ler ID do usuário:", error);
    }
  };

  useEffect(() => {
    obterUsuarioLogado();
    carregarTopicos();
  }, []);

  // ==========================================
  // 2. SALVAR / EDITAR NO BACKEND (POST / PUT)
  // ==========================================
  const salvarTopico = async () => {
    if (salvandoRef.current) return;
    salvandoRef.current = true;
    setSalvando(true);

    try {
      if (!modal.titulo.trim()) return;

      if (modal.modo === "Criar") {
        // Criar Novo Fórum
        const response = await fetch(URL_FORUM, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            titulo: modal.titulo,
            usuarioId: usuarioLogadoId // 🌟 Enviando o ID real do AsyncStorage
          })
        });

        if (!response.ok) throw new Error("Erro ao criar o fórum no servidor.");
      } else {
        // Editar Fórum
        const response = await fetch(`${URL_FORUM}/${modal.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            titulo: modal.titulo,
            usuarioId: usuarioLogadoId // Enviando o ID real do AsyncStorage para o backend validar dono
          })
        });

        if (!response.ok) {
          if(response.status === 403) throw new Error("Você não tem permissão para editar este fórum.");
          throw new Error("Erro ao editar o fórum no servidor.");
        }
      }

      carregarTopicos();
      fecharModal();

    } catch (error) {
      console.error("Erro ao salvar:", error);
      Alert.alert("Ação Negada", error.message);
    } finally {
      salvandoRef.current = false;
      setSalvando(false);
    }
  };

  // ==========================================
  // 3. ELIMINAR DO BACKEND (DELETE) - individual
  // ==========================================
  const eliminarTopico = (id) => {
    Alert.alert(
      "Confirmar Exclusão",
      "Tem certeza que deseja apagar este fórum? Todos os tópicos dentro dele também serão apagados.",
      [
        { text: "Cancelar", style: "cancel" },
        { 
          text: "Apagar", 
          style: "destructive", 
          onPress: async () => {
            try {
              const response = await fetch(`${URL_FORUM}/${id}`, { 
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                  usuarioId: usuarioLogadoId // 🌟 Diz pro backend quem está tentando apagar
                })
              });

              if (!response.ok) {
                if(response.status === 403) throw new Error("Você não tem permissão para apagar este fórum.");
                throw new Error("Erro ao eliminar do servidor.");
              }
              
              setTopicos(topicos.filter(item => item.id !== id));
              Alert.alert("Sucesso", "Fórum e todos os seus tópicos foram excluídos com sucesso!");
            } catch (error) {
              console.error("Erro ao eliminar:", error);
              Alert.alert("Ação Negada", error.message);
            }
          }
        }
      ]
    );
  };

  // ==========================================
  // 3b. SELEÇÃO MÚLTIPLA
  // ==========================================
  const entrarModoSelecao = (idInicial) => {
    setModoSelecao(true);
    setSelecionados(idInicial ? [idInicial] : []);
  };

  const cancelarSelecao = () => {
    setModoSelecao(false);
    setSelecionados([]);
  };

  const alternarSelecionado = (item) => {
    const podeGerenciar = item.usuarioIdCriador === usuarioLogadoId || ehModerador;
    if (!podeGerenciar) {
      Alert.alert("Ação Negada", "Você não tem permissão para apagar este fórum.");
      return;
    }

    setSelecionados((atual) => {
      if (atual.includes(item.id)) {
        return atual.filter((id) => id !== item.id);
      }
      return [...atual, item.id];
    });
  };

  // 🆕 Aplica o filtro escolhido (Todos / Meus fóruns) antes de qualquer outra lógica de exibição
  const topicosFiltrados = (filtro === 'meus'
    ? topicos.filter((item) => item.usuarioIdCriador === usuarioLogadoId)
    : topicos
  ).filter((item) => {
    const termo = search.trim().toLowerCase();
    if (!termo) return true;

    const titulo = `${item.titulo || ''}`.toLowerCase();
    const descricao = `${item.descricao || ''}`.toLowerCase();
    const autor = `${item.autor || ''}`.toLowerCase();
    return titulo.includes(termo) || descricao.includes(termo) || autor.includes(termo);
  });

  // 🆕 Marca ou desmarca todos os fóruns visíveis (já filtrados) que o usuário pode gerenciar (dono ou moderador)
  const idsGerenciaveis = topicosFiltrados
    .filter((item) => item.usuarioIdCriador === usuarioLogadoId || ehModerador)
    .map((item) => item.id);

  const todosSelecionados = idsGerenciaveis.length > 0 && idsGerenciaveis.every((id) => selecionados.includes(id));

  const alternarSelecionarTodos = () => {
    if (todosSelecionados) {
      setSelecionados([]);
    } else {
      setSelecionados(idsGerenciaveis);
    }
  };

  const eliminarSelecionados = () => {
    if (selecionados.length === 0) return;

    Alert.alert(
      "Confirmar Exclusão",
      `Tem certeza que deseja apagar ${selecionados.length} fórum(ns)? Todos os tópicos dentro deles também serão apagados.`,
      [
        { text: "Cancelar", style: "cancel" },
        {
          text: "Apagar",
          style: "destructive",
          onPress: async () => {
            try {
              setApagandoSelecionados(true);

              const resultados = await Promise.allSettled(
                selecionados.map((id) =>
                  fetch(`${URL_FORUM}/${id}`, {
                    method: "DELETE",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ usuarioId: usuarioLogadoId }),
                  }).then((r) => {
                    if (!r.ok) throw new Error(`Falha ao apagar fórum ${id}`);
                    return id;
                  })
                )
              );

              const apagadosComSucesso = resultados
                .filter((r) => r.status === "fulfilled")
                .map((r) => r.value);
              const falhas = resultados.filter((r) => r.status === "rejected").length;

              setTopicos((atual) => atual.filter((item) => !apagadosComSucesso.includes(item.id)));
              cancelarSelecao();

              if (falhas > 0) {
                Alert.alert(
                  "Concluído com erros",
                  `${apagadosComSucesso.length} fórum(ns) apagado(s). ${falhas} não puderam ser apagados (permissão ou erro no servidor).`
                );
              } else {
                Alert.alert("Sucesso", `${apagadosComSucesso.length} fórum(ns) apagado(s) com sucesso!`);
              }
            } catch (error) {
              console.error("Erro ao apagar selecionados:", error);
              Alert.alert("Erro", "Não foi possível apagar os fóruns selecionados.");
            } finally {
              setApagandoSelecionados(false);
            }
          }
        }
      ]
    );
  };

  const fecharModal = () => setModal({ visible: false, modo: "Criar", titulo: "", id: null });

  return (
    <View style={[styles.container, { backgroundColor: theme.background }]}>
      <Header nomeTela={"Fórum"} temGoBack={true} carregando={carregando} />
      {/* 🆕 Filtro: Todos os fóruns ou só os que eu criei */}
      {!carregando && topicos.length > 0 && !modoSelecao && (
        <View style={styles.filtroRow}>
          <TouchableOpacity
            style={[styles.filtroBtn, filtro === 'todos' && { backgroundColor: COLORS.primary }]}
            onPress={() => setFiltro('todos')}
          >
            <Text style={[styles.filtroBtnTexto, filtro === 'todos' && styles.filtroBtnTextoAtivo, { fontSize: 13 * fontSizeScale }]}>
              Todos
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.filtroBtn, filtro === 'meus' && { backgroundColor: COLORS.primary }]}
            onPress={() => setFiltro('meus')}
          >
            <Text style={[styles.filtroBtnTexto, filtro === 'meus' && styles.filtroBtnTextoAtivo, { fontSize: 13 * fontSizeScale }]}>
              Meus fóruns
            </Text>
          </TouchableOpacity>
        </View>
      )}

      {/* 🆕 Barra de ações da seleção múltipla */}
      {!carregando && topicos.length > 0 && (
        <View style={styles.selecaoBarRow}>
          {modoSelecao ? (
            <>
              <Text style={[styles.selecaoContagem, { color: theme.text, fontSize: 13 * fontSizeScale }]}>
                {selecionados.length} selecionado(s)
              </Text>
              <View style={{ flexDirection: "row", gap: 16 }}>
                <TouchableOpacity onPress={alternarSelecionarTodos}>
                  <Text style={[styles.selecaoAcaoTexto, { fontSize: 13 * fontSizeScale }]}>
                    {todosSelecionados ? "Desmarcar todos" : "Selecionar todos"}
                  </Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={cancelarSelecao}>
                  <Text style={[styles.selecaoAcaoTexto, { fontSize: 13 * fontSizeScale }]}>Cancelar</Text>
                </TouchableOpacity>
              </View>
            </>
          ) : (
            <TouchableOpacity onPress={() => entrarModoSelecao(null)}>
              <Text style={[styles.selecaoAcaoTexto, { fontSize: 13 * fontSizeScale }]}>Selecionar fóruns</Text>
            </TouchableOpacity>
          )}
        </View>
      )}

      {carregando ? (
        <View style={{ flex: 1, padding: 20 }}>
          {[1, 2, 3].map((item) => (
            <Skeleton key={item} width="100%" height={90} borderRadius={16} style={{ marginBottom: 16 }} />
          ))}
        </View>
      ) : (
        <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: modoSelecao ? 90 : 0 }}>
          {topicosFiltrados.length === 0 ? (
            <View style={{ marginTop: 40, alignItems: 'center', paddingHorizontal: 20 }}>
              <Text style={{ color: theme.text, opacity: 0.6, textAlign: 'center', fontSize: 13 * fontSizeScale }}>
                Nenhum fórum encontrado.
              </Text>
            </View>
          ) : topicosFiltrados.map((item) => {
            // 🆕 Mostra editar/apagar se for o dono OU se for professor (moderador)
            const podeGerenciar = item.usuarioIdCriador === usuarioLogadoId || ehModerador;
            const estaSelecionado = selecionados.includes(item.id);

            return (
              <TouchableOpacity 
                key={item.id} 
                // Card usa cor do tema (card)
                style={[styles.card, { backgroundColor: theme.card }, modoSelecao && estaSelecionado && { borderWidth: 2, borderColor: COLORS.primary }]} 
                activeOpacity={0.8}
                onPress={() => {
                  if (modoSelecao) {
                    alternarSelecionado(item);
                  } else {
                    navigation.navigate("Titulo", { topico: item });
                  }
                }}
                onLongPress={() => {
                  if (!modoSelecao) entrarModoSelecao(item.id);
                }}
              >
                {/* 🆕 Checkbox de seleção, só quando o modo seleção está ativo */}
                {modoSelecao && (
                  <View style={styles.checkboxWrap}>
                    <Ionicons 
                      name={estaSelecionado ? "checkmark-circle" : "ellipse-outline"} 
                      size={22} 
                      color={podeGerenciar ? (estaSelecionado ? COLORS.primary : "#94A3B8") : "#CBD5E1"} 
                    />
                  </View>
                )}

                <View style={[styles.iconBox, { backgroundColor: item.cor }]}><Ionicons name="chatbubble-ellipses" size={22} color="#fff" /></View>
                <View style={styles.content}>
                  <View style={styles.topRow}>
                    {/* Fonte escalável e cor do texto do tema */}
                    <Text style={[styles.title, { color: theme.text, fontSize: 15 * fontSizeScale }]} numberOfLines={1}>{item.titulo}</Text>
                    <Text style={[styles.time, { fontSize: 11 * fontSizeScale }]}>{item.tempo}</Text>
                  </View>
                  <Text style={[styles.description, { color: theme.text, fontSize: 13 * fontSizeScale }]} numberOfLines={2}>{item.descricao}</Text>
                  
                  <View style={styles.footer}>
                    <View style={styles.footerLeft}>
                      <View style={styles.info}>
                        <Ionicons name="person-outline" size={13} color={theme.text} />
                        <Text style={[styles.infoText, { color: theme.text, fontSize: 11 * fontSizeScale }]} numberOfLines={1}>
                          {item.autor}
                        </Text>
                      </View>
                    </View>

                    {!modoSelecao && podeGerenciar && (
                      <View style={styles.actions}>
                        <TouchableOpacity style={styles.editButton} onPress={() => setModal({ visible: true, modo: "Editar", titulo: item.titulo, id: item.id })}><Feather name="edit-2" size={16} color="#5B5EF7" /></TouchableOpacity>
                        <TouchableOpacity style={styles.deleteButton} onPress={() => eliminarTopico(item.id)}><MaterialIcons name="delete-outline" size={18} color="#FF6B6B" /></TouchableOpacity>
                      </View>
                    )}
                  </View>
                </View>
              </TouchableOpacity>
            );
          })}
        </ScrollView>
      )}

      {/* 🆕 Barra fixa embaixo com a ação de apagar selecionados */}
      {modoSelecao && selecionados.length > 0 && (
        <View style={[styles.barraInferior, { backgroundColor: theme.card, borderTopColor: theme.border }]}>
          <TouchableOpacity 
            style={[styles.apagarSelecionadosBtn, apagandoSelecionados && { opacity: 0.6 }]} 
            onPress={eliminarSelecionados}
            disabled={apagandoSelecionados}
          >
            {apagandoSelecionados ? (
              <ActivityIndicator size="small" color="#fff" />
            ) : (
              <>
                <MaterialIcons name="delete-outline" size={20} color="#fff" />
                <Text style={styles.apagarSelecionadosTexto}>Apagar {selecionados.length} selecionado(s)</Text>
              </>
            )}
          </TouchableOpacity>
        </View>
      )}

      {!modoSelecao && (
        <TouchableOpacity style={styles.fab} onPress={() => setModal({ visible: true, modo: "Criar", titulo: "", id: null })}><Ionicons name="add" size={28} color="#fff" /></TouchableOpacity>
      )}

      {/* MODAL DE CRIAÇÃO / EDIÇÃO */}
      <Modal visible={modal.visible} transparent animationType="fade" onRequestClose={fecharModal}>
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={fecharModal}>
          <TouchableWithoutFeedback>
            {/* Fundo do modal usa theme.card */}
            <View style={[styles.modalContent, { backgroundColor: theme.card }]}>
              
              <View style={styles.modalHeader}>
                <Text style={[styles.modalTitle, { fontSize: 18 * fontSizeScale }]}>{modal.modo === "Criar" ? "Criar Fórum" : "Editar Fórum"}</Text>
                <TouchableOpacity onPress={fecharModal} style={{ position: 'absolute', right: 20 }}>
                  <Feather name="x" size={20} color="white" />
                </TouchableOpacity>
              </View>

              <View style={styles.modalBody}>
                <View style={styles.inputContainer}>
                  <Text style={[styles.inputLabel, { color: theme.text, fontSize: 14 * fontSizeScale }]}>Título do Fórum</Text>
                  {/* TextInput adaptado */}
                  <TextInput 
                    placeholder="Digite o título..." 
                    placeholderTextColor={theme.text + '80'}
                    value={modal.titulo} 
                    onChangeText={(t) => setModal({ ...modal, titulo: t })} 
                    style={[styles.input, { backgroundColor: theme.background, color: theme.text, borderColor: theme.border, fontSize: 16 * fontSizeScale }]} 
                  />
                </View>

                <TouchableOpacity style={[styles.saveBtn, salvando && { opacity: 0.6 }]} onPress={salvarTopico} disabled={salvando}>
                  {salvando ? <ActivityIndicator color="#fff" /> : <Text style={styles.saveBtnText}>{modal.modo === "Criar" ? "Criar" : "Salvar"}</Text>}
                </TouchableOpacity>
              </View>
            </View>
          </TouchableWithoutFeedback>
        </TouchableOpacity>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#ffffff" },
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
  card: { backgroundColor: "#fff", marginHorizontal: 12, marginBottom: 12, borderRadius: 16, padding: 14, flexDirection: "row", elevation: 2 },
  iconBox: { width: 42, height: 42, borderRadius: 21, justifyContent: "center", alignItems: "center", marginRight: 12 },
  content: { flex: 1 },
  topRow: { flexDirection: "row", justifyContent: "space-between" },
  title: { flex: 1, fontSize: 15, fontWeight: "700", color: "#222" },
  time: { fontSize: 11, color: "#888" },
  description: { fontSize: 13, color: "#555", marginTop: 4, lineHeight: 18 },
  footer: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginTop: 10 },
  footerLeft: { flexDirection: "row", flex: 1, marginRight: 8, alignItems: 'center' }, 
  info: { flexDirection: "row", alignItems: "center", marginRight: 10, maxWidth: 90 }, 
  infoText: { marginLeft: 4, color: "#777", fontSize: 11 },
  actions: { flexDirection: "row" },
  editButton: { marginRight: 10, padding: 4 },
  deleteButton: { padding: 4 },
  fab: { position: "absolute", bottom: 20, right: 20, width: 56, height: 56, borderRadius: 28, backgroundColor: "#ff8c00", justifyContent: "center", alignItems: "center", elevation: 4 },

  // 🆕 Estilos do filtro Todos / Meus fóruns
  filtroRow: {
    flexDirection: "row",
    gap: 10,
    paddingHorizontal: 16,
    paddingTop: 10,
  },
  filtroBtn: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: "#EEF2FF",
  },
  filtroBtnTexto: { color: COLORS.primary, fontWeight: "600" },
  filtroBtnTextoAtivo: { color: "#fff" },

  // 🆕 Estilos da seleção múltipla
  selecaoBarRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  selecaoContagem: { fontWeight: "600" },
  selecaoAcaoTexto: { color: COLORS.primary, fontWeight: "700" },
  checkboxWrap: { justifyContent: "center", alignItems: "center", marginRight: 10 },
  barraInferior: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 0,
    padding: 14,
    borderTopWidth: 1,
  },
  apagarSelecionadosBtn: {
    backgroundColor: "#FF6B6B",
    borderRadius: 14,
    paddingVertical: 14,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: 8,
  },
  apagarSelecionadosTexto: { color: "#fff", fontWeight: "700", fontSize: 14 },
  
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0, 0, 0, 0.67)', justifyContent: 'center', padding: 15 },
  modalContent: { backgroundColor: 'white', borderRadius: 25, overflow: 'hidden' },
  modalHeader: { backgroundColor: COLORS.primary, flexDirection: 'row', padding: 20, alignItems: 'center', justifyContent: 'center' },
  modalTitle: { color: 'white', fontSize: 18, fontWeight: 'bold' },
  modalBody: { padding: 20 },
  inputContainer: { marginBottom: 15 },
  inputLabel: { fontSize: 14, fontWeight: "600", color: "#333", marginBottom: 6, paddingLeft: 2 },
  input: { borderWidth: 1, borderColor: '#ddd', borderRadius: 12, padding: 12 },
  saveBtn: { backgroundColor: COLORS.primary, padding: 15, borderRadius: 12, alignItems: 'center', marginTop: 10 },
  saveBtnText: { color: 'white', fontWeight: 'bold' }
});
