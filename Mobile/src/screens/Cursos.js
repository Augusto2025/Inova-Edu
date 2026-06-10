import React, { useState } from 'react';
import { 
  View, 
  Text, 
  ScrollView, 
  TouchableOpacity, 
  Image
} from 'react-native';
import Header from '../components/Header';
import styles from '../styles/Curso';
import { COLORS } from '../components/Cores';

export default function CursosScreen({ navigation }) {
  const [search, setSearch] = useState('');

  // Adicionada a propriedade opcional 'imagem' nos dados do curso
  const cursos = [
    { id: 1, nome_curso: 'Informática Básica', imagem: null },
    { id: 2, nome_curso: 'Excel Avançado', imagem: 'https://picsum.photos/seed/shop/300/200' },
    { id: 3, nome_curso: 'Desenvolvimento Web Full Stack', imagem: null },
  ];

  const irParaTurmas = (curso) => {
    navigation.navigate("Turmas", { cursoId: curso.id, nomeCurso: curso.nome_curso });
  };

  return (
    <View style={styles.container}>
      {/* HEADER */}
      <Header foto={null} escolherImagem={null} nomeTela={"Cursos"} />
      
      <ScrollView contentContainerStyle={styles.listaCursos}>
        {cursos.length === 0 ? (
          <Text style={styles.vazio}>Nenhum resultado encontrado.</Text>
        ) : (
          cursos.map((curso) => (
            <TouchableOpacity 
              key={curso.id} 
              style={styles.cardCursoGrid}
              onPress={() => irParaTurmas(curso)}
              activeOpacity={0.8}
            >
              {/* Renderiza a imagem se houver, caso contrário renderiza um bloco container placeholder */}
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
    </View>
  );
}