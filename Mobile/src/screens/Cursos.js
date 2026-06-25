import React, { useState, useContext, useCallback } from 'react';
import { 
  View, 
  Text, 
  ScrollView, 
  TouchableOpacity, 
  Image,
  ActivityIndicator, 
  Alert
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native'; // 1. Hook de recarregamento
import Header from '../components/Header';
import styles from '../styles/Curso';
import BarraPesquisa from '../components/BarraPesquisa';
import { API_ENDPOINTS } from '../services/api';

// 2. Importação do Contexto de Tema e Acessibilidade
import { ThemeContext } from '../context/ThemeContext';

const URL_CURSOS = API_ENDPOINTS.cursos;

export default function CursosScreen({ navigation }) {
  // Puxando as variáveis globais
  const { theme, fontSizeScale } = useContext(ThemeContext);

  const [search, setSearch] = useState('');
  const [cursos, setCursos] = useState([]); 
  const [carregando, setCarregando] = useState(true); 

  // 3. Transformamos a busca em um useCallback para evitar loops infinitos
  const buscarCursos = useCallback(async () => {
    try {
      setCarregando(true);
      const resposta = await fetch(URL_CURSOS, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });

      const dados = await resposta.json(); 
      setCursos(dados); 
      
    } catch (error) {
      console.error('Erro ao buscar cursos:', error);
      Alert.alert('Erro', 'Não foi possível carregar os cursos.');
    } finally {
      setCarregando(false);
    }
  }, []);

  // 4. MÁGICA DO RECARREGAMENTO: Executa buscarCursos() toda vez que a tela é aberta
  useFocusEffect(
    useCallback(() => {
      buscarCursos();
    }, [buscarCursos])
  );

  const irParaTurmas = (curso) => {
    navigation.navigate("Turmas", { cursoId: curso.idcurso, nomeCurso: curso.nome_curso });
  };

  return (
    // Fundo dinâmico aplicado ao container principal
    <View style={[styles.container, { backgroundColor: theme.background }]}>
      
      <Header foto={null} escolherImagem={null} nomeTela={"Cursos"} />
      
      <BarraPesquisa value={search} onChangeText={setSearch} />

      {carregando ? (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <ActivityIndicator size="large" color="#1459b3" />
          <Text style={{ marginTop: 10, color: theme.text, fontSize: 14 * fontSizeScale }}>
            Buscando cursos...
          </Text>
        </View>
      ) : (
        <ScrollView contentContainerStyle={styles.listaCursos}>
          {cursos.length === 0 ? (
            <Text style={[styles.vazio, { color: theme.text, fontSize: 16 * fontSizeScale }]}>
              Nenhum resultado encontrado.
            </Text>
          ) : (
            cursos.map((curso) => (
              <TouchableOpacity 
                key={curso.idcurso} 
                // Card dinâmico (Cor de fundo se adapta ao modo escuro)
                style={[styles.cardCursoGrid, { backgroundColor: theme.card }]}
                onPress={() => irParaTurmas(curso)}
                activeOpacity={0.8}
              >
                {curso.imagem ? (
                  <Image source={{ uri: curso.imagem }} style={styles.cursoImagem} />
                ) : (
                  // O fundo do placeholder também fica mais escuro no dark mode
                  <View style={[styles.placeholderImagemContainer, { backgroundColor: theme.border }]}>
                    <Text style={styles.placeholderIcone}>🎓</Text>
                  </View>
                )}
                
                <View style={styles.textoCursoContainer}>
                  {/* Fonte dinâmica e cor do texto adaptável */}
                  <Text style={[styles.tituloCursoGrid, { color: theme.text, fontSize: 14 * fontSizeScale }]} numberOfLines={2}>
                    {curso.nome_curso}
                  </Text>
                </View>
              </TouchableOpacity>
            ))
          )}
        </ScrollView>
      )}
    </View>
  );
}