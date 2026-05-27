import React from "react";
import { View, TextInput, StyleSheet } from "react-native";
import { Ionicons } from '@expo/vector-icons';

export default function BarraPesquisa() {
    return (
        <View style={styles.searchWrapper}>
            <View style={styles.searchContainer}>
                <Ionicons name="search" size={20} color="#1e4f8a" />

                <TextInput
                placeholder="Pesquisar Tópicos..."
                style={styles.input}
                placeholderTextColor="#999"
                />
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
  searchWrapper: {
    marginTop: 15,
    paddingHorizontal: 10,
    paddingBottom: 10,
  },

  searchContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#fff",
    borderRadius: 20,
    paddingHorizontal: 12,
    height: 50,
  },

  input: {
    flex: 1,
    marginLeft: 8,
    color: "#333",
  },
});

