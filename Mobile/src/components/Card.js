import React from 'react';
import { StyleSheet, View, Text, Image, TouchableOpacity } from 'react-native';
import { Feather } from '@expo/vector-icons';

const COLORS = {
  primary: '#005eb8',    // Azul Senac
  darkBlue: '#003d7a',   // Azul Header
  accent: '#f7941d',     // Laranja Senac
  card: '#FFFFFF',
  textMain: '#1E293B',
  textSecondary: '#64748B',
};

// Passamos propriedades genéricas: titulo, descricao, imagem, textoBotao, iconeBotao e a acaoClique
export default function Card({ 
  titulo, 
  descricao, 
  imagem, 
  textoBotao = "Entrar", // 'Entrar' será o padrão se você não enviar nada
  iconeBotao = "arrow-right", 
  aoPressionar 
}) {

  return (
    <View style={styles.card}>
      
      {/* Imagem ou Placeholder */}
      {imagem ? (
        <Image source={{ uri: imagem }} style={styles.cardImage} />
      ) : (
        <View style={[styles.cardImage, styles.noImage]}>
          <Text style={styles.textoSemImagem}>Sem Imagem</Text>
        </View>
      )}

      {/* Corpo do Card */}
      <View style={styles.cardBody}>
        <Text style={styles.cardTitulo}>{titulo}</Text>
        
        {/* Só renderiza a descrição se ela existir (Cursos não têm, Projetos têm) */}
        {descricao && (
          <Text style={styles.cardDesc} numberOfLines={2}>
            {descricao}
          </Text>
        )}

        {/* Linha separadora e Botão de Ação */}
        <View style={styles.cardActions}>
          <TouchableOpacity 
            style={styles.btnAcao} 
            onPress={aoPressionar}
            activeOpacity={0.7}
          >
            <Text style={styles.btnAcaoText}>{textoBotao}</Text>
            <Feather name={iconeBotao} size={14} color="white" />
          </TouchableOpacity>
        </View>
      </View>

    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: COLORS.card,
    borderRadius: 15,
    marginBottom: 16,
    overflow: 'hidden',
    elevation: 3,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 5,
    shadowOffset: { width: 0, height: 2 },
    width: '100%', // Mantendo a proporção da tela de cursos
    alignSelf: 'center'
  },
  cardImage: { 
    width: '100%', 
    height: 140, 
    resizeMode: 'cover'
  },
  noImage: { 
    backgroundColor: '#E9ECEF', 
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
  cardBody: { 
    padding: 15 
  },
  cardTitulo: { 
    fontSize: 18, 
    fontWeight: 'bold', 
    color: COLORS.darkBlue // Unificando com o azul escuro padrão das duas telas
  },
  cardDesc: { 
    fontSize: 14, 
    color: COLORS.textSecondary, 
    marginTop: 5, 
    lineHeight: 20 
  },
  cardActions: {
    flexDirection: 'row',
    justifyContent: 'center', 
    alignItems: 'center',
    marginTop: 15,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
  },
  btnAcao: {
    backgroundColor: COLORS.primary,
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    width: '100%', // Botão largo igual o da tela de cursos antiga
    justifyContent: 'center',
    borderRadius: 8,
    gap: 8,
  },
  btnAcaoText: { 
    color: 'white', 
    fontWeight: 'bold', 
    fontSize: 15 
  },
});