import React, { useState } from 'react';
import {
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  Image,
  Modal,
  TextInput,
  SafeAreaView
} from 'react-native';
import Header from '../components/Header';
import BreadcrumbCard from '../components/BreadcrumbCard';
import { Feather } from '@expo/vector-icons';
import { COLORS } from "../components/Cores"; 
import styles from '../styles/Projeto';

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
    imagem: null, 
    repo: "https://github.com/exemplo/eco"
  }
];

export default function ProjetosScreen({ navigation }) {
  const [modalVisible, setModalVisible] = useState(false);

  const irParaRepositorio = (repositorio) => {
    navigation.navigate("Repositorio", { url: repositorio });
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.dark} />
      
      <Header 
        foto={null} 
        escolherImagem={null} 
        nomeTela={"Projetos"} 
        temGoBack={true} 
        telaDestino={"Turmas"} 
      />

      <BreadcrumbCard titulo="Projetos:" itemSub="Turma: ADS-2024-1A" />

      {/* Botão flutuante ou de topo para abrir o cadastro do modal, caso precise */}
      {/* <View style={{ paddingHorizontal: 16, alignItems: 'flex-end', marginBottom: 4 }}>
        <TouchableOpacity style={styles.btnAdd} onPress={() => setModalVisible(true)}>
          <Feather name="plus" size={20} color="white" />
        </TouchableOpacity>
      </View> */}

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {PROJETOS_ESTATICOS.map((projeto) => (
          <TouchableOpacity 
            key={projeto.id} 
            style={styles.projetoCard}
            onPress={() => irParaRepositorio(projeto.repo)}
            activeOpacity={0.7}
          >
            <View style={styles.cardInfo}>
              
              {/* Imagem Quadrada (ou Placeholder) alinhada à esquerda */}
              {projeto.imagem ? (
                <Image source={{ uri: projeto.imagem }} style={styles.projetoImagemQuadrada} />
              ) : (
                <View style={[styles.projetoImagemQuadrada, styles.placeholderImagemContainer]}>
                  <Feather name="folder" size={22} color={COLORS.primary} />
                </View>
              )}
              
              {/* Bloco de texto: Nome acima e Descrição abaixo */}
              <View style={{ flex: 1 }}> 
                <Text style={styles.projetoNome} numberOfLines={1}>
                  {projeto.nome}
                </Text>
                <Text style={styles.projetoDesc} numberOfLines={2}>
                  {projeto.descricao}
                </Text>
              </View>
            </View>

            {/* Ícone de seta lateral idêntico ao das turmas */}
            <View style={styles.setaContainer}>
              <Feather name="chevron-right" size={22} color={COLORS.primary} />
            </View>
          </TouchableOpacity>
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