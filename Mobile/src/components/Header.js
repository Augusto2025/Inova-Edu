import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
} from "react-native";

import { Feather, Ionicons } from "@expo/vector-icons";
import { COLORS } from "./Cores"; // Importando as cores para manter a consistência visual
import { useNavigation, TabActions } from "@react-navigation/native";

export default function Header({
  nomeTela,
  temGoBack,
  telaDestino,
  exibirPerfil = false, 
  exibirCurva = true, 
}) {
  const navigation = useNavigation();

  const lidarComVoltar = () => {
    if (telaDestino) {
      try {
        navigation.dispatch(TabActions.jumpTo(telaDestino));
      } catch (e) {
        navigation.navigate(telaDestino);
      }
    } else {
      navigation.goBack();
    }
  };

  return (
    <View style={styles.wrapper}>

      {/* LINHA DA LOGOMARCA: Adicionada no topo do Header */}
      <View style={styles.logoRow}>
        <Text style={styles.logoText}>Inova-Edu</Text>
      </View>

      {/* CONTEÚDO DO HEADER */}
      <View style={styles.header}>

        {/* ESQUERDA */}
        <View style={styles.left}>
          
          {/* CASO 1: SE FOR A HOME (exibirPerfil === true) */}
          {exibirPerfil ? (
            <View style={styles.profileContainer}>
              <Image
                source={{ uri: "https://i.pravatar.cc/300" }}
                style={styles.profileImage}
              />
              <View style={styles.rightHeaderText}>
                <Text style={styles.title} numberOfLines={1}>{nomeTela}</Text>
                <Text style={styles.courseSubtitle} numberOfLines={1}>
                  Tec. Desenvolvimento de Sistemas
                </Text>
              </View>
            </View>
          ) : (
            
            /* CASO 2: SE FOR OUTRA TELA (Sem perfil, com botão de voltar embaixo do tema) */
            <View style={styles.noProfileContainer}>
              {/* O Tema/Título fica em cima */}
              <Text style={styles.title} numberOfLines={1}>{nomeTela}</Text>
              
              {/* O botão de voltar fica embaixo */}
              {temGoBack && (
                <TouchableOpacity
                  onPress={lidarComVoltar}
                  style={styles.backButtonUnder}
                  activeOpacity={0.7}
                >
                  <Feather name="arrow-left" size={16} color="#dfe6ff" />
                  <Text style={styles.backButtonText}>Voltar</Text>
                </TouchableOpacity>
              )}
            </View>
          )}

        </View>

        {/* NOTIFICAÇÃO (Fica alinhada com o conteúdo inferior) */}
        <TouchableOpacity
          style={styles.notification}
          onPress={() => navigation.navigate("Notifications")}
        >
          <Feather name="bell" size={24} color="#fff" />
          <View style={styles.badge}>
            <Text style={styles.badgeText}>3</Text>
          </View>
        </TouchableOpacity>
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
          </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    backgroundColor: "#1459b3",
  },
  // Estilização da nova linha da logo
  logoRow: {
    paddingTop: 55, // Afasta dos elementos físicos/notch do celular
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#1459b3",
  },
  logoText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "800", // Bem marcante
    letterSpacing: 1, // Espaçamento elegante entre as letras
    opacity: 0.95,
  },
  header: {
    paddingTop: 15, // Reduzido o paddingTop aqui porque a logo já ocupa o topo
    paddingBottom: 19, 
    paddingHorizontal: 22,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start", 
    backgroundColor: "#1459b3",
  },
  left: {
    flex: 1,
    marginRight: 10,
    flexDirection: "column",
    alignItems: "flex-start",
  },
  backButton: {
    marginRight: 5,
  },
  profileArea: {
    flexDirection: "column",
  },
  logoText: {
    color: "#fff",
    fontSize: 25,
    marginBottom: 8,
    alignItems: "center",
  },
  profileContainer: {
    width: "100%",
    flexDirection: "row",
    justifyContent: "space-between",
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
  rightHeaderText: {
    flex: 1,
  },
  noProfileContainer: {
    flexDirection: "column",
    justifyContent: "center",
    height: 52, 
  },
  backButtonUnder: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 4,
  },
  backButtonText: {
    color: "#dfe6ff",
    fontSize: 13,
    fontWeight: "500",
    marginLeft: 4,
  },
  title: {
    color: "#fff",
    fontSize: 22,
    fontWeight: "bold",
  },
  courseSubtitle: {
    color: "#dfe6ff",
    fontSize: 12,
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
    alignSelf: "center", 
  },
  badge: {
    position: "absolute",
    top: 5,
    right: 5,
    backgroundColor: COLORS.alert,
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
  curveContainer: {
    backgroundColor: "#1459b3",
  },
  curve: {
    height: 35,
    backgroundColor: "#f5f7fb",
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
    height: 35,
    backgroundColor: COLORS.background,
    borderTopLeftRadius: 35,
    borderTopRightRadius: 35,
    marginTop: -15,
  },
});