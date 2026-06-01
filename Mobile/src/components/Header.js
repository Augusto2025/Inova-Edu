import React, { useEffect, useRef } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  Animated, // IMPORTADO: API de animação do React Native
} from "react-native";

import { Feather } from "@expo/vector-icons";
import { useNavigation, TabActions } from "@react-navigation/native";

export default function Header({
  nomeTela,
  temGoBack,
  telaDestino,
  exibirPerfil = false, 
  exibirCurva = true, 
}) {
  const navigation = useNavigation();

  // 1. CRIAR A CONFIGURAÇÃO DO VALOR DA ANIMAÇÃO (Começa em 1 = tamanho normal)
  const pulseAnim = useRef(new Animated.Value(1)).current;

  // 2. CONFIGURAR O LOOP DO PULSO
  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        // Encolhe um pouquinho ou expande (vamos expandir até 1.08x)
        Animated.timing(pulseAnim, {
          toValue: 1.08,
          duration: 1200, // Tempo de ida (1.2 segundos)
          useNativeDriver: true, // Melhora absurdamente a performance
        }),
        // Volta ao tamanho original
        Animated.timing(pulseAnim, {
          toValue: 1.0,
          duration: 1200, // Tempo de volta (1.2 segundos)
          useNativeDriver: true,
        }),
      ])
    ).start(); // Inicia o loop infinito
  }, [pulseAnim]);

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

      {/* LINHA DA LOGOMARCA COM ANIMAÇÃO */}
      <View style={styles.logoRow}>
        {/*Substituímos o <Text> comum por <Animated.Text> para aceitar o estilo de escala */}
        <Animated.Text 
          style={[
            styles.logoText, 
            { transform: [{ scale: pulseAnim }] } // Aplica a pulsação aqui!
          ]}
        >
          Inova-Edu
        </Animated.Text>
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
            
            /* CASO 2: SE FOR OUTRA TELA */
            <View style={styles.noProfileContainer}>
              <Text style={styles.title} numberOfLines={1}>{nomeTela}</Text>
              
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
  logoRow: {
    paddingTop: 55, 
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#1459b3",
    height: 90, // Forçamos uma altura fixa para a linha da logo não tremer o resto da tela ao pulsar
  },
  logoText: {
    color: '#f7941d',
    fontSize: 18,
    fontWeight: "800", 
    letterSpacing: 1, 
    opacity: 0.95,
  },
  header: {
    paddingTop: 5, // Ajustado levemente para encaixar o respiro da logo fixa
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
  curveContainer: {
    backgroundColor: "#1459b3",
  },
  curve: {
    height: 45,
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
  },
});