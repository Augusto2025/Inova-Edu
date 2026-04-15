import React from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { Feather } from '@expo/vector-icons';

export default function Header({ foto, escolherImagem, nomeTela }) {
  const logo = require('../../assets/LOGOBRANCO.png');

  return (
    <View style={styles.heade}>
      <TouchableOpacity style={styles.backButton}>
        <Feather name="chevron-left" size={24} color="white" />
      </TouchableOpacity>

      <View style={styles.nomeTela}>
        <Text style={styles.Titulo}>{nomeTela}</Text>
      </View>

      
    </View>
  );
}

const styles = StyleSheet.create({
 heade: {
  backgroundColor: "#1459b3",
  height: 90,
  paddingTop: 30, // 👈 AQUI
  padding: 20,
  paddingBottom: 15,
  flexDirection: "row",
  justifyContent: "space-between",
  alignItems: "center",
  borderBottomLeftRadius: 30,
  borderBottomRightRadius: 30,
},

  Titulo: 
   { color: '#FFF', fontSize: 18, fontWeight: 'bold', marginTop: 20 },

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

  container: {
  flex: 1,
  backgroundColor: "#eef1f5", // 🔥 mais suave
},
});

