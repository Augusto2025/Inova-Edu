import { StyleSheet, Dimensions } from 'react-native';
import { COLORS } from "../components/Cores"; // Mantendo a consistência visual do seu projeto

const { width } = Dimensions.get('window');
// Calcula a largura exata para 2 colunas considerando as margens da lista
const CARD_WIDTH = (width - 48) / 2; 

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8F9FA' },
  
  filtroContainer: { width: '100%', paddingRight: 20, justifyContent: 'flex-end', alignItems: 'center', flexDirection: 'row' },
  filtroBotaoHeader: { width: 50 },
  filtroIconeTexto: { color: '#004A8D', fontSize: 45, textAlign: 'right' },

  // NOVA ESTRUTURA DE LISTA EM DUAS COLUNAS
  listaCursos: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    padding: 16,
  },
  cardCursoGrid: {
    backgroundColor: '#FFFFFF',
    width: CARD_WIDTH,
    borderRadius: 12,
    marginBottom: 16,
    overflow: 'hidden',
    // Sombras leves para destacar os blocos
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  cursoImagem: {
    width: '100%',
    height: 110,
    resizeMode: 'cover',
  },
  placeholderImagemContainer: {
    width: '100%',
    height: 110,
    backgroundColor: '#E9ECEF',
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholderIcone: {
    fontSize: 28,
  },
  textoCursoContainer: {
    padding: 12,
    justifyContent: 'center',
    minHeight: 50,
  },
  tituloCursoGrid: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333333',
    textAlign: 'center',
  },
  vazio: {
    width: '100%',
    textAlign: 'center',
    marginTop: 40,
    color: '#666',
    fontSize: 16,
  },

  // SIDEBAR (Preservado original)
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

export default styles;