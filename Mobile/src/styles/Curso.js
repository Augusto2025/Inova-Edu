import { StyleSheet, Dimensions } from 'react-native';
import { COLORS } from "../components/Cores"; // Importando as cores para manter a consistência visual
const { width } = Dimensions.get('window');

// Criamos e exportamos como PADRÃO (default)
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8F9FA' },
  
  filtroContainer: { width: '100%', paddingRight: 20, justifyContent: 'flex-end', alignItems: 'center', flexDirection: 'row' },
  filtroBotaoHeader: { width: 50 },
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

export default styles;