import React, { useState, useEffect, useContext, useCallback } from 'react';
import {
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator,
  Alert
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import Header from '../components/Header';
import Skeleton from '../components/Skeleton';
import { Feather } from '@expo/vector-icons';
import BreadcrumbCard from '../components/BreadcrumbCard'; 
import { COLORS } from "../components/Cores"; 
import styles from '../styles/Repositorio'; 

import * as FileSystem from 'expo-file-system/legacy';
import * as Sharing from 'expo-sharing';

// Importação do Contexto de Tema (Obrigatório para o modo escuro)
import { ThemeContext } from '../context/ThemeContext';
import { URL_BASE } from '../config/backend';

export default function RepositorioScreen({ route, navigation }) {
  // AQUI ESTÁ A CORREÇÃO! Puxando as configurações visuais do app.
  const context = useContext(ThemeContext);
  const theme = context?.theme || { background: '#FFFFFF', card: '#F8FAFC', text: '#000000', border: '#E2E8F0', dark: false };
  const fontSizeScale = context?.fontSizeScale || 1;

  const { projetoId, projetoNome } = route.params || { projetoId: null, projetoNome: "Projeto" };

  const [pastas, setPastas] = useState([]);
  const [arquivos, setArquivos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false); 
  
  const [pastaIdAtual, setPastaIdAtual] = useState(null);
  const [historicoPastas, setHistoricoPastas] = useState([]); 

  // Função convertida para useCallback para rodar perfeitamente com o useFocusEffect
  const carregarConteudo = useCallback(async () => {
    try {
      setLoading(true);
      let url = `${URL_BASE}/repositorio?projetoId=${projetoId}`;
      if (pastaIdAtual) {
        url += `&pastaId=${pastaIdAtual}`;
      }

      const resposta = await fetch(url);

      if (!resposta.ok) {
        throw new Error(`Servidor respondeu com código ${resposta.status}`);
      }

      const dados = await resposta.json();

      if (dados.pastas && dados.arquivos) {
        setPastas(dados.pastas);
        setArquivos(dados.arquivos);
      } else {
        Alert.alert("Erro", dados.mensagem || "Não foi possível carregar os dados.");
      }
    } catch (error) {
      Alert.alert(
        "Erro na Requisição", 
        error.message === "Network request failed" 
          ? "Falha na conexão: Verifique sua internet ou se o servidor está ligado." 
          : error.message
      );
    } finally {
      setLoading(false);
    }
  }, [projetoId, pastaIdAtual]);

  // Atualiza as pastas sempre que o usuário voltar para essa tela
  useFocusEffect(
    useCallback(() => {
      if (projetoId) {
        carregarConteudo();
      }
    }, [carregarConteudo, projetoId])
  );

  const baixarRepositorioZip = async () => {
    if (!projetoId) {
      Alert.alert("Erro", "Não foi possível identificar o ID do projeto.");
      return;
    }

    try {
      setDownloading(true);

      const urlZip = `${URL_BASE}/repositorio/download-zip?projetoId=${projetoId}`;
      const localDoArquivo = `${FileSystem.documentDirectory}repositorio_${projetoId}.zip`;

      const resultadoDownload = await FileSystem.downloadAsync(urlZip, localDoArquivo);

      if (resultadoDownload.status === 200) {
        const disponivel = await Sharing.isAvailableAsync();
        if (disponivel) {
          await Sharing.shareAsync(resultadoDownload.uri, {
            mimeType: 'application/zip',
            dialogTitle: `Baixar Repositório: ${projetoNome}`,
            UTI: 'public.zip-archive' 
          });
        } else {
          Alert.alert("Erro", "Seu dispositivo não suporta compartilhamento de arquivos.");
        }
      } else {
        Alert.alert("Erro", "Não foi possível gerar o arquivo ZIP no servidor.");
      }
    } catch (error) {
      Alert.alert("Falha no download", "Houve um problema ao baixar o arquivo do repositório.");
      console.log(error);
    } finally {
      setDownloading(false);
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

  const stringCaminho = historicoPastas.length > 0 
    ? `Projeto: ${projetoNome} > ${historicoPastas.map(p => p.nome).join(' > ')}`
    : `Projeto: ${projetoNome}`;

  return (
    <View style={[styles.container, { backgroundColor: theme.background }]}>
      <Header nomeTela={"Repositório"} temGoBack={true} telaDestino={"Projetos"} carregando={loading} />

      <View style={{ flex: 1, backgroundColor: theme.background }}>
        <BreadcrumbCard 
          titulo="Repositório:" 
          itemSub={stringCaminho}
        />

        {loading ? (
          <View style={{ flex: 1, padding: 20 }}>
            <Skeleton width="100%" height={50} borderRadius={16} style={{ marginBottom: 16 }} />
            {[1, 2, 3].map((item) => (
              <Skeleton key={item} width="100%" height={80} borderRadius={18} style={{ marginBottom: 16 }} />
            ))}
          </View>
        ) : (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            {pastaIdAtual && (
              <TouchableOpacity style={[styles.itemCard, { backgroundColor: theme.card }]} onPress={voltarPasta}>
                <View style={styles.itemInfo}>
                  <Feather name="arrow-left" size={20 * fontSizeScale} color={theme.text} />
                  <Text style={{ marginLeft: 12, color: theme.text, fontSize: 14 * fontSizeScale }}>Voltar</Text>
                </View>
              </TouchableOpacity>
            )}

            {/* VERIFICAÇÃO DE VAZIO: Se não houver pastas nem arquivos */}
            {pastas.length === 0 && arquivos.length === 0 ? (
              <View style={{ marginTop: 40, alignItems: 'center', padding: 20 }}>
                <Feather name="folder-minus" size={48 * fontSizeScale} color={theme.text} style={{ opacity: 0.5 }} />
                <Text style={{ color: theme.text, fontSize: 16 * fontSizeScale, marginTop: 15, textAlign: 'center', opacity: 0.7 }}>
                  Nenhuma pasta ou arquivo disponível neste local.
                </Text>
              </View>
            ) : (
              <>
                {/* Pastas */}
                {pastas.length > 0 && (
                  <>
                    <Text style={[styles.sectionTitle, { color: theme.text, marginVertical: 10, fontSize: 16 * fontSizeScale }]}>Pastas</Text>
                    {pastas.map((pasta) => (
                      <TouchableOpacity key={pasta.id} style={[styles.itemCard, { backgroundColor: theme.card, borderColor: theme.border }]} onPress={() => entrarNaPasta(pasta)}>
                        <View style={styles.itemInfo}>
                          <Feather name="folder" size={24 * fontSizeScale} color={COLORS.primary} />
                          <View style={{ marginLeft: 12 }}>
                            <Text style={[styles.itemName, { color: theme.text, fontSize: 15 * fontSizeScale }]}>{pasta.nome}</Text>
                          </View>
                        </View>
                      </TouchableOpacity>
                    ))}
                  </>
                )}

                {/* Arquivos */}
                {arquivos.length > 0 && (
                  <>
                    <Text style={[styles.sectionTitle, { color: theme.text, marginVertical: 10, fontSize: 16 * fontSizeScale }]}>Arquivos</Text>
                    {arquivos.map((arquivo) => (
                      <View key={arquivo.id} style={[styles.itemCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
                        <View style={styles.itemInfo}>
                          <Feather name="file-text" size={24 * fontSizeScale} color={theme.text} />
                          <View style={{ marginLeft: 12 }}>
                            <Text style={[styles.itemName, { color: theme.text, fontSize: 15 * fontSizeScale }]}>{arquivo.nome}</Text>
                          </View>
                        </View>
                      </View>
                    ))}
                  </>
                )}
              </>
            )}
          </ScrollView>
        )}
      </View>

      <TouchableOpacity 
        style={[styles.btnActionMain, downloading && { backgroundColor: '#94A3B8' }]} 
        onPress={baixarRepositorioZip}
        disabled={downloading}
        activeOpacity={0.7}
      >
        {downloading ? (
          <ActivityIndicator size="small" color="white" />
        ) : (
          <>
            <Feather name="download" size={25} color="white"/>
            <Text style={{ color: 'white', fontSize: 13, marginTop: 2 }}>Baixar</Text>
          </>
        )}
      </TouchableOpacity>
    </View>
  );
}