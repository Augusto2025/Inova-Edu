import React, { useState, useEffect } from 'react';
import {
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator,
  Alert,
  BackHandler // 🌟 Reimportado para controlar o botão físico do Android
} from 'react-native';
import Header from '../components/Header';
import BreadcrumbCard from '../components/BreadcrumbCard';
import { Feather } from '@expo/vector-icons';
import { COLORS } from "../components/Cores"; 
import styles from '../styles/Turma';
import BarraPesquisa from '../components/BarraPesquisa';

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

export default function TurmasScreen({ route, navigation }) {
  const { cursoId, nomeCurso } = route.params || { cursoId: null, nomeCurso: "Curso" };

  const [turmas, setTurmas] = useState([]); 
  const [carregando, setCarregando] = useState(true);
  const [search, setSearch] = useState('');
  
  const [anoSelecionado, setAnoSelecionado] = useState(null); 
  const [turnoSelecionado, setTurnoSelecionado] = useState(null); 
  const [ordemAlfabetica, setOrdemAlfabetica] = useState(false); 

  // 🌟 FUNÇÃO DE VOLTAR CORRIGIDA: Usa goBack() para evitar o erro JUMP_TO de abas aninhadas
  const lidarComVoltar = () => {
    if (navigation.canGoBack()) {
      navigation.goBack(); // Desempilha a tela atual e revela a anterior sem forçar rotas por nome
    } else {
      navigation.navigate("Home"); // Fallback seguro
    }
  };

  // 🌟 Controla o comportamento do botão físico do Android
  useEffect(() => {
    const acaoBotaoVoltar = () => {
      lidarComVoltar();
      return true; 
    };

    const backHandler = BackHandler.addEventListener(
      'hardwareBackPress',
      acaoBotaoVoltar
    );

    return () => backHandler.remove(); 
  }, [navigation]);

  useEffect(() => {
    if (cursoId) {
      buscarTurmas();
    }
  }, [cursoId]);

  const buscarTurmas = async () => {
    try {
      setCarregando(true);
      const urlCompleta = `${URL_BASE}/turmas?cursoId=${cursoId}`;
      const resposta = await fetch(urlCompleta);
      const dados = await resposta.json();
      
      if (Array.isArray(dados)) {
        setTurmas(dados);
      } else {
        Alert.alert(
          "Erro no Banco de Dados", 
          `${dados.mensagem}\n\nDetalhe Técnico: ${dados.detalhe || 'Verifique os logs.'}`
        );
      }
    } catch (error) {
      Alert.alert("Erro", "Não foi possível conectar ao servidor.");
    } finally {
      setCarregando(false);
    }
  };

  const irParaProjetos = (turma) => {
    navigation.navigate("Projetos", { turmaId: turma.idturma, codigoTurma: turma.codigo_turma });
  };

  let turmasExibidas = turmas.filter(turma => {
    const passaAno = anoSelecionado ? String(turma.ano) === String(anoSelecionado) : true;
    const passaTurno = turnoSelecionado ? turma.turno === turnoSelecionado : true;
    const passaPesquisa = search ? turma.codigo_turma.toLowerCase().includes(search.toLowerCase()) : true;
    return passaAno && passaTurno && passaPesquisa;
  });

  if (ordemAlfabetica) {
    turmasExibidas = [...turmasExibidas].sort((a, b) => 
      (a.professor || '').localeCompare(b.professor || '')
    );
  }

  return (
    <View style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.dark} />
      
      {/* 🌟 CORRIGIDO: Removido 'telaDestino' e adicionado 'onPressBack' chamando a função com goBack() */}
      <Header 
        foto={null} 
        escolherImagem={null} 
        nomeTela={"Turmas"} 
        temGoBack={true} 
        onPressBack={lidarComVoltar}
      />

      {/* 🌟 NOVO DESIGN DE FILTROS: Clean, moderno e espaçado */}
      <View style={{ paddingVertical: 12, backgroundColor: '#FFF', borderBottomWidth: 1, borderBottomColor: '#F2F2F2' }}>
        <ScrollView 
          horizontal 
          showsHorizontalScrollIndicator={false} 
          contentContainerStyle={{ paddingHorizontal: 16, alignItems: 'center', gap: 8 }}
        >
          {/* Botão de Ordenação Inteligente */}
          <TouchableOpacity 
            style={[
              styles.chip, 
              ordemAlfabetica && styles.chipAtivo,
              { flexDirection: 'row', alignItems: 'center', borderRadius: 20, paddingHorizontal: 14, paddingVertical: 6 }
            ]} 
            onPress={() => setOrdemAlfabetica(!ordemAlfabetica)}
          >
            <Feather 
              name="sliders" 
              size={14} 
              color={ordemAlfabetica ? '#FFF' : COLORS.primary} 
              style={{ marginRight: 6 }} 
            />
            <Text style={[styles.chipTexto, ordemAlfabetica && styles.chipTextoAtivo, { fontWeight: '600' }]}>
              {ordemAlfabetica ? 'A-Z Ativo' : 'Ordenar A-Z'}
            </Text>
          </TouchableOpacity>

          {/* Filtros Dinâmicos de Ano */}
          {['2026', '2025', '2024'].map(ano => (
            <TouchableOpacity 
              key={ano}
              style={[
                styles.chip, 
                anoSelecionado === ano && styles.chipAtivo,
                { borderRadius: 20, paddingHorizontal: 14, paddingVertical: 6 }
              ]} 
              onPress={() => setAnoSelecionado(anoSelecionado === ano ? null : ano)}
            >
              <Text style={[styles.chipTexto, anoSelecionado === ano && styles.chipTextoAtivo, { fontWeight: '500' }]}>
                {anoSelecionado === ano ? `Ano: ${ano}` : ano}
              </Text>
            </TouchableOpacity>
          ))}

          {/* Filtros Dinâmicos de Turno */}
          {['Manhã', 'Tarde', 'Noite'].map(turno => (
            <TouchableOpacity 
              key={turno}
              style={[
                styles.chip, 
                turnoSelecionado === turno && styles.chipAtivo,
                { borderRadius: 20, paddingHorizontal: 14, paddingVertical: 6 }
              ]} 
              onPress={() => setTurnoSelecionado(turnoSelecionado === turno ? null : turno)}
            >
              <Text style={[styles.chipTexto, turnoSelecionado === turno && styles.chipTextoAtivo, { fontWeight: '500' }]}>
                {turnoSelecionado === turno ? `Turno: ${turno}` : turno}
              </Text>
            </TouchableOpacity>
          ))}

        </ScrollView>
      </View>
      
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