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

const { width } = Dimensions.get('window');

export default function CursosScreen({ navigation }) {
  const [modalVisible, setModalVisible] = useState(false);
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
      {/* HEADER */}

      <ScrollView contentContainerStyle={styles.listaCursos}>
        <Header foto={null} escolherImagem={null} nomeTela={"Cursos"} />
        
        <View style={styles.filtroContainer}>
          <TouchableOpacity 
            style={styles.filtroBotaoHeader} 
            onPress={() => setModalVisible(true)}
          >
            <Text style={styles.filtroIconeTexto}>≡</Text>
          </TouchableOpacity>
        </View>
        
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

      {/* MODAL SIDEBAR (DIREITA) */}
      <Modal
        animationType="fade"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <TouchableOpacity 
            style={styles.foraModal} 
            activeOpacity={1} 
            onPress={() => setModalVisible(false)} 
          />
          
          <View style={styles.sidebar}>
            <View style={styles.sidebarHeader}>
              <Text style={styles.sidebarTitulo}>Filtros</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Text style={styles.closeBtn}>✕</Text>
              </TouchableOpacity>
            </View>

            <View style={styles.formFiltro}>
              <Text style={styles.label}>Pesquisa</Text>
              <TextInput 
                style={styles.input} 
                placeholder="Ex: Excel" 
                value={search}
                onChangeText={setSearch}
              />

              <Text style={styles.label}>Data de início</Text>
              <View style={styles.inputFake}><Text style={{color: '#999'}}>dd/mm/aaaa</Text></View>

              <Text style={styles.label}>Ordenar por</Text>
              <View style={styles.inputFake}><Text>Padrão</Text></View>

              <TouchableOpacity 
                style={styles.btnAplicar} 
                onPress={() => setModalVisible(false)}
              >
                <Text style={styles.btnAplicarTexto}>Aplicar Filtros</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8F9FA' },
  
  filtroContainer: { width: '100%', paddingRight: 20, justifyContent: 'flex-end', alignItems: 'center', flexDirection: 'row' },
  filtroBotaoHeader: { width: 50,},
  filtroIconeTexto: { color: '#004A8D', fontSize: 45, textAlign: 'right' },

  // SIDEBAR
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.4)', flexDirection: 'row' },
  foraModal: { flex: 1 },
  sidebar: { 
    width: width * 0.75, 
    backgroundColor: '#fff', 
    height: '100%', 
    padding: 25 
  },
  sidebarHeader: { 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    marginBottom: 30, 
    marginTop: 20 
  },
  sidebarTitulo: { fontSize: 22, fontWeight: 'bold', color: '#004A8D' },
  closeBtn: { fontSize: 22, color: '#999' },
  label: { fontSize: 14, color: '#666', marginBottom: 8, fontWeight: '600' },
  input: { backgroundColor: '#F1F3F5', borderRadius: 8, padding: 12, marginBottom: 20 },
  inputFake: { backgroundColor: '#F1F3F5', borderRadius: 8, padding: 12, marginBottom: 20 },
  btnAplicar: { 
    backgroundColor: '#FF8200', 
    padding: 16, 
    borderRadius: 8, 
    alignItems: 'center', 
    marginTop: 'auto', 
    marginBottom: 40 
  },
  btnAplicarTexto: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
});