import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';

export default function Header({ foto, escolherImagem }) {
  const logo = require('../../assets/LOGOBRANCO.png');

  return (
    <View style={styles.header}>
      <Image source={logo} style={styles.logo} />

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

        <Text style={styles.nome}>Alcides</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    backgroundColor: '#1459b3',
    paddingTop: 50,
    padding: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    
  },

  logo: {
    width: 60,
    height: 60,
    tintColor: 'white',
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