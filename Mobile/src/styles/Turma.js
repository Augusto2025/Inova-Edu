import { StyleSheet, Dimensions } from 'react-native';
import { COLORS } from "../components/Cores"; 

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: COLORS.backgroundCard,
  },
  
  // ESTILOS DA SELEÇÃO DE FILTROS POR CHIPS
  filtroContainer: {
    backgroundColor: COLORS.backgroundCard,
    borderBottomWidth: 1,
    borderBottomColor: '#E9ECEF',
    paddingVertical: 10,
  },
  filtroScroll: {
    paddingHorizontal: 16,
    alignItems: 'center',
    flexDirection: 'row',
  },
  chip: {
    backgroundColor: '#F1F3F5',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    marginRight: 8,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E9ECEF',
  },
  chipAtivo: {
    backgroundColor: COLORS.primary, // Fica azul (ou a cor primária) quando ativo
    borderColor: COLORS.primary,
  },
  chipTexto: {
    fontSize: 13,
    color: '#495057',
    fontWeight: '600',
  },
  chipTextoAtivo: {
    color: '#FFFFFF', // Texto fica branco quando ativo
  },
  divisorFiltro: {
    width: 1,
    height: 20,
    backgroundColor: '#DEE2E6',
    marginRight: 8,
  },

  // RESTANTE DOS ESTILOS (Mantidos conforme o padrão anterior)
  scrollContent: {
    padding: 16,
    paddingTop: 16,
  },
  turmaCard: {
    backgroundColor: COLORS.backgroundCard,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    elevation: 3,
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
  iconCircle: {
    width: 42,
    height: 42,
    borderRadius: 21,
    backgroundColor: '#E0EEFF',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 14,
  },
  professorText: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.dark,
    marginBottom: 4,
  },
  subInfoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  turnoText: {
    fontSize: 13,
    color: COLORS.textSecondary,
    fontWeight: '600',
  },
  divisor: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginHorizontal: 8,
  },
  codigoText: {
    fontSize: 13,
    color: COLORS.primary,
    fontWeight: '500',
  },
  setaContainer: {
    paddingLeft: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  vazio: {
    textAlign: 'center',
    marginTop: 40,
    color: COLORS.textSecondary,
    fontSize: 15,
    paddingHorizontal: 20,
  }
});

export default styles;