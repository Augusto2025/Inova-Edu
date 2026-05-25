import { StyleSheet, Dimensions, Platform } from 'react-native';
import { COLORS } from "../components/Cores"; // Importando as cores para manter a consistência visual

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  center: { justifyContent: 'center', alignItems: 'center' },
  
  header: {
    height: 60,
    backgroundColor: COLORS.darkBlue,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
  },
  headerTitle: { color: 'white', fontSize: 18, fontWeight: 'bold', letterSpacing: 1 },
  
  scrollContent: { padding: 16 },

  // Breadcrumb
  breadcrumbCard: {
    borderRadius: 12,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
    borderLeftWidth: 5,
    backgroundColor: COLORS.card,
    borderLeftColor: COLORS.accent,
  },
  breadcrumbPath: { fontSize: 12, color: COLORS.textSecondary },
  turmaBadge: { fontSize: 14, fontWeight: 'bold', color: COLORS.darkBlue, marginTop: 2 },
  btnAdd: { backgroundColor: COLORS.primary, width: 40, height: 40, borderRadius: 20, justifyContent: 'center', alignItems: 'center' },

  itemSub: { fontSize: 11, color: COLORS.textSecondary },

  // Cards de Projeto
  card: {
    backgroundColor: COLORS.card,
    borderRadius: 15,
    marginBottom: 16,
    overflow: 'hidden',
    elevation: 3,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  cardImage: { width: '100%', height: 140, objectFit: 'cover' },
  noImage: { backgroundColor: '#F1F5F9', justifyContent: 'center', alignItems: 'center' },
  cardBody: { padding: 15 },
  projetoNome: { fontSize: 18, fontWeight: 'bold', color: COLORS.textMain },
  projetoDesc: { fontSize: 14, color: COLORS.textSecondary, marginTop: 5, lineHeight: 20 },
  
  cardActions: {
    justifyContent: 'right',
    alignItems: 'center',
    marginTop: 15,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
  },
  btnRepo: {
    backgroundColor: COLORS.primary,
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    paddingHorizontal: 50,
    borderRadius: 8,
    gap: 8,
  },
  btnRepoText: { color: 'white', fontWeight: 'bold', fontSize: 15 },
  
  // Modal
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'flex-end' },
  modalContent: { 
    backgroundColor: 'white', 
    borderTopLeftRadius: 25, 
    borderTopRightRadius: 25, 
    padding: 25,
    minHeight: 400
  },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  modalTitle: { fontSize: 20, fontWeight: 'bold', color: COLORS.darkBlue },
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