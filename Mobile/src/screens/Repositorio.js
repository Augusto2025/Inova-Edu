import React, { useState, useEffect } from 'react';
import {
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator,
  Alert
} from 'react-native';
import Header from '../components/Header';
import { Feather } from '@expo/vector-icons';
import BreadcrumbCard from '../components/BreadcrumbCard'; 
import { COLORS } from "../components/Cores"; 
import styles from '../styles/Repositorio'; 

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

export default function RepositorioScreen({ route, navigation }) {
  // Captura os dados vindos da tela de Projetos
  const { projetoId, projetoNome } = route.params || { projetoId: null, projetoNome: "Projeto" };

  const [pastas, setPastas] = useState([]);
  const [arquivos, setArquivos] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Estados para controlar a navegação profunda
  const [pastaIdAtual, setPastaIdAtual] = useState(null);
  const [historicoPastas, setHistoricoPastas] = useState([]); 

  useEffect(() => {
    if (projetoId) {
      carregarConteudo();
    }
  }, [projetoId, pastaIdAtual]);

  const carregarConteudo = async () => {
    try {
      setLoading(true);
      let url = `${URL_BASE}/repositorio?projetoId=${projetoId}`;
      if (pastaIdAtual) {
        url += `&pastaId=${pastaIdAtual}`;
      }

      const resposta = await fetch(url);
      const dados = await resposta.json();

      if (dados.pastas && dados.arquivos) {
        setPastas(dados.pastas);
        setArquivos(dados.arquivos);
      } else {
        Alert.alert("Erro", dados.mensagem || "Não foi possível carregar os dados.");
      }
    } catch (error) {
      Alert.alert("Erro", "Falha na conexão com o servidor do repositório.");
    } finally {
      setLoading(false);
    }
  };

  const entrarNaPasta = (pasta) => {
    setHistoricoPastas([...historicoPastas, { id: pasta.id, nome: pasta.nome }]);
    setPastaIdAtual(pasta.id);
  };

  const voltarPasta = () => {
    const novoHistorico = [...historicoPastas];
    novoHistorico.pop(); 
    setHistoricoPastas(novoHistorico);
    setPastaIdAtual(novoHistorico.length > 0 ? novoHistorico[novoHistorico.length - 1].id : null);
  };

  // Cria a string do caminho atual dinamicamente (Ex: Projeto: Hospital > Web > Src)
  const stringCaminho = historicoPastas.length > 0 
    ? `Projeto: ${projetoNome} > ${historicoPastas.map(p => p.nome).join(' > ')}`
    : `Projeto: ${projetoNome}`;

  return (
    <View style={styles.container}>
      <Header nomeTela={"Repositório"} temGoBack={true} telaDestino={"Projetos"} />

      <View style={{ flex: 1, backgroundColor: COLORS.backgroundCard }}>
        <BreadcrumbCard 
          titulo="Repositório:" 
          itemSub={stringCaminho}
        />

        {loading ? (
          <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <ActivityIndicator size="large" color={COLORS.primary} />
            <Text style={{ marginTop: 10, color: COLORS.primary }}>Carregando arquivos...</Text>
          </View>
        ) : (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            
            {/* Botão de Voltar de nível (aparece apenas quando estiver dentro de alguma pasta) */}
            {pastaIdAtual && (
              <TouchableOpacity style={[styles.itemCard, { backgroundColor: '#F8FAFC' }]} onPress={voltarPasta}>
                <View style={styles.itemInfo}>
                  <Feather name="arrow-left" size={22} color={COLORS.textSecondary} />
                  <Text style={[styles.itemName, { marginLeft: 12, color: COLORS.textSecondary }]}>.. Voltar para pasta anterior</Text>
                </View>
              </TouchableOpacity>
            )}

            {/* SEÇÃO DE PASTAS */}
            <View style={styles.sectionHeader}>
              <Text style={styles.sectionTitle}>Pastas</Text>
            </View>

            {pastas.length === 0 && (
              <Text style={[styles.itemSub, { paddingLeft: 16, fontStyle: 'italic' }]}>Nenhuma subpasta aqui.</Text>
            )}

            {pastas.map((pasta) => (
              <TouchableOpacity 
                key={pasta.id} 
                style={[styles.itemCard, styles.folderBorder]}
                onPress={() => entrarNaPasta(pasta)}
              >
                <View style={styles.itemInfo}>
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

            {arquivos.length === 0 && (
              <Text style={[styles.itemSub, { paddingLeft: 16, fontStyle: 'italic' }]}>Nenhum arquivo nesta pasta.</Text>
            )}

            {arquivos.map((arquivo) => (
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
        )}
      </View>

      <TouchableOpacity 
        style={styles.btnActionMain} 
        onPress={() => {}}
        activeOpacity={0.7}
      >
        <Feather name="download" size={25} color="white"/>
        <Text style={{ color: 'white', fontSize: 13, marginTop: 2 }}>Baixar</Text>
      </TouchableOpacity>
    </View>
  );
}