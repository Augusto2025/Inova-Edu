import { StyleSheet, Dimensions } from 'react-native';
import { COLORS } from "../components/Cores"; 

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.backgroundCard },
  center: { justifyContent: 'center', alignItems: 'center' },
  
  scrollContent: { 
    padding: 16,
    marginTop: 10, 
  },
  // NOVO CARD DE PROJETO NO ESTILO DA TELA DE TURMAS
  projetoCard: {
    backgroundColor: COLORS.backgroundCard,
    borderRadius: 12,
    padding: 12,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    elevation: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
  },
  cardInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  projetoImagemQuadrada: {
    width: 65,
    height: 65,
    borderRadius: 8, // Mantém o formato quadrado com cantos suavemente lapidados
    marginRight: 14,
    resizeMode: 'cover',
  },
  placeholderImagemContainer: {
    backgroundColor: '#E2E8F0',
    justifyContent: 'center',
    alignItems: 'center',
  },
  projetoNome: { 
    fontSize: 16, 
    fontWeight: '700', 
    color: COLORS.dark,
    marginBottom: 4,
  },
  projetoDesc: { 
    fontSize: 13, 
    color: COLORS.textSecondary, 
    lineHeight: 18,
    paddingRight: 4 
  },
  setaContainer: {
    paddingLeft: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  
  // Modal (Preservado original)
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'flex-end' },
  modalContent: { 
    backgroundColor: 'white', 
    borderTopLeftRadius: 25, 
    borderTopRightRadius: 25, 
    padding: 25,
    minHeight: 400
  },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  modalTitle: { fontSize: 20, fontWeight: 'bold', color: COLORS.dark },
  input: {
    backgroundColor: '#F8FAFC',
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 10,
    padding: 12,
    marginBottom: 15,
    color: COLORS.textMain
  },
  uploadBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: COLORS.primary,
    borderStyle: 'dashed',
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
    gap: 10
  },
  uploadText: { color: COLORS.primary, fontWeight: 'bold' },
  btnSave: { backgroundColor: COLORS.accent, padding: 16, borderRadius: 12, alignItems: 'center' },
  btnSaveText: { color: 'white', fontWeight: 'bold', fontSize: 16 }
});

export default styles;