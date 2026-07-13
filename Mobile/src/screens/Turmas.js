import React, { useState, useContext, useCallback } from 'react';
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
import { useFocusEffect } from '@react-navigation/native'; // 1. Hook de recarregamento
import Header from '../components/Header';
import BreadcrumbCard from '../components/BreadcrumbCard';
import { Feather } from '@expo/vector-icons';
import { COLORS } from "../components/Cores"; 
import styles from '../styles/Turma';
import BarraPesquisa from '../components/BarraPesquisa';

// 2. Importação do Contexto de Tema e Acessibilidade
import { ThemeContext } from '../context/ThemeContext';

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

export default function TurmasScreen({ route, navigation }) {
  // Puxando as variáveis globais
  const { theme, fontSizeScale } = useContext(ThemeContext);

  const { cursoId, nomeCurso } = route.params || { cursoId: null, nomeCurso: "Curso" };

  const [turmas, setTurmas] = useState([]); 
  const [carregando, setCarregando] = useState(true);
  const [search, setSearch] = useState('');
  
  const [anoSelecionado, setAnoSelecionado] = useState(null); 
  const [turnoSelecionado, setTurnoSelecionado] = useState(null); 
  const [ordemAlfabetica, setOrdemAlfabetica] = useState(false); 

  // 3. Transformando em useCallback para o useFocusEffect
  const buscarTurmas = useCallback(async () => {
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
  }, [cursoId]);

  // 4. Executa a busca toda vez que a tela ganha foco
  useFocusEffect(
    useCallback(() => {
      if (cursoId) {
        buscarTurmas();
      }
    }, [buscarTurmas, cursoId])
  );

  const irParaProjetos = (turma) => {
    navigation.navigate("Projetos", { turmaId: turma.idturma, codigoTurma: turma.codigo_turma });
  };

  const lidarComVoltar = () => {
    navigation.goBack();
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
    // Fundo dinâmico da tela
    <View style={[styles.safeArea, { backgroundColor: theme.background }]}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.dark} />
      
      {/* 🌟 CORRIGIDO: Removido 'telaDestino' e adicionado 'onPressBack' chamando a função com goBack() */}
      <Header 
        foto={null} 
        escolherImagem={null} 
        nomeTela={"Turmas"} 
        temGoBack={true} 
        onPressBack={lidarComVoltar}
      />

      {/* Container de Filtros com cores dinâmicas */}
      <View style={{ paddingVertical: 12, backgroundColor: theme.card, borderBottomWidth: 1, borderBottomColor: theme.border }}>
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
              { 
                flexDirection: 'row', 
                alignItems: 'center', 
                borderRadius: 20, 
                paddingHorizontal: 14, 
                paddingVertical: 6,
                backgroundColor: ordemAlfabetica ? COLORS.primary : theme.background,
                borderColor: ordemAlfabetica ? COLORS.primary : theme.border,
                borderWidth: 1
              }
            ]} 
            onPress={() => setOrdemAlfabetica(!ordemAlfabetica)}
          >
            <Feather 
              name="sliders" 
              size={14 * fontSizeScale} 
              color={ordemAlfabetica ? '#FFF' : theme.text} 
              style={{ marginRight: 6 }} 
            />
            <Text style={[
              styles.chipTexto, 
              { 
                fontWeight: '600', 
                color: ordemAlfabetica ? '#FFF' : theme.text,
                fontSize: 14 * fontSizeScale 
              }
            ]}>
              {ordemAlfabetica ? 'A-Z Ativo' : 'Ordenar A-Z'}
            </Text>
          </TouchableOpacity>

          {/* Filtros Dinâmicos de Ano */}
          {['2026', '2025', '2024'].map(ano => (
            <TouchableOpacity 
              key={ano}
              style={[
                styles.chip, 
                { 
                  borderRadius: 20, 
                  paddingHorizontal: 14, 
                  paddingVertical: 6,
                  backgroundColor: anoSelecionado === ano ? COLORS.primary : theme.background,
                  borderColor: anoSelecionado === ano ? COLORS.primary : theme.border,
                  borderWidth: 1
                }
              ]} 
              onPress={() => setAnoSelecionado(anoSelecionado === ano ? null : ano)}
            >
              <Text style={[
                styles.chipTexto, 
                { 
                  fontWeight: '500',
                  color: anoSelecionado === ano ? '#FFF' : theme.text,
                  fontSize: 14 * fontSizeScale
                }
              ]}>
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
                { 
                  borderRadius: 20, 
                  paddingHorizontal: 14, 
                  paddingVertical: 6,
                  backgroundColor: turnoSelecionado === turno ? COLORS.primary : theme.background,
                  borderColor: turnoSelecionado === turno ? COLORS.primary : theme.border,
                  borderWidth: 1
                }
              ]} 
              onPress={() => setTurnoSelecionado(turnoSelecionado === turno ? null : turno)}
            >
              <Text style={[
                styles.chipTexto, 
                { 
                  fontWeight: '500',
                  color: turnoSelecionado === turno ? '#FFF' : theme.text,
                  fontSize: 14 * fontSizeScale
                }
              ]}>
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
          <Text style={{ marginTop: 10, color: theme.text, fontSize: 14 * fontSizeScale }}>
            Carregando turmas...
          </Text>
        </View>
      ) : (
        <ScrollView contentContainerStyle={styles.scrollContent}>
          {turmasExibidas.length === 0 ? (
            <Text style={[styles.vazio, { color: theme.text, fontSize: 16 * fontSizeScale }]}>
              Nenhuma turma corresponde aos filtros selecionados.
            </Text>
          ) : (
            turmasExibidas.map((turma) => (
              <TouchableOpacity 
                key={turma.idturma} 
                style={[styles.turmaCard, { backgroundColor: theme.card, borderColor: theme.border, borderWidth: 1 }]}
                onPress={() => irParaProjetos(turma)}
                activeOpacity={0.7}
              >
                <View style={styles.cardInfo}>
                  <View style={styles.iconCircle}>
                    <Feather name="users" size={18 * fontSizeScale} color={COLORS.primary} />
                  </View>
                  
                  <View style={{ flex: 1 }}> 
                    <Text style={[styles.professorText, { color: theme.text, fontSize: 16 * fontSizeScale }]}>
                      {turma.professor || "Sem professor designado"}
                    </Text>
                    
                    <View style={styles.subInfoContainer}>
                      <Text style={[styles.turnoText, { color: theme.text, fontSize: 14 * fontSizeScale }]}>{turma.turno}</Text>
                      <Text style={[styles.divisor, { color: theme.text }]}>•</Text>
                      <Text style={[styles.codigoText, { color: theme.text, fontSize: 14 * fontSizeScale }]}>{turma.codigo_turma}</Text>
                      <Text style={[styles.divisor, { color: theme.text }]}>•</Text>
                      <Text style={[styles.codigoText, { color: theme.text, fontSize: 14 * fontSizeScale }]}>{turma.ano}</Text>
                    </View>
                  </View>
                </View>

                <View style={styles.setaContainer}>
                  <Feather name="chevron-right" size={22 * fontSizeScale} color={COLORS.primary} />
                </View>
              </TouchableOpacity>
            ))
          )}
        </ScrollView>
      )}
    </View>
  );
}