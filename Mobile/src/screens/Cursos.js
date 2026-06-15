import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  ScrollView, 
  TouchableOpacity, 
  Image,
  ActivityIndicator, // Adicionado para o efeito de carregamento
  Alert
} from 'react-native';
import Header from '../components/Header';
import styles from '../styles/Curso';
import BarraPesquisa from '../components/BarraPesquisa';
import { COLORS } from '../components/Cores';

// Sem gambiarra de .replace()! Somamos a BASE com o caminho de cursos:
const BASE_URL = process.env.EXPO_PUBLIC_URL_BACKEND;
const URL_CURSOS = `${BASE_URL}/cursos`;

export default function CursosScreen({ navigation }) {
  const [search, setSearch] = useState('');
  const [cursos, setCursos] = useState([]); // 📥 Começa como uma lista vazia
  const [carregando, setCarregando] = useState(true); // ⏳ Estado de carregamento

  // Dispara a busca automática assim que a tela abre
  useEffect(() => {
    buscarCursos();
  }, []);

  const buscarCursos = async () => {
    try {
      setCarregando(true);
      const resposta = await fetch(URL_CURSOS, {
        method: 'GET', // Requisição do tipo GET para puxar dados
        headers: {
          'Content-Type': 'application/json',
        }
      });

      const dados = await resposta.json();
      
      // Se o backend devolver a lista diretamente:
      setCursos(dados); 
      
    } catch (error) {
      console.error('Erro ao buscar cursos:', error);
      Alert.alert('Erro', 'Não foi possível carregar os cursos do servidor.');
    } finally {
      setCarregando(false); // Desliga a rodinha de carregamento
    }
  };

  const irParaTurmas = (curso) => {
    // Ajustado de curso.id para curso.idcurso para bater com seu Django
    navigation.navigate("Turmas", { cursoId: curso.idcurso, nomeCurso: curso.nome_curso });
  };

  return (
    <View style={styles.container}>
      {/* HEADER */}
      <Header foto={null} escolherImagem={null} nomeTela={"Cursos"} />
      
      <BarraPesquisa value={search} onChangeText={setSearch} />

      {/* Se estiver carregando, mostra a rodinha. Se não, mostra a lista */}
      {carregando ? (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <ActivityIndicator size="large" color="#1459b3" />
          <Text style={{ marginTop: 10, color: '#1459b3' }}>Buscando cursos...</Text>
        </View>
      ) : (
        <ScrollView contentContainerStyle={styles.listaCursos}>
          {cursos.length === 0 ? (
            <Text style={styles.vazio}>Nenhum resultado encontrado.</Text>
          ) : (
            cursos.map((curso) => (
              <TouchableOpacity 
                key={curso.idcurso} // Ajustado para idcurso
                style={styles.cardCursoGrid}
                onPress={() => irParaTurmas(curso)}
                activeOpacity={0.8}
              >
                {/* O Cloudinary envia a URL pronta na propriedade curso.imagem */}
                {curso.imagem ? (
                  <Image source={{ uri: curso.imagem }} style={styles.cursoImagem} />
                ) : (
                  <View style={styles.placeholderImagemContainer}>
                    <Text style={styles.placeholderIcone}>🎓</Text>
                  </View>
                )}
                
                <View style={styles.textoCursoContainer}>
                  <Text style={styles.tituloCursoGrid} numberOfLines={2}>
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