import React, { useState } from 'react';
import {
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  StatusBar
} from 'react-native';
import Header from '../components/Header';
import BreadcrumbCard from '../components/BreadcrumbCard';
import { Feather } from '@expo/vector-icons';
import { COLORS } from "../components/Cores"; 
import styles from '../styles/Turma';
import BarraPesquisa from '../components/BarraPesquisa';

const DATA_TURMAS = [
  { idturma: 1, codigo_turma: "ADS-2024-1A", turno: "Manhã", professor: "Prof. Carlos Silva", ano: "2024" },
  { idturma: 2, codigo_turma: "ADS-2024-1B", turno: "Noite", professor: "Profa. Ana Beatriz", ano: "2024" },
  { idturma: 3, codigo_turma: "GTI-2024-2N", turno: "Noite", professor: "Prof. Marcos Oliveira", ano: "2024" },
  { idturma: 4, codigo_turma: "ADS-2023-2B", turno: "Tarde", professor: "Profa. Juliana Costa", ano: "2023" },
  { idturma: 5, codigo_turma: "GTI-2023-1A", turno: "Manhã", professor: "Prof. Roberto Mendes", ano: "2023" },
];

export default function TurmasScreen({ navigation }) {
  // Estados para gerenciar as seleções dos filtros
  const [anoSelecionado, setAnoSelecionado] = useState(null); // '2024', '2023' ou null
  const [turnoSelecionado, setTurnoSelecionado] = useState(null); // 'Manhã', 'Tarde', 'Noite' ou null
  const [ordemAlfabetica, setOrdemAlfabetica] = useState(false); // true ou false

  const irParaProjetos = (turma) => {
    navigation.navigate("Projetos", { turmaId: turma.idturma, codigoTurma: turma.codigo_turma });
  };

  // 1. Aplica as regras de filtragem (Ano e Turno)
  let turmasExibidas = DATA_TURMAS.filter(turma => {
    const passaAno = anoSelecionado ? turma.ano === anoSelecionado : true;
    const passaTurno = turnoSelecionado ? turma.turno === turnoSelecionado : true;
    return passaAno && passaTurno;
  });

  // 2. Aplica a ordenação alfabética pelo nome do professor se estiver ativa
  if (ordemAlfabetica) {
    turmasExibidas = [...turmasExibidas].sort((a, b) => 
      a.professor.localeCompare(b.professor)
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
        telaDestino={"Repositório"} 
      />

      {/* SELEÇÃO DE FILTROS HORIZONTAIS (Acima do Breadcrumb) */}
      <View style={styles.filtroContainer}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.filtroScroll}>
          
          {/* Filtro de Ordem Alfabética */}
          <TouchableOpacity 
            style={[styles.chip, ordemAlfabetica && styles.chipAtivo]} 
            onPress={() => setOrdemAlfabetica(!ordemAlfabetica)}
          >
            <Feather name="sort-by-alpha" size={14} color={ordemAlfabetica ? '#FFF' : COLORS.primary} style={{ marginRight: 4 }} />
            <Text style={[styles.chipTexto, ordemAlfabetica && styles.chipTextoAtivo]}>A-Z</Text>
          </TouchableOpacity>

          {/* Separador visual opcional */}
          <View style={styles.divisorFiltro} />

          {/* Filtros de Ano */}
          {['2024', '2023'].map(ano => (
            <TouchableOpacity 
              key={ano}
              style={[styles.chip, anoSelecionado === ano && styles.chipAtivo]} 
              onPress={() => setAnoSelecionado(anoSelecionado === ano ? null : ano)}
            >
              <Text style={[styles.chipTexto, anoSelecionado === ano && styles.chipTextoAtivo]}>{ano}</Text>
            </TouchableOpacity>
          ))}

          <View style={styles.divisorFiltro} />

          {/* Filtros de Turno */}
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
      
      <BreadcrumbCard titulo="Turmas:" itemSub="Curso: Programador de Sistemas" />

      <BarraPesquisa />
      
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
                  <Text style={styles.professorText}>{turma.professor}</Text>
                  
                  <View style={styles.subInfoContainer}>
                    <Text style={styles.turnoText}>{turma.turno}</Text>
                    <Text style={styles.divisor}>•</Text>
                    <Text style={styles.codigoText}>{turma.codigo_turma}</Text>
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
    </View>
  );
}