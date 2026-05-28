import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator,
  Alert,
  Modal,
  TextInput
} from 'react-native';

// CORREÇÃO AQUI: Importando o SafeAreaView da biblioteca correta para sumir o aviso
import { SafeAreaView } from 'react-native-safe-area-context'; 

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
  const [modalPastaVisible, setModalPastaVisible] = useState(false);
  const [selecaoAtiva, setSelecaoAtiva] = useState(false);

  // CORREÇÃO AQUI: Simulando o fim do carregamento para não travar a tela
  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000); // esconde o loading após 1 segundo

    return () => clearTimeout(timer);
  }, []);

  // Se ainda estiver carregando, mostra o indicador visual
  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: COLORS.darkBlue }}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.darkBlue} />
      
      <Header nomeTela={"Repositório"} temGoBack={true} telaDestino={"Projetos"} />

      <BreadcrumbCard titulo="Repositório:" itemSub="Projeto: Sistema de Gestão Hospitalar" botaoAcao={true} aoPressionar={() => {}} iconeBotao="download" />

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
    </SafeAreaView>
  );
}