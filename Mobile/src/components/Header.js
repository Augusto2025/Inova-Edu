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
import { useNavigation } from "@react-navigation/native";
import Skeleton from "./Skeleton";

// IMPORTE A SUA FOTO LOCAL AQUI
import FotoPerfilLocal from "../../assets/pascal.jpg"; 

// 1. IMPORTANDO O CONTEXTO DO TEMA
import { ThemeContext } from "../context/ThemeContext";

const AnimatedTouchableOpacity = Animated.createAnimatedComponent(TouchableOpacity);

export default function Header({
  nomeTela,
  temGoBack, 
  telaDestino, // Mantido para compatibilidade de telas antigas
  onPressBack, // Permite passar ações customizadas de voltar
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

  // FUNÇÃO DE VOLTAR
  const lidarComVoltar = () => {
    if (onPressBack) {
      onPressBack();
      return;
    }
    if (navigation.canGoBack()) {
      navigation.goBack();
    } else {
      navigation.navigate("Home"); 
    }
  };

  return (
    <View style={[styles.wrapper, { backgroundColor: headerBgColor }]}>
      <View style={[styles.logoRow, { backgroundColor: headerBgColor }]} />

      <View style={[styles.header, { backgroundColor: headerBgColor }]}>
        
        {exibirPerfil ? (
          <View style={styles.left}>
            <View style={styles.profileContainer}>
              {carregando ? (
                <Skeleton 
                  width={52 * fontSizeScale} 
                  height={52 * fontSizeScale} 
                  borderRadius={(52 * fontSizeScale) / 2} 
                  style={{ marginRight: 12 }} 
                />
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
          </View>
        ) : (
          <View style={styles.centerContainerRow}>
            {/* BOTÃO DE VOLTAR - ESQUERDA */}
            <View style={styles.leftActionArea}>
              {temGoBack && (
                <TouchableOpacity 
                  style={styles.backButton} 
                  onPress={lidarComVoltar}
                  activeOpacity={0.7}
                >
                  <Feather name="arrow-left" size={26 * fontSizeScale} color={headerTextColor} />
                </TouchableOpacity>
              )}
            </View>

            {/* TÍTULO CENTRALIZADO */}
            <View style={styles.centerTextContainer}>
              {carregando ? (
                <Skeleton width={140 * fontSizeScale} height={20 * fontSizeScale} borderRadius={4} />
              ) : (
                <Text style={[styles.title, { color: headerTextColor, fontSize: 20 * fontSizeScale }]} numberOfLines={1}>
                  {nomeTela}
                </Text>
              )}
            </View>
          </View>
        )}

        {/* BOTÃO DE NOTIFICAÇÃO - DIREITA */}
        <View style={styles.rightActionArea}>
          {carregando ? (
            <Skeleton width={48 * fontSizeScale} height={48 * fontSizeScale} borderRadius={24 * fontSizeScale} />
          ) : (
            <AnimatedTouchableOpacity
              style={[
                styles.notification,
                { backgroundColor: isDarkMode ? theme.border : "rgba(255,255,255,0.15)" },
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

      </View>

      {/* CURVA DINÂMICA */}
      {exibirCurva && (
        <View style={[styles.curveContainer, { backgroundColor: headerBgColor }]}>
          <View style={[styles.curve, { backgroundColor: theme.background }]} />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {}, 
  logoRow: { paddingTop: 45, height: 50 }, 
  header: { 
    paddingBottom: 15, 
    paddingHorizontal: 22, 
    flexDirection: "row", 
    justifyContent: "space-between", 
    alignItems: "center" 
  },
  left: { flex: 1, marginRight: 10 },
  profileContainer: { flexDirection: "row", alignItems: "center" },
  profileImage: { width: 52, height: 52, borderRadius: 26, marginRight: 12, borderWidth: 2 },
  rightHeaderText: { flex: 1, justifyContent: 'center' },
  title: { fontWeight: "bold" },
  courseSubtitle: { marginTop: 2, fontWeight: "500" },
  
  // Alinhamentos estruturais das telas internas
  centerContainerRow: { flex: 1, flexDirection: 'row', alignItems: 'center', marginRight: 10 },
  leftActionArea: { width: 40, justifyContent: 'center', alignItems: 'flex-start' },
  centerTextContainer: { flex: 1, justifyContent: 'center', alignItems: 'flex-start', paddingLeft: 5 },
  backButton: { paddingVertical: 5, paddingRight: 5 },
  
  rightActionArea: { justifyContent: 'center', alignItems: 'center' },
  notification: { width: 48, height: 48, borderRadius: 24, justifyContent: "center", alignItems: "center" },
  badge: { position: "absolute", top: 5, right: 5, backgroundColor: "#ff4d67", justifyContent: "center", alignItems: "center" },
  badgeText: { color: "#fff", fontWeight: "bold" },
  curveContainer: {},
  curve: { height: 45, borderTopLeftRadius: 30, borderTopRightRadius: 30 },
});