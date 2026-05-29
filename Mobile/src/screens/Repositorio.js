import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator
} from 'react-native';

import Header from '../components/Header';
import SplashScreen from '../screens/SplashScreen';

import { Feather } from '@expo/vector-icons';
import BreadcrumbCard from '../components/BreadcrumbCard'; 
import { COLORS } from "../components/Cores"; 
import styles from '../styles/Repositorio'; 

// DADOS MOCK (PASTAS E ARQUIVOS)
const REPOSITORIO_MOCK = {
  projeto_nome: "Sistema de Gestão Hospitalar",
  pastas: [
    { id: 1, nome: "Documentação", itens: 3 },
    { id: 2, nome: "Imagens do Protótipo", itens: 8 },
    { id: 3, nome: "Scripts SQL", itens: 2 },
  ],
  arquivos: [
    { id: 1, nome: "index.html", tamanho: "12kb" },
    { id: 2, nome: "readme.md", tamanho: "5kb" },
    { id: 3, nome: "package.json", tamanho: "2kb" },
  ]
};

export default function RepositorioScreen() {
  const [loading, setLoading] = useState(true);
  const [selecaoAtiva, setSelecaoAtiva] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 600); 

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#1459b3' }}>
        <ActivityIndicator size="large" color="#fff" />
      </View>
    );
  }

  return (
    // ALTERADO: Trocado por View normal para alinhar a altura exata do Header com as outras telas
    <View style={[styles.container, { flex: 1, backgroundColor: '#1459b3' }]}>
      
      {/* StatusBar configurada exatamente igual às outras telas */}
      <StatusBar barStyle="light-content" backgroundColor="#1459b3" translucent={false} />
      
      {/* Header padrão chamando os parâmetros limpos */}
      <Header nomeTela="Repositório" temGoBack={true} telaDestino="Home" />

      {/* Corpo da tela com o fundo correto */}
      <View style={{ flex: 1, backgroundColor: '#f5f7fb' }}>
        <BreadcrumbCard 
          titulo="Repositório:" 
          itemSub="Projeto: Sistema de Gestão Hospitalar" 
          botaoAcao={true} 
          aoPressionar={() => {}} 
          iconeBotao="download" 
        />

        <ScrollView contentContainerStyle={styles.scrollContent}>
          
          {/* SEÇÃO DE PASTAS */}
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Pastas</Text>
          </View>

          {REPOSITORIO_MOCK.pastas.map((pasta) => (
            <TouchableOpacity key={pasta.id} style={[styles.itemCard, styles.folderBorder]}>
              <View style={styles.itemInfo}>
                {selecaoAtiva && <View style={styles.checkboxPlaceholder} />}
                <Feather name="folder" size={24} color={COLORS.primary} />
                <View style={{ marginLeft: 12 }}>
                  <Text style={styles.itemName}>{pasta.nome}</Text>
                  <Text style={styles.itemSub}>{pasta.itens} itens</Text>
                </View>
              </View>
            </TouchableOpacity>
          ))}

          {/* SEÇÃO DE ARQUIVOS */}
          <View style={[styles.sectionHeader, { marginTop: 20 }]}>
            <Text style={styles.sectionTitle}>Arquivos</Text>
          </View>

          {REPOSITORIO_MOCK.arquivos.map((arquivo) => (
            <View key={arquivo.id} style={[styles.itemCard, styles.fileBorder]}>
              <View style={styles.itemInfo}>
                <Feather name="file-text" size={24} color={COLORS.textSecondary} />
                <View style={{ marginLeft: 12 }}>
                  <Text style={styles.itemName}>{arquivo.nome}</Text>
                  <Text style={styles.itemSub}>{arquivo.tamanho}</Text>
                </View>
              </View>
            </View>
          ))}
        </ScrollView>
      </View>
    </View>
  );
}