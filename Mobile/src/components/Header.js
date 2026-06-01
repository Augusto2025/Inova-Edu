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

      {/* HEADER: Agora com padding fixo e igual para todas as telas */}
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
              {/* O Tema/Título fica em cima, no mesmo nível de altura da foto da Home */}
              <Text style={styles.title} numberOfLines={1}>{nomeTela}</Text>
              
              {/* O botão de voltar fica embaixo, alinhado onde ficaria o subtítulo da Home */}
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

          <View style={styles.profileArea}>
            
            <View style={styles.profileContainer}>
              <View style={{ flexDirection: "row", alignItems: "center" }}>
                {temGoBack && (
                  <TouchableOpacity
                    onPress={lidarComVoltar}
                    style={styles.backButton}
                  >
                    <Feather name="chevron-left" size={24} color="#fff" />
                  </TouchableOpacity>
                )}

                <Image
                  source={{ uri: "https://i.pravatar.cc/300" }}
                  style={styles.profileImage}
                />

                <View>
                  <Text style={styles.title}>{nomeTela}</Text>
                  {subtitulo && (
                    <Text style={styles.courseSubtitle}>{subtitulo}</Text>
                  )}
                </View>

              </View>

        {/* NOTIFICAÇÃO (Fica travada no topo à direita em todas as telas) */}
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
        </View>
      </View>
      {/* CURVA */}
      {exibirCurva && (
        <View style={styles.curveContainer}>
          <View style={styles.curve} />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    backgroundColor: "#1459b3",
  },
  header: {
    paddingTop: 80,
    paddingBottom: 16, // Travado igual para todos!
    paddingTop: 70,
    paddingBottom: 40,
    paddingHorizontal: 22,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start", // Alinha pelo topo para a notificação não dançar
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
  
  // Estrutura das outras telas (Sem perfil)
  noProfileContainer: {
    flexDirection: "column",
    justifyContent: "center",
    height: 52, // Força ter EXATAMENTE a mesma altura que a foto de perfil da Home
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

  // Textos Globais
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

  // Botão de Notificação
  notification: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(255,255,255,0.15)",
    alignSelf: "center", // Mantém centralizado verticalmente com o bloco da esquerda
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

  // Sistema da Curva
  curveContainer: {
    backgroundColor: "#1459b3",
  },
  curve: {
    height: 45,
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