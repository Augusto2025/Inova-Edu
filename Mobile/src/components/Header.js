import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
} from "react-native";

import { Feather, Ionicons } from "@expo/vector-icons";
import { COLORS } from "./Cores"; // Importando as cores para manter a consistência visual
import { useNavigation, TabActions } from "@react-navigation/native";

export default function Header({
  nomeTela,
  subtitulo,
  temGoBack,
  telaDestino,
}) {

  const navigation = useNavigation();

  const lidarComVoltar = () => {
    if (telaDestino) {
      navigation.dispatch(TabActions.jumpTo(telaDestino));
    } else {
      navigation.goBack();
    }
  };

  return (
    <View style={styles.wrapper}>

      {/* HEADER */}
      <View style={styles.header}>

        {/* ESQUERDA */}
        <View style={styles.left}>

          {temGoBack ? (
            <TouchableOpacity
              onPress={lidarComVoltar}
              style={styles.backButton}
            >
              <Feather
                name="chevron-left"
                size={24}
                color="#fff"
              />
            </TouchableOpacity>
          ) : null}

          <View>
            <Text style={styles.title}>
              {nomeTela}
            </Text>

            {subtitulo ? (
              <View style={styles.subtitleRow}>
                <Ionicons
                  name="location-sharp"
                  size={14}
                  color="#dfe6ff"
                />

                <Text style={styles.subtitle}>
                  {subtitulo}
                </Text>
              </View>
            ) : null}
          </View>
        </View>

        {/* NOTIFICAÇÃO */}
        <TouchableOpacity
        style={styles.notification}
          onPress={() => navigation.navigate("Notifications")}>
          <Feather
            name="bell"
            size={24}
            color="#fff"
          />

          <View style={styles.badge}>
            <Text style={styles.badgeText}>
              3
            </Text>
          </View>
        </TouchableOpacity>
      </View>

      {/* CURVA */}
      <View style={styles.curve} />
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    backgroundColor: COLORS.primary,
  },

  header: {
    paddingTop: 60,
    paddingBottom: 45,
    paddingHorizontal: 22,

    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",

    backgroundColor: COLORS.primary,
  },

  left: {
    flexDirection: "row",
    alignItems: "center",
  },

  backButton: {
    marginRight: 12,
  },

  title: {
    color: "#fff",
    fontSize: 25,
    fontWeight: "bold",
  },

  subtitleRow: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 4,
  },

  subtitle: {
    color: "#dfe6ff",
    marginLeft: 4,
    fontSize: 14,
  },

  notification: {
    width: 48,
    height: 48,

    borderRadius: 24,

    justifyContent: "center",
    alignItems: "center",

    backgroundColor: "rgba(255,255,255,0.15)",
  },

  badge: {
    position: "absolute",
    top: 5,
    right: 5,

    backgroundColor: "#ff4d67",

    width: 18,
    height: 18,

    borderRadius: 9,

    justifyContent: "center",
    alignItems: "center",
  },

  badgeText: {
    color: "#fff",
    fontSize: 10,
    fontWeight: "bold",
  },

  curve: {
    height: 35,

    backgroundColor: COLORS.background,

    borderTopLeftRadius: 35,
    borderTopRightRadius: 35,

    marginTop: -15,
  },
});