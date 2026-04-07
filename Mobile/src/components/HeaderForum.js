import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";

export default function HeaderForum({ onBack }) {
  return (
    <View style={styles.wrapper}>
      <View style={styles.container}>
        
        {/* Lado esquerdo */}
        <View style={styles.left}>
          <TouchableOpacity onPress={onBack}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>

          <View style={styles.iconForum}>
            <Ionicons name="chatbubbles" size={28} color="#ffffff" />
          </View>

          <View>
            <Text style={styles.name}>Fórum</Text>
            <Text style={styles.status}>Topicos ativos</Text>
          </View>
        </View>

        {/* Lado direito */}
        <View style={styles.right}>
          <TouchableOpacity style={styles.icon}>
            <Ionicons name="search" size={22} color="#fff" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.icon}>
            <Ionicons name="add-circle-outline" size={24} color="#ffffff" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.icon}>
            <Ionicons name="ellipsis-vertical" size={22} color="#fff" />
          </TouchableOpacity>
        </View>

      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    marginTop: 35,       // espaço em cima
    paddingHorizontal: 0, // espaço lateral
  },
  container: {
    height: 70,
    backgroundColor: "#1e4f8a",
    // borderRadius: 12, // deixa moderno
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 10,
    elevation: 4,
  },
  left: {
    flexDirection: "row",
    alignItems: "center",
  },
  iconForum: {
    marginHorizontal: 8,
  },
  name: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "bold",
  },
  status: {
    color: "#ddd",
    fontSize: 12,
  },
  right: {
    flexDirection: "row",
  },
  icon: {
    marginLeft: 15,
  },
});