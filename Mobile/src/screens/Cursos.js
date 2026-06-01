import React, { useState } from 'react';
import { 
  StyleSheet, 
  View, 
  Text, 
  ScrollView, 
  TouchableOpacity, 
  TextInput, 
  Modal,
  SafeAreaView,
  Dimensions
} from 'react-native';
import Card from '../components/Card';
import Header from '../components/Header';
import styles from '../styles/Curso';

const { width } = Dimensions.get('window');

export default function CursosScreen({ navigation }) {
  const [search, setSearch] = useState('');

  const cursos = [
    { id: 1, nome_curso: 'Informática Básica' },
    { id: 2, nome_curso: 'Excel Avançado' },
    { id: 3, nome_curso: 'Desenvolvimento Web Full Stack' },
  ];

  const irParaTurmas = (curso) => {
    navigation.navigate("Turmas", { cursoId: curso.id, nomeCurso: curso.nome_curso });
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.listaCursos}>
        {/* HEADER */}
        <Header foto={null} escolherImagem={null} nomeTela={"Cursos"} />
        
        <View style={{ width: '90%', margin: 20, marginBottom: 0, marginTop: 0 }}>
          {cursos.length === 0 ? (
            <Text style={styles.vazio}>Nenhum resultado encontrado.</Text>
          ) : (
            cursos.map((curso) => (
              <Card 
                key={curso.id}
                titulo={curso.nome_curso}
                textoBotao="Entrar"
                iconeBotao="arrow-right"
                aoPressionar={() => irParaTurmas(curso)}
              />
            ))
          )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};