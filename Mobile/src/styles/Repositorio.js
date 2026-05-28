import { StyleSheet, Dimensions, Platform } from 'react-native';
import { COLORS } from "../components/Cores"; // Importando as cores para manter a consistência visual

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  center: { justifyContent: 'center', alignItems: 'center' },
  
  header: {
    height: 60,
    backgroundColor: COLORS.dark,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 15,
    elevation: 4,
  },
  headerTitle: { color: 'white', fontSize: 18, fontWeight: 'bold' },
  backButton: { width: 40 },
  downloadHeader: { width: 40, alignItems: 'flex-end' },
  
  scrollContent: { padding: 16, paddingBottom: 40 },

  // Breadcrumb
  breadcrumbCard: {
    backgroundColor: COLORS.backgroundCard,
    borderRadius: 12,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
    borderLeftWidth: 5,
    borderLeftColor: COLORS.accent,
  },
  breadcrumbPath: { fontSize: 11, color: COLORS.textSecondary },
  projetoBadge: { fontSize: 15, fontWeight: 'bold', color: COLORS.dark, marginTop: 2 },
  btnActionMain: { width: 45, height: 45, borderRadius: 12, justifyContent: 'center', alignItems: 'center' },

  // Listagem
  sectionHeader: { 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'center', 
    marginBottom: 12,
    paddingHorizontal: 4
  },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', color: COLORS.textMain },
  btnToggleText: { color: COLORS.primary, fontWeight: 'bold', fontSize: 13 },
  btnUploadSmall: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    backgroundColor: 'white', 
    paddingHorizontal: 10, 
    paddingVertical: 5, 
    borderRadius: 6,
    borderWidth: 1,
    borderColor: COLORS.primary
  },
  btnUploadSmallText: { color: COLORS.primary, fontSize: 12, fontWeight: 'bold', marginLeft: 5 },

  itemCard: {
    backgroundColor: COLORS.backgroundCard,
    borderRadius: 12,
    padding: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 10,
    elevation: 1,
  },
  folderBorder: { borderLeftWidth: 4, borderLeftColor: COLORS.primary },
  fileBorder: { borderLeftWidth: 4, borderLeftColor: COLORS.textSecondary },
  
  itemInfo: { flexDirection: 'row', alignItems: 'center', flex: 1 },
  itemName: { fontSize: 14, fontWeight: '600', color: COLORS.textMain },
  itemSub: { fontSize: 11, color: COLORS.textSecondary },
  checkboxPlaceholder: { 
    width: 20, 
    height: 20, 
    borderRadius: 4, 
    borderWidth: 2, 
    borderColor: COLORS.primary, 
    marginRight: 10 
  },

  // Mass Actions
  massActions: { marginTop: 10, alignItems: 'center' },
  btnMassDelete: { 
    backgroundColor: '#FEE2E2', 
    padding: 12, 
    borderRadius: 8, 
    width: '100%', 
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.danger
  },
  btnMassDeleteText: { color: COLORS.danger, fontWeight: 'bold' },

  // Modal
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'center', padding: 20 },
  modalContent: { backgroundColor: 'white', borderRadius: 20, padding: 20 },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  modalTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.dark },
  label: { fontSize: 14, color: COLORS.textMain, marginBottom: 8, fontWeight: '500' },
  input: {
    backgroundColor: '#F8FAFC',
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 10,
    padding: 12,
    marginBottom: 20,
    color: COLORS.textMain
  },
  modalFooter: { flexDirection: 'row', gap: 10 },
  btnCancel: { flex: 1, padding: 14, borderRadius: 10, alignItems: 'center', backgroundColor: '#F1F5F9' },
  btnCancelText: { color: COLORS.textSecondary, fontWeight: 'bold' },
  btnSave: { flex: 2, padding: 14, borderRadius: 10, alignItems: 'center', backgroundColor: COLORS.accent },
  btnSaveText: { color: 'white', fontWeight: 'bold' }
});

export default styles;