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
      <View style={styles.header}>
        <View style={{ width: 40 }} />
        <Text style={styles.headerText}>Cursos</Text>
        <TouchableOpacity 
          style={styles.filtroBotaoHeader} 
          onPress={() => setModalVisible(true)}
        >
          <Text style={styles.filtroIconeTexto}>≡</Text>
        </TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={styles.listaCursos}>
        {cursos.length === 0 ? (
          <Text style={styles.vazio}>Nenhum resultado encontrado.</Text>
        ) : (
          cursos.map((curso) => (
            <View key={curso.id} style={styles.card}>
              
              {/* ESPAÇO DA IMAGEM (SEM IMAGEM DEFINIDA) */}
              <View style={styles.containerImagemPlaceholder}>
                <Text style={styles.textoSemImagem}>Sem Imagem</Text>
              </View>

              <View style={styles.cardContent}>
                <Text style={styles.nomeCurso}>{curso.nome_curso}</Text>
                <View style={styles.borda} />
                <TouchableOpacity style={styles.botaoEntrar} onPress={() => irParaTurmas(curso)}>
                  <Text style={styles.botaoTexto}>Entrar</Text>
                </TouchableOpacity>
              </View>
            </View>
          ))
        )}
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
  
  header: { 
    height: 70, 
    backgroundColor: '#004A8D', 
    flexDirection: 'row', 
    alignItems: 'center', 
    justifyContent: 'space-between',
    paddingHorizontal: 20,
  },
  headerText: { color: '#fff', fontSize: 20, fontWeight: 'bold' },
  filtroIconeTexto: { color: '#fff', fontSize: 30 },

  listaCursos: { padding: 20 },
  card: { 
    backgroundColor: '#fff', 
    borderRadius: 15, 
    marginBottom: 20, 
    overflow: 'hidden', // Importante para a imagem não vazar a borda arredondada
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
  },
  
  // ESTILO DO CAMPO "SEM IMAGEM"
  containerImagemPlaceholder: {
    width: '100%',
    height: 150,
    backgroundColor: '#E9ECEF', // Cinza claro
    justifyContent: 'center',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#DEE2E6'
  },
  textoSemImagem: {
    color: '#ADB5BD',
    fontSize: 14,
    fontWeight: '600',
    textTransform: 'uppercase'
  },

  cardContent: { padding: 16 },
  nomeCurso: { fontSize: 18, fontWeight: '700', color: '#004A8D', marginBottom: 8 },
  borda: { height: 1, backgroundColor: '#F1F1F1', marginVertical: 12 },
  botaoEntrar: { 
    backgroundColor: '#004A8D', 
    paddingVertical: 12, 
    borderRadius: 8, 
    alignItems: 'center' 
  },
  botaoTexto: { color: '#fff', fontWeight: 'bold' },

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