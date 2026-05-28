import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  Platform,
  StatusBar,
  ActivityIndicator,
  Image,
  Alert,
  Modal,
  TextInput,
  SafeAreaView
} from 'react-native';
import Header from '../components/Header';
import SplashScreen from '../screens/SplashScreen';

import { Feather } from '@expo/vector-icons';
import Card from '../components/Card';

import { COLORS } from "../components/Cores"; // Importando as cores para manter a consistência visual
import BreadcrumbCard from '../components/BreadcrumbCard'; // Importando o BreadcrumbCard para mostrar a rota atual
import styles from '../styles/Projeto'; // Importando os estilos específicos para a tela de Projetos

// DADOS ESTÁTICOS (MOCK)
const PROJETOS_ESTATICOS = [
  {
    id: 1,
    nome: "Sistema de Gestão Hospitalar",
    descricao: "Desenvolvimento de uma interface para triagem rápida de pacientes em prontos-socorros.",
    imagem: "https://picsum.photos/seed/hosp/300/200",
    repo: "https://github.com/exemplo/hospital"
  },
  {
    id: 2,
    nome: "E-Commerce de Artesanato",
    descricao: "Plataforma para artesãos locais venderem produtos com foco em sustentabilidade.",
    imagem: "https://picsum.photos/seed/shop/300/200",
    repo: "https://github.com/exemplo/shop"
  },
  {
    id: 3,
    nome: "App de Monitoramento Ambiental",
    descricao: "Aplicação mobile que utiliza sensores IoT para medir a qualidade do ar em tempo real.",
    imagem: null, // Teste sem imagem
    repo: "https://github.com/exemplo/eco"
  }
];

export default function ProjetosScreen({ navigation }) {
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);

  const confirmarExclusao = (nome) => {
    Alert.alert(
      "🗑️ Excluir Projeto",
      `Deseja realmente apagar o projeto "${nome}"?`,
      [
        { text: "Cancelar", style: "cancel" },
        { text: "Excluir", style: "destructive", onPress: () => console.log("Excluído") }
      ]
    );
  };

  const irParaRepositorio = (repositorio) => {
    navigation.navigate("Repositorio", { url: repositorio });
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.dark} />
      
      <Header foto={null} escolherImagem={null} nomeTela={"Projetos"} temGoBack={true} telaDestino={"Turmas"} />

      <BreadcrumbCard titulo="Projetos:" itemSub="Turma: ADS-2024-1A" />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* LISTAGEM DE PROJETOS */}
        {PROJETOS_ESTATICOS.map((projeto) => (
          <Card 
            key={projeto.id}
            titulo={projeto.nome}
            descricao={projeto.descricao}
            imagem={projeto.imagem}
            textoBotao="Repositório"
            iconeBotao="external-link"
            aoPressionar={() => irParaRepositorio(projeto.repo)}
          />
        ))}
      </ScrollView>

      {/* MODAL DE CADASTRO (ESTÁTICO) */}
      <Modal animationType="slide" transparent={true} visible={modalVisible}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Novo Projeto</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Feather name="x" size={24} color={COLORS.textSecondary} />
              </TouchableOpacity>
            </View>

            <TextInput style={styles.input} placeholder="Nome do projeto" placeholderTextColor="#94A3B8" />
            <TextInput 
              style={[styles.input, { height: 100, textAlignVertical: 'top' }]} 
              placeholder="Descrição curta..." 
              multiline 
              placeholderTextColor="#94A3B8"
            />
            <TouchableOpacity style={styles.uploadBtn}>
              <Feather name="image" size={20} color={COLORS.primary} />
              <Text style={styles.uploadText}>Upload de Capa</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.btnSave} onPress={() => setModalVisible(false)}>
              <Text style={styles.btnSaveText}>Salvar Projeto</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}