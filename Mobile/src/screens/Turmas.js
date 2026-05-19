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
  ActivityIndicator
} from 'react-native';

import { Feather } from '@expo/vector-icons';

const COLORS = {
  primary: '#005eb8',   // Azul Senac
  darkBlue: '#003d7a',  // Azul mais escuro para o Header
  accent: '#f7941d',    // Laranja Senac
  background: '#EBF2F7', // Fundo levemente azulado
  card: '#FFFFFF',
  textMain: '#1E293B',
  textSecondary: '#64748B',
  border: '#CBD5E1'
};

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

  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 1200);
    return () => clearTimeout(timer);
  }, []);

  const toggleYear = (year) => {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setExpandedYear(expandedYear === year ? null : year);
  };

  if (isLoading) {
    return (
      <View style={[styles.safeArea, styles.center]}>
        <ActivityIndicator size="large" color={COLORS.primary} />
        <Text style={styles.loadingText}>Carregando Turmas...</Text>
      </View>
    );
  }

  const irParaProjetos = (turma) => {
    navigation.navigate("Projetos", { turmaId: turma.idturma, codigoTurma: turma.codigo_turma });
  };

  return (
    <View style={styles.safeArea}>
      {/* StatusBar Branca para contrastar com Header Azul */}
      <StatusBar barStyle="light-content" backgroundColor={COLORS.darkBlue} />
      
      {/* Header Centralizado e Azul */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Turmas</Text>
      </View>

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
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  center: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 15,
    color: COLORS.primary,
    fontSize: 14,
    fontWeight: '600',
  },
  header: {
    paddingTop: Platform.OS === 'ios' ? 55 : 20,
    paddingBottom: 20,
    backgroundColor: COLORS.darkBlue,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 10,
    shadowColor: '#black',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 5,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  scrollContent: {
    padding: 16,
    paddingTop: 24,
  },
  yearSection: {
    marginBottom: 14,
  },
  yearHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: COLORS.card,
    padding: 18,
    borderRadius: 12,
    borderLeftWidth: 5,
    borderLeftColor: COLORS.primary, // Indicador azul lateral
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
  },
  activeYearHeader: {
    borderBottomLeftRadius: 0,
    borderBottomRightRadius: 0,
    borderLeftColor: COLORS.accent, // Muda para laranja quando aberto
  },
  yearRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  yearLabel: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.primary,
  },
  activeYearLabel: {
    color: COLORS.textMain,
  },
  cardsContainer: {
    backgroundColor: '#D1DEE9', // Fundo azulado interno
    padding: 10,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
  },
  turmaCard: {
    backgroundColor: COLORS.card,
    borderRadius: 10,
    padding: 15,
    marginBottom: 8,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  cardInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  iconCircle: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: '#E0EEFF',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  codigoText: {
    fontSize: 15,
    fontWeight: '700',
    color: COLORS.darkBlue,
  },
  turnoText: {
    fontSize: 12,
    color: COLORS.textSecondary,
    fontWeight: '500',
  },
  actionButton: {
    backgroundColor: COLORS.primary,
    paddingVertical: 8,
    paddingHorizontal: 14,
    borderRadius: 8,
    flexDirection: 'row',
    alignItems: 'center',
  },
  actionButtonText: {
    color: 'white',
    fontSize: 12,
    fontWeight: 'bold',
    marginRight: 5,
  },
});