import { StyleSheet } from "react-native";
import { COLORS } from "../components/Cores";

const styles = StyleSheet.create({
  container: { flex: 1 },
  calendarContainer: { backgroundColor: '#FFF', margin: 15, borderRadius: 20, padding: 10, elevation: 4 },
  eventSection: { paddingHorizontal: 20 },
  eventSectionTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 15, color: COLORS.primary },
  eventCard: {
    backgroundColor: '#FFF',
    flexDirection: 'row',
    padding: 12,
    borderRadius: 15,
    marginBottom: 12,
    alignItems: 'center',
    elevation: 2,
  },
  dateBadge: { width: 55, height: 60, borderWidth: 1, borderRadius: 8, overflow: 'hidden', marginRight: 15 },
  dateBadgeTop: { height: '40%', justifyContent: 'center', alignItems: 'center' },
  monthText: { color: '#FFF', fontSize: 10, fontWeight: 'bold' },
  dateBadgeBottom: { height: '60%', justifyContent: 'center', alignItems: 'center', backgroundColor: '#FFF' },
  dayText: { fontSize: 18, fontWeight: 'bold' },
  eventInfo: { flex: 1 },
  eventTitle: { fontSize: 16, fontWeight: 'bold', color: COLORS.primary },
  eventTimeInfo: { fontSize: 13, color: '#666', marginTop: 4 },
  statusDot: { width: 8, height: 8, borderRadius: 4, marginLeft: 10 },
  
  // Estilos do Modal
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center', alignItems: 'center' },
  modalContent: { width: '85%', backgroundColor: 'white', borderRadius: 20, overflow: 'hidden' },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 20 },
  modalTitle: { color: 'white', fontSize: 18, fontWeight: 'bold', flex: 1 },
  modalBody: { padding: 20 },
  modalInfoRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  modalInfoText: { marginLeft: 10, fontSize: 16, color: '#444' },
  descriptionTitle: { fontWeight: 'bold', marginTop: 15, fontSize: 16, color: '#333' },
  descriptionText: { marginTop: 5, fontSize: 14, color: '#666', lineHeight: 20 },
  closeButton: { backgroundColor: '#1459b3', marginTop: 20, padding: 12, borderRadius: 10, alignItems: 'center' },
  closeButtonText: { color: 'white', fontWeight: 'bold', fontSize: 16 }
});

export default styles;