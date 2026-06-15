import React, { useState, useEffect } from 'react';
import {
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator, // Adicionado para o carregamento
  Alert
} from 'react-native';
import Header from '../components/Header';
import BreadcrumbCard from '../components/BreadcrumbCard';
import { Feather } from '@expo/vector-icons';
import { COLORS } from "../components/Cores"; 
import styles from '../styles/Turma';
import BarraPesquisa from '../components/BarraPesquisa';

// URL Base limpa para buscar as turmas
const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

export default function TurmasScreen({ route, navigation }) { // 🌟 Adicionado 'route' aqui
  // Captura os dados enviados pela tela de Cursos (com um fallback seguro)
  const { cursoId, nomeCurso } = route.params || { cursoId: null, nomeCurso: "Curso" };

  const [turmas, setTurmas] = useState([]); // 📥 Armazena as turmas vindas do banco
  const [carregando, setCarregando] = useState(true);
  const [search, setSearch] = useState('');
  
  const [anoSelecionado, setAnoSelecionado] = useState(null); 
  const [turnoSelecionado, setTurnoSelecionado] = useState(null); 
  const [ordemAlfabetica, setOrdemAlfabetica] = useState(false); 

  // 🚀 Busca as turmas correspondentes ao curso assim que a tela abre
  useEffect(() => {
    if (cursoId) {
      buscarTurmas();
    }
  }, [cursoId]);

  const buscarTurmas = async () => {
    try {
      setCarregando(true);
      const urlCompleta = `${URL_BASE}/turmas?cursoId=${cursoId}`;
      console.log("Tentando conectar em:", urlCompleta);

      const resposta = await fetch(urlCompleta);
      const dados = await resposta.json(); // Lemos direto como JSON de forma segura
      
      console.log("================ SERVIDOR RESPONDEU (TURMAS) ================");
      console.log(dados);
      console.log("=============================================================");

      // 🌟 Só salva no estado se o servidor devolveu uma LISTA válida
      if (Array.isArray(dados)) {
        setTurmas(dados);
      } else {
        // Se o backend mandou um objeto de erro, exibe o motivo na tela!
        Alert.alert(
          "Erro no Banco de Dados", 
          `${dados.mensagem}\n\nDetalhe Técnico: ${dados.detalhe || 'Verifique os logs.'}`
        );
      }
    } catch (error) {
      console.error("Erro ao buscar turmas:", error);
      Alert.alert("Erro", "Não foi possível conectar ao servidor.");
    } finally {
      setCarregando(false);
    }
  };

  const irParaProjetos = (turma) => {
    navigation.navigate("Projetos", { turmaId: turma.idturma, codigoTurma: turma.codigo_turma });
  };

  // 1. Aplica os filtros (Ano e Turno) e também a Barra de Pesquisa (opcional por código do curso)
  let turmasExibidas = turmas.filter(turma => {
    const passaAno = anoSelecionado ? String(turma.ano) === String(anoSelecionado) : true;
    const passaTurno = turnoSelecionado ? turma.turno === turnoSelecionado : true;
    const passaPesquisa = search ? turma.codigo_turma.toLowerCase().includes(search.toLowerCase()) : true;
    return passaAno && passaTurno && passaPesquisa;
  });

  // 2. Aplica a ordenação alfabética pelo nome do professor
  if (ordemAlfabetica) {
    turmasExibidas = [...turmasExibidas].sort((a, b) => 
      (a.professor || '').localeCompare(b.professor || '')
    );
  }

  return (
    <View style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.dark} />
      
      <Header 
        foto={null} 
        escolherImagem={null} 
        nomeTela={"Turmas"} 
        temGoBack={true} 
        telaDestino={"Cursos"} // Retorna para a listagem de cursos
      />

      {/* SELEÇÃO DE FILTROS HORIZONTAIS */}
      <View style={styles.filtroContainer}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.filtroScroll}>
          
          <TouchableOpacity 
            style={[styles.chip, ordemAlfabetica && styles.chipAtivo]} 
            onPress={() => setOrdemAlfabetica(!ordemAlfabetica)}
          >
            <Feather name="sort-by-alpha" size={14} color={ordemAlfabetica ? '#FFF' : COLORS.primary} style={{ marginRight: 4 }} />
            <Text style={[styles.chipTexto, ordemAlfabetica && styles.chipTextoAtivo]}>A-Z</Text>
          </TouchableOpacity>

          <View style={styles.divisorFiltro} />

          {['2026', '2025', '2024'].map(ano => (
            <TouchableOpacity 
              key={ano}
              style={[styles.chip, anoSelecionado === ano && styles.chipAtivo]} 
              onPress={() => setAnoSelecionado(anoSelecionado === ano ? null : ano)}
            >
              <Text style={[styles.chipTexto, anoSelecionado === ano && styles.chipTextoAtivo]}>{ano}</Text>
            </TouchableOpacity>
          ))}

          <View style={styles.divisorFiltro} />

          {['Manhã', 'Tarde', 'Noite'].map(turno => (
            <TouchableOpacity 
              key={turno}
              style={[styles.chip, turnoSelecionado === turno && styles.chipAtivo]} 
              onPress={() => setTurnoSelecionado(turnoSelecionado === turno ? null : turno)}
            >
              <Text style={[styles.chipTexto, turnoSelecionado === turno && styles.chipTextoAtivo]}>{turno}</Text>
            </TouchableOpacity>
          ))}

        </ScrollView>
      </View>
      
      {/* 🌟 O Breadcrumb agora exibe dinamicamente o nome do curso clicado! */}
      <BreadcrumbCard titulo="Turmas:" itemSub={`Curso: ${nomeCurso}`} />

      <BarraPesquisa value={search} onChangeText={setSearch} />
      
      {carregando ? (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <ActivityIndicator size="large" color={COLORS.primary} />
          <Text style={{ marginTop: 10, color: COLORS.primary }}>Carregando turmas...</Text>
        </View>
      ) : (
        <ScrollView contentContainerStyle={styles.scrollContent}>
          {turmasExibidas.length === 0 ? (
            <Text style={styles.vazio}>Nenhuma turma corresponde aos filtros selecionados.</Text>
          ) : (
            turmasExibidas.map((turma) => (
              <TouchableOpacity 
                key={turma.idturma} 
                style={styles.turmaCard}
                onPress={() => irParaProjetos(turma)}
                activeOpacity={0.7}
              >
                <View style={styles.cardInfo}>
                  <View style={styles.iconCircle}>
                    <Feather name="users" size={18} color={COLORS.primary} />
                  </View>
                  
                  <View style={{ flex: 1 }}> 
                    {/* Exibe o nome do professor vindo do JOIN do banco */}
                    <Text style={styles.professorText}>{turma.professor || "Sem professor designado"}</Text>
                    
                    <View style={styles.subInfoContainer}>
                      <Text style={styles.turnoText}>{turma.turno}</Text>
                      <Text style={styles.divisor}>•</Text>
                      <Text style={styles.codigoText}>{turma.codigo_turma}</Text>
                      <Text style={styles.divisor}>•</Text>
                      <Text style={styles.codigoText}>{turma.ano}</Text>
                    </View>
                  </View>
                </View>

                <View style={styles.setaContainer}>
                  <Feather name="chevron-right" size={22} color={COLORS.primary} />
                </View>
              </TouchableOpacity>
            ))
          )}
        </ScrollView>
      )}
    </View>
  );
}