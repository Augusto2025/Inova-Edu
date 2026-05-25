import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  LayoutAnimation,
  Platform,
  StatusBar,
  ActivityIndicator,
  Dimensions
} from 'react-native';
import Header from '../components/Header';
import CursosScreen from './Cursos';
import SplashScreen from '../screens/SplashScreen';
import BreadcrumbCard from '../components/BreadcrumbCard';
import { Feather } from '@expo/vector-icons';
import { COLORS } from "../components/Cores"; // Importando as cores para manter a consistência visual
import styles from '../styles/Turma';

const { width } = Dimensions.get('window');

const DATA_MOCK = {
  "2024": [
    { idturma: 1, codigo_turma: "ADS-2024-1A", turno: "Manhã" },
    { idturma: 2, codigo_turma: "ADS-2024-1B", turno: "Noite" },
    { idturma: 3, codigo_turma: "GTI-2024-2N", turno: "Noite" },
  ],
  "2023": [
    { idturma: 4, codigo_turma: "ADS-2023-2B", turno: "Tarde" },
    { idturma: 5, codigo_turma: "GTI-2023-1A", turno: "Manhã" },
  ]
};

export default function TurmasScreen({ navigation }) {
  const [expandedYear, setExpandedYear] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const toggleYear = (year) => {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setExpandedYear(expandedYear === year ? null : year);
  };

  const irParaProjetos = (turma) => {
    navigation.navigate("Projetos", { turmaId: turma.idturma, codigoTurma: turma.codigo_turma });
  };

  return (
    <View style={styles.safeArea}>
      {/* StatusBar Branca para contrastar com Header Azul */}
      <StatusBar barStyle="light-content" backgroundColor={COLORS.darkBlue} />
      
      {/* 
      chamada da header (foto=não tem; escolherImagem=não tem; nome da tela; temGoBack= se sim vai voltar; telaDestino=nome da tela no tabroutes) 
      se temGoBack=true, o botão de voltar aparece e ao clicar ele volta para a tela definida em telaDestino. Se temGoBack=false, o botão de voltar não aparece
      */}
      <Header foto={null} escolherImagem={null} nomeTela={"Turmas"} temGoBack={true} telaDestino={"Repositório"} />

      <BreadcrumbCard titulo="Nome do Curso Selecionado:" itemSub="Curso: Programador de Sistemas" />
      
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {Object.entries(DATA_MOCK).map(([ano, turmas]) => (
          <View key={ano} style={styles.yearSection}>
            
            <TouchableOpacity
              style={[
                styles.yearHeader, 
                expandedYear === ano && styles.activeYearHeader
              ]}
              onPress={() => toggleYear(ano)}
              activeOpacity={0.8}
            >
              <View style={styles.yearRow}>
                <Feather 
                  name="calendar" 
                  size={18} 
                  color={expandedYear === ano ? COLORS.accent : COLORS.primary} 
                  style={{marginRight: 10}}
                />
                <Text style={[
                  styles.yearLabel, 
                  expandedYear === ano && styles.activeYearLabel
                ]}>
                  Ano Letivo {ano}
                </Text>
              </View>
              <Feather 
                name={expandedYear === ano ? "chevron-up" : "chevron-down"} 
                size={20} 
                color={expandedYear === ano ? COLORS.accent : COLORS.textSecondary} 
              />
            </TouchableOpacity>

            {expandedYear === ano && (
              <View style={styles.cardsContainer}>
                {turmas.map((turma) => (
                  <View key={turma.idturma} style={styles.turmaCard}>
                    <View style={styles.cardInfo}>
                      <View style={styles.iconCircle}>
                        <Feather name="users" size={18} color={COLORS.primary} />
                      </View>
                      <View style={{ flex: 1 }}> 
                        <Text style={styles.codigoText}>{turma.codigo_turma}</Text>
                        <Text style={styles.turnoText}>{turma.turno}</Text>
                      </View>
                    </View>

                    <TouchableOpacity 
                      style={styles.actionButton}
                      onPress={() => irParaProjetos(turma)}
                    >
                      <Text style={styles.actionButtonText}>Abrir</Text>
                      <Feather name="external-link" size={12} color="white" />
                    </TouchableOpacity>
                  </View>
                ))}
              </View>
            )}
          </View>
        ))}
      </ScrollView>
    </View>
  );
};