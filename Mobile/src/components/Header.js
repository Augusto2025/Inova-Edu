import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
} from "react-native";

import { Feather } from "@expo/vector-icons";
import { useNavigation, TabActions } from "@react-navigation/native";

export default function Header({
  nomeTela,
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

        {/* ESQUERDA - Perfil com o novo Logo acima */}
        <View style={styles.left}>
          {temGoBack && (
            <TouchableOpacity
              onPress={lidarComVoltar}
              style={styles.backButton}
            >
              <Feather name="chevron-left" size={24} color="#fff" />
            </TouchableOpacity>
          )}

          <View style={styles.profileArea}>
            {/* Nome do app/logo em cima da foto */}
            <Text style={styles.logoText}>Inova-Edu</Text>
            
            <View style={styles.profileContainer}>
              <Image
                source={{ uri: "https://i.pravatar.cc/300" }}
                style={styles.profileImage}
              />
              <View>
                <Text style={styles.title}>{nomeTela}</Text>
                {/* Apenas o nome do curso aqui embaixo */}
                <Text style={styles.courseSubtitle}>
                  Tec. Desenvolvimento de Sistemas
                </Text>
              </View>
            </View>
          </View>
        </View>

        {/* NOTIFICAÇÃO */}
        <TouchableOpacity
          style={styles.notification}
          onPress={() => navigation.navigate("Notifications")}
        >
          <Feather name="bell" size={24} color="#fff" />
          <View style={styles.badge}>
            <Text style={styles.badgeText}>3</Text>
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
    backgroundColor: "#2155f3",
  },
  header: {
    paddingTop: 50,
    paddingBottom: 40,
    paddingHorizontal: 22,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-end", // Alinha melhor com o crescimento vertical do lado esquerdo
    backgroundColor: "#1459b3",
  },
  left: {
    flexDirection: "row",
    alignItems: "flex-end",
  },
  backButton: {
    marginRight: 12,
    marginBottom: 10,
  },
  profileArea: {
    flexDirection: "column",
  },
  logoText: {
    color: "#fff",
    fontSize: 20,
    marginBottom: 8,
    
    
  },
  profileContainer: {
    flexDirection: "row",
    alignItems: "center",
  },
  profileImage: {
    width: 52,
    height: 52,
    borderRadius: 26,
    marginRight: 12,
    borderWidth: 2,
    borderColor: "#fff",
  },
  title: {
    color: "#fff",
    fontSize: 22,
    fontWeight: "bold",
  },
  courseSubtitle: {
    color: "#dfe6ff",
    fontSize: 13,
    marginTop: 2,
    fontWeight: "500",
  },
  notification: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(255,255,255,0.15)",
    marginBottom: 2, // Ajuste fino de alinhamento
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
    backgroundColor: "#f5f7fb",
    borderTopLeftRadius: 35,
    borderTopRightRadius: 35,
    marginTop: -15,
  },
});