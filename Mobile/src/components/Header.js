import React, { useEffect, useRef, useContext } from "react";
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
import Skeleton from "./Skeleton";

// IMPORTE A SUA FOTO LOCAL AQUI
import FotoPerfilLocal from "../../assets/pascal.jpg"; 

// 1. IMPORTANDO O CONTEXTO DO TEMA
import { ThemeContext } from "../context/ThemeContext";

const AnimatedTouchableOpacity = Animated.createAnimatedComponent(TouchableOpacity);

export default function Header({
  nomeTela,
  temGoBack,
  telaDestino,
  exibirPerfil = false, 
  exibirCurva = true, 
  quantidadeNotificacoes = 0, 
  aoClicarNoSino,            
  carregando = false, 
}) {
  const navigation = useNavigation();
  const pulseAnim = useRef(new Animated.Value(1)).current;

  // 2. RESGATANDO AS VARIÁVEIS DE TEMA COM PROTEÇÃO (FALLBACK)
  const context = useContext(ThemeContext);
  const theme = context?.theme || { background: '#F8FAFC', card: '#FFFFFF', text: '#333333', border: '#E2E8F0' };
  const fontSizeScale = context?.fontSizeScale || 1;
  const isDarkMode = context?.isDarkMode || false;

  // Cores dinâmicas para o Header
  const headerBgColor = isDarkMode ? theme.card : "#1459b3";
  const headerTextColor = isDarkMode ? theme.text : "#fff";
  const headerSubTextColor = isDarkMode ? theme.text : "#dfe6ff";

  useEffect(() => {
    if (quantidadeNotificacoes > 0 && !carregando) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, { toValue: 1.1, duration: 1000, useNativeDriver: true }),
          Animated.timing(pulseAnim, { toValue: 1.0, duration: 1000, useNativeDriver: true }),
        ])
      ).start();
    } else {
      pulseAnim.setValue(1); 
    }
  }, [pulseAnim, quantidadeNotificacoes, carregando]);

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
    // Fundo principal adaptável
    <View style={[styles.wrapper, { backgroundColor: headerBgColor }]}>
      <View style={[styles.logoRow, { backgroundColor: headerBgColor }]} />

      <View style={[styles.header, { backgroundColor: headerBgColor }]}>
        <View style={styles.left}>
          {exibirPerfil ? (
            <View style={styles.profileContainer}>
              
              {carregando ? (
                <Skeleton width={52 * fontSizeScale} height={52 * fontSizeScale} borderRadius={(52 * fontSizeScale)/2} style={{ marginRight: 12 }} />
              ) : (
                <Image source={FotoPerfilLocal} style={[styles.profileImage, { borderColor: headerBgColor }]} />
              )}

              <View style={styles.rightHeaderText}>
                {carregando ? (
                  <View style={{ gap: 6, justifyContent: 'center', height: 52 * fontSizeScale }}>
                    <Skeleton width={110 * fontSizeScale} height={16 * fontSizeScale} borderRadius={4} />
                    <Skeleton width={150 * fontSizeScale} height={12 * fontSizeScale} borderRadius={4} />
                  </View>
                ) : (
                  <>
                    {/* Textos com escala de fonte e cor adaptável */}
                    <Text style={[styles.title, { color: headerTextColor, fontSize: 22 * fontSizeScale }]} numberOfLines={1}>
                      {nomeTela}
                    </Text>
                    <Text style={[styles.courseSubtitle, { color: headerSubTextColor, fontSize: 12 * fontSizeScale, opacity: isDarkMode ? 0.7 : 1 }]} numberOfLines={1}>
                      Tec. Desenvolvimento de Sistemas
                    </Text>
                  </>
                )}
              </View>
            </View>
          ) : (
            <View style={styles.noProfileContainer}>
              {carregando ? (
                <Skeleton width={140 * fontSizeScale} height={20 * fontSizeScale} borderRadius={4} />
              ) : (
                <Text style={[styles.title, { color: headerTextColor, fontSize: 22 * fontSizeScale }]} numberOfLines={1}>
                  {nomeTela}
                </Text>
              )}
            </View>
          )}
        </View>

        {carregando ? (
          <Skeleton width={48 * fontSizeScale} height={48 * fontSizeScale} borderRadius={24 * fontSizeScale} style={{ alignSelf: 'center' }} />
        ) : (
          <AnimatedTouchableOpacity
            style={[
              styles.notification,
              { backgroundColor: isDarkMode ? theme.border : "rgba(255,255,255,0.15)" }, // Fundo do botão ajustado
              quantidadeNotificacoes > 0 && { transform: [{ scale: pulseAnim }] }
            ]}
            onPress={() => {
              if (aoClicarNoSino) aoClicarNoSino(); 
              navigation.navigate("Notifications");
            }}
            activeOpacity={0.8}
          >
            <Feather name="bell" size={24 * fontSizeScale} color={headerTextColor} />
            {quantidadeNotificacoes > 0 && (
              <View style={[styles.badge, { width: 18 * fontSizeScale, height: 18 * fontSizeScale, borderRadius: 9 * fontSizeScale }]}>
                <Text style={[styles.badgeText, { fontSize: 10 * fontSizeScale }]}>{quantidadeNotificacoes}</Text>
              </View>
            )}
          </AnimatedTouchableOpacity>
        )}
      </View>

      {/* CURVA DINÂMICA: O fundo de trás assume a cor do header, a curva em si assume a cor da tela */}
      {exibirCurva && (
        <View style={[styles.curveContainer, { backgroundColor: headerBgColor }]}>
          <View style={[styles.curve, { backgroundColor: theme.background }]} />
        </View>
      )}
    </View>
  );
}

// Estilos limpos (cores estáticas e dinâmicas tratadas inline no componente)
const styles = StyleSheet.create({
  wrapper: {}, 
  logoRow: { paddingTop: 70, height: 60 },
  header: { paddingTop: 5, paddingBottom: 19, paddingHorizontal: 22, flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start" },
  left: { flex: 1, marginRight: 10 },
  profileContainer: { flexDirection: "row", alignItems: "center" },
  profileImage: { width: 52, height: 52, borderRadius: 26, marginRight: 12, borderWidth: 2 },
  rightHeaderText: { flex: 1 },
  noProfileContainer: { flexDirection: "column", justifyContent: "center", height: 52 },
  title: { fontWeight: "bold" },
  courseSubtitle: { marginTop: 2, fontWeight: "500" },
  notification: { width: 48, height: 48, borderRadius: 24, justifyContent: "center", alignItems: "center", alignSelf: "center" },
  badge: { position: "absolute", top: 5, right: 5, backgroundColor: "#ff4d67", justifyContent: "center", alignItems: "center" },
  badgeText: { color: "#fff", fontWeight: "bold" },
  curveContainer: {},
  curve: { height: 45, borderTopLeftRadius: 30, borderTopRightRadius: 30 },

});