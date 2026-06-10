import React, { useEffect, useRef } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  Animated,
} from "react-native";
import { Feather } from "@expo/vector-icons";
import { useNavigation, TabActions } from "@react-navigation/native";

const AnimatedTouchableOpacity = Animated.createAnimatedComponent(TouchableOpacity);

export default function Header({
  nomeTela,
  temGoBack,
  telaDestino,
  exibirPerfil = false, 
  exibirCurva = true, 
  quantidadeNotificacoes = 0, // CORRIGIDO: Recebe do componente pai
  aoClicarNoSino,            // CORRIGIDO: Executa função para mudar o estado local da Home
}) {
  const navigation = useNavigation();
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    // Só deixa ativo o efeito de pulsação se houver notificações pendentes
    if (quantidadeNotificacoes > 0) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, { toValue: 1.1, duration: 1000, useNativeDriver: true }),
          Animated.timing(pulseAnim, { toValue: 1.0, duration: 1000, useNativeDriver: true }),
        ])
      ).start();
    } else {
      pulseAnim.setValue(1); // Mantém o tamanho original caso esteja zerado
    }
  }, [pulseAnim, quantidadeNotificacoes]);

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
      <View style={styles.logoRow}>
        {/* <Text style={styles.logoText}>Inova-Edu</Text> */}
      </View>

      <View style={styles.header}>
        <View style={styles.left}>
          {exibirPerfil ? (
            <View style={styles.profileContainer}>
              <Image source={{ uri: "https://i.pravatar.cc/300" }} style={styles.profileImage} />
              <View style={styles.rightHeaderText}>
                <Text style={styles.title} numberOfLines={1}>{nomeTela}</Text>
                <Text style={styles.courseSubtitle} numberOfLines={1}>
                  Tec. Desenvolvimento de Sistemas
                </Text>
              </View>
            </View>
          ) : (
            <View style={styles.noProfileContainer}>
              <Text style={styles.title} numberOfLines={1}>{nomeTela}</Text>
              {temGoBack && (
                <TouchableOpacity onPress={lidarComVoltar} style={styles.backButtonUnder} activeOpacity={0.7}>
                  <Feather name="arrow-left" size={16} color="#dfe6ff" />
                  <Text style={styles.backButtonText}>Voltar</Text>
                </TouchableOpacity>
              )}
            </View>
          )}
        </View>

        {/* BOTÃO DO SINO INTEIRO COM FEEDBACK DINÂMICO */}
        <AnimatedTouchableOpacity
          style={[
            styles.notification,
            quantidadeNotificacoes > 0 && { transform: [{ scale: pulseAnim }] }
          ]}
          onPress={() => {
            if (aoClicarNoSino) aoClicarNoSino(); // Zera as notificações na Home
            navigation.navigate("Notifications");
          }}
          activeOpacity={0.8}
        >
          <Feather name="bell" size={24} color="#fff" />
          
          {/* CORRIGIDO: O número vermelho do Badge some totalmente se for igual a 0 */}
          {quantidadeNotificacoes > 0 && (
            <View style={styles.badge}>
              <Text style={styles.badgeText}>{quantidadeNotificacoes}</Text>
            </View>
          )}
        </AnimatedTouchableOpacity>
      </View>

      {exibirCurva && (
        <View style={styles.curveContainer}>
          <View style={styles.curve} />
        </View>
      )}
    </View>
  );
}

// ... Mantive os mesmos estilos abaixo
const styles = StyleSheet.create({
  wrapper: { backgroundColor: "#1459b3" },
  logoRow: { paddingTop: 55, alignItems: "center", justifyContent: "center", backgroundColor: "#1459b3", height: 90 },
  logoText: { color: '#f7941d', fontSize: 18, fontWeight: "800", letterSpacing: 1, opacity: 0.95 },
  header: { paddingTop: 5, paddingBottom: 19, paddingHorizontal: 22, flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start", backgroundColor: "#1459b3" },
  left: { flex: 1, marginRight: 10 },
  profileContainer: { flexDirection: "row", alignItems: "center" },
  profileImage: { width: 52, height: 52, borderRadius: 26, marginRight: 12, borderWidth: 2, borderColor: "#fff" },
  rightHeaderText: { flex: 1 },
  noProfileContainer: { flexDirection: "column", justifyContent: "center", height: 52 },
  backButtonUnder: { flexDirection: "row", alignItems: "center", marginTop: 4 },
  backButtonText: { color: "#dfe6ff", fontSize: 13, fontWeight: "500", marginLeft: 4 },
  title: { color: "#fff", fontSize: 22, fontWeight: "bold" },
  courseSubtitle: { color: "#dfe6ff", fontSize: 12, marginTop: 2, fontWeight: "500" },
  notification: { width: 48, height: 48, borderRadius: 24, justifyContent: "center", alignItems: "center", backgroundColor: "rgba(255,255,255,0.15)", alignSelf: "center" },
  badge: { position: "absolute", top: 5, right: 5, backgroundColor: "#ff4d67", width: 18, height: 18, borderRadius: 9, justifyContent: "center", alignItems: "center" },
  badgeText: { color: "#fff", fontSize: 10, fontWeight: "bold" },
  curveContainer: { backgroundColor: "#1459b3" },
  curve: { height: 45, backgroundColor: '#FFFFFF', borderTopLeftRadius: 30, borderTopRightRadius: 30 },
});