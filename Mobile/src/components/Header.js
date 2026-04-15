import React from 'react';
<<<<<<< HEAD
import { SafeAreaView } from 'react-native-safe-area-context';
import Header from '../components/Header';
=======
>>>>>>> Deploys
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { Feather } from '@expo/vector-icons';

export default function Header({ foto, escolherImagem, nomeTela }) {
  const logo = require('../../assets/LOGOBRANCO.png');

  return (
    <View style={styles.header}>
      <TouchableOpacity style={styles.backButton}>
        <Feather name="chevron-left" size={24} color="white" />
      </TouchableOpacity>

      <View style={styles.nomeTela}>
        <Text style={styles.Titulo}>{nomeTela}teste</Text>
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
<<<<<<< HEAD
 header: {
  backgroundColor: "#1459b3",
  paddingTop: 40, // 👈 AQUI
  padding: 20,
  borderBottomLeftRadius: 25,
  borderBottomRightRadius: 25,
  flexDirection: "row",
  justifyContent: "space-between",
  alignItems: "center",
},
=======
  header: {
    backgroundColor: '#1459b3',
    paddingTop: 35,
    padding: 15,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
>>>>>>> Deploys

  Titulo: {
    color: '#fff',
    fontSize: 25,
    fontWeight: 'bold',
  },

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
    marginTop: 5,
  },
});