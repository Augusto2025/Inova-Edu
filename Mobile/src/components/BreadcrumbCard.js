import React from "react";
// IMPORTANTE: Adicionado o StyleSheet que estava faltando aqui em cima
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Feather } from '@expo/vector-icons';
import { COLORS } from "./Cores"; // Importando as cores do Card para manter a consistência visual

// CORREÇÃO: Nome do componente alterado para começar com Letra Maiúscula (BreadcrumbCard)
export default function BreadcrumbCard({ titulo, itemSub, botaoAcao, aoPressionar, iconeBotao }) {
  return (
    <View style={styles.breadcrumbCard}>
      <View style={styles.breadcrumbInfo}>
        <Text style={styles.itemSub}>{itemSub}</Text>
        <Text style={styles.textPrimary}>{titulo}</Text>
      </View>
      {botaoAcao && (
        <TouchableOpacity 
          style={styles.btnActionMain} 
          onPress={aoPressionar}
          activeOpacity={0.7}
        >
          <Feather name={iconeBotao} size={20} color="white"/>
        </TouchableOpacity>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  breadcrumbCard: {
    borderRadius: 12,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'center',
    margin: 15,
    marginBottom: 0,
    borderLeftWidth: 5,
    backgroundColor: COLORS.card,
    borderLeftColor: COLORS.accent,
  },
  breadcrumbInfo: { // Adicionado para evitar quebra caso use propriedades dele
    flexDirection: 'column',
  },
  btnActionMain: { marginLeft: '30%', backgroundColor: COLORS.accent, width: 45, height: 45, borderRadius: 12, justifyContent: 'center', alignItems: 'center' },
  textPrimary: { 
    fontSize: 14, 
    fontWeight: 'bold', 
    color: COLORS.darkBlue, 
    marginTop: 2 
  },
  itemSub: { 
    fontSize: 11, 
    color: COLORS.textSecondary 
  },
});