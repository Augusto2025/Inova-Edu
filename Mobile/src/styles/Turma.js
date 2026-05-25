import { StyleSheet, Dimensions, Platform } from 'react-native';
import { COLORS } from "../components/Cores"; // Importando as cores para manter a consistência visual

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  center: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 15,
    color: COLORS.primary,
    fontSize: 14,
    fontWeight: '600',
  },

  scrollContent: {
    padding: 16,
    paddingTop: 24,
  },
  yearSection: {
    marginBottom: 14,
  },
  yearHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: COLORS.card,
    padding: 18,
    borderRadius: 12,
    borderLeftWidth: 5,
    borderLeftColor: COLORS.primary, // Indicador azul lateral
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
  },
  activeYearHeader: {
    borderBottomLeftRadius: 0,
    borderBottomRightRadius: 0,
    borderLeftColor: COLORS.accent, // Muda para laranja quando aberto
  },
  yearRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  yearLabel: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.primary,
  },
  activeYearLabel: {
    color: COLORS.textMain,
  },
  cardsContainer: {
    backgroundColor: '#D1DEE9', // Fundo azulado interno
    padding: 10,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
  },
  turmaCard: {
    backgroundColor: COLORS.card,
    borderRadius: 10,
    padding: 15,
    marginBottom: 8,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  cardInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  iconCircle: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: '#E0EEFF',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  codigoText: {
    fontSize: 15,
    fontWeight: '700',
    color: COLORS.darkBlue,
  },
  turnoText: {
    fontSize: 12,
    color: COLORS.textSecondary,
    fontWeight: '500',
  },
  actionButton: {
    backgroundColor: COLORS.primary,
    paddingVertical: 8,
    paddingHorizontal: 14,
    borderRadius: 8,
    flexDirection: 'row',
    alignItems: 'center',
  },
  actionButtonText: {
    color: 'white',
    fontSize: 12,
    fontWeight: 'bold',
    marginRight: 5,
  },
});

export default styles;