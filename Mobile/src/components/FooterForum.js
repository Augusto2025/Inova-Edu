import React from "react";
import { View, StyleSheet } from "react-native";

export default function Footer() {
  return (
    <View style={styles.footer}>
      
      <View style={styles.item}></View>
      <View style={styles.item}></View>
      <View style={styles.item}></View>

    </View>
  );
}

const styles = StyleSheet.create({
  footer: {
    position: "absolute",
    bottom: 0,
    left: 0,
    width: "100%",
    height: 70,
    backgroundColor: "blue",
    marginBottom: 50,
    // marginTop: 20,
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
  },

  item: {
    width: 40,
    height: 40,
    backgroundColor: "white", // só pra você enxergar os espaços
    borderRadius: 20,
  },
});