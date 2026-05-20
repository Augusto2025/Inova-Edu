import React from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { useNavigation, TabActions } from '@react-navigation/native';
import { Feather } from '@expo/vector-icons';

export default function Header({ foto, escolherImagem, nomeTela, temGoBack, telaDestino }) {
  const logo = require('../../assets/LOGOBRANCO.png');
  const navigation = useNavigation(); // 2. Inicializa o controle de navegação

  // Função que decide para onde vai ao clicar no botão de voltar
  const lidarComVoltar = () => {
    if (telaDestino) {
      // Se você definiu uma tela específica, ele vai para ela
      navigation.dispatch(TabActions.jumpTo(telaDestino));
    } else {
      // Se não definiu, ele só volta para a tela imediatamente anterior
      navigation.goBack();
    }
  };

  return (
    <View style={styles.header}>
      {temGoBack ? (
        <TouchableOpacity style={styles.backButton} onPress={lidarComVoltar}>
          <Feather name="chevron-left" size={24} color="white" />
        </TouchableOpacity>
      ) : (
        // Esse View vazio com largura 24 serve para o título não desalinhar do centro
        <View style={{ width: 24 }} /> 
      )}

      <View style={styles.nomeTela}>
        <Text style={styles.Titulo}>{nomeTela}</Text>
      </View>

      <View style={styles.user}>
        <TouchableOpacity onPress={escolherImagem}>
          {foto ? (
            <Image source={{ uri: foto }} style={styles.avatar} />
          ) : (
            <View style={styles.avatarFallback}>
              <Text style={styles.letra}>A</Text>
            </View>
          )}
        </TouchableOpacity>
      </View>

      
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    backgroundColor: '#1459b3',
    paddingTop: 35,
    padding: 15,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  Titulo: 
  { color: '#FFF', fontSize: 18, fontWeight: 'bold',},

  user: {
    alignItems: 'center',
  },

  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    borderWidth: 2,
    borderColor: '#fff',
  },

  avatarFallback: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: '#6c63ff',
    justifyContent: 'center',
    alignItems: 'center',
  },

  letra: {
    color: '#fff',
    fontWeight: 'bold',
  },

  nome: {
    color: '#fff',
  },

  container: {
  flex: 1,
  backgroundColor: "#eef1f5",
},
});