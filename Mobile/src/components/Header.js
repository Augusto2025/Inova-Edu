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

<<<<<<< HEAD
// IMPORTAÇÃO DA SUA FOTO LOCAL
=======
// IMPORTE A SUA FOTO LOCAL AQUI
>>>>>>> Deploys
import FotoPerfilLocal from "../../assets/pascal.jpg"; 

// 1. IMPORTANDO O CONTEXTO DO TEMA
import { ThemeContext } from "../context/ThemeContext";

const AnimatedTouchableOpacity = Animated.createAnimatedComponent(TouchableOpacity);

export default function Header({
  nomeTela,
  temGoBack, 
  telaDestino, // Pode manter para compatibilidade de telas antigas
  onPressBack, // 🌟 NOVA PROPRIEDADE: Permite passar ações customizadas de voltar
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

  // 🌟 FUNÇÃO DE VOLTAR CORRIGIDA
  const lidarComVoltar = () => {
    // 1º Cenário: Se a tela passou uma função customizada (ex: lidarComVoltar), executa ela
    if (onPressBack) {
      onPressBack();
      return;
    }

    // 2º Cenário: Se não há função customizada, limpa o uso de rotas fixas e usa o histórico nativo
    if (navigation.canGoBack()) {
      navigation.goBack();
    } else {
      navigation.navigate("Home"); // Fallback seguro
    }
  };

  return (
    // Fundo principal adaptável
    <View style={[styles.wrapper, { backgroundColor: headerBgColor }]}>
      <View style={[styles.logoRow, { backgroundColor: headerBgColor }]} />

<<<<<<< HEAD
      <View style={styles.header}>
        
        {/* SE FOR PERFIL (HOME): Usa o layout padrão estendido na linha */}
        {exibirPerfil ? (
          <View style={styles.homeProfileRow}>
            <View style={styles.profileContainer}>
=======
      <View style={[styles.header, { backgroundColor: headerBgColor }]}>
        <View style={styles.left}>
          {exibirPerfil ? (
            <View style={styles.profileContainer}>
              
>>>>>>> Deploys
              {carregando ? (
                <Skeleton width={52 * fontSizeScale} height={52 * fontSizeScale} borderRadius={(52 * fontSizeScale)/2} style={{ marginRight: 12 }} />
              ) : (
<<<<<<< HEAD
                <Image source={FotoPerfilLocal} style={styles.profileImageHome} />
=======
                <Image source={FotoPerfilLocal} style={[styles.profileImage, { borderColor: headerBgColor }]} />
>>>>>>> Deploys
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
          </View>
        ) : (
          /* SE NÃO FOR PERFIL (OUTRAS TELAS): Ativa a estrutura de centro perfeito */
          <>
            {/* BOTÃO DE VOLTAR - FIXO NA ESQUERDA */}
            <View style={styles.leftActionArea}>
              {temGoBack && (
                <TouchableOpacity 
                  style={styles.backButton} 
                  onPress={lidarComVoltar}
                  activeOpacity={0.7}
                >
                  <Feather name="arrow-left" size={26} color="#fff" />
                </TouchableOpacity>
              )}
            </View>

            {/* TÍTULO CENTRALIZADO */}
            <View style={styles.centerContainer}>
              {carregando ? (
                <Skeleton width={140 * fontSizeScale} height={20 * fontSizeScale} borderRadius={4} />
              ) : (
<<<<<<< HEAD
                <Text style={styles.titleCenter} numberOfLines={1}>{nomeTela}</Text>
=======
                <Text style={[styles.title, { color: headerTextColor, fontSize: 22 * fontSizeScale }]} numberOfLines={1}>
                  {nomeTela}
                </Text>
>>>>>>> Deploys
              )}
            </View>
          </>
        )}

        {/* BOTÃO DE NOTIFICAÇÃO - FIXO NA DIREITA (PÁRA AMBOS OS LAYOUTS) */}
        <View style={styles.rightActionArea}>
          {carregando ? (
            <Skeleton width={48} height={48} borderRadius={24} />
          ) : (
            <AnimatedTouchableOpacity
              style={[
                styles.notification,
                quantidadeNotificacoes > 0 && { transform: [{ scale: pulseAnim }] }
              ]}
              onPress={() => {
                if (aoClicarNoSino) aoClicarNoSino(); 
                navigation.navigate("Notifications");
              }}
              activeOpacity={0.8}
            >
              <Feather name="bell" size={24} color="#fff" />
              {quantidadeNotificacoes > 0 && (
                <View style={styles.badge}>
                  <Text style={styles.badgeText}>{quantidadeNotificacoes}</Text>
                </View>
              )}
            </AnimatedTouchableOpacity>
          )}
        </View>
<<<<<<< HEAD
=======

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
>>>>>>> Deploys
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
<<<<<<< HEAD
  wrapper: { backgroundColor: "#1459b3" },
  logoRow: { paddingTop: 60, backgroundColor: "#1459b3", height: 50 },
  header: { 
    paddingBottom: 19, 
    paddingHorizontal: 22, 
    flexDirection: "row", 
    justifyContent: "space-between", 
    alignItems: "center", 
    backgroundColor: "#1459b3" 
  },
  
  // ESTILOS EXCLUSIVOS DA HOME (ALINHADO À ESQUERDA)
  homeProfileRow: {
    flex: 1,
    marginRight: 10,
  },
  profileContainer: { flexDirection: "row", alignItems: "center" },
  profileImageHome: { width: 52, height: 52, borderRadius: 26, marginRight: 12, borderWidth: 2, borderColor: "#fff" },
  rightHeaderText: { flex: 1 },
  title: { color: "#fff", fontSize: 22, fontWeight: "bold" },
  courseSubtitle: { color: "#dfe6ff", fontSize: 12, marginTop: 2, fontWeight: "500" },

  // ESTILOS DAS OUTRAS TELAS (TÍTULO NO MEIO, VOLTAR NA ESQUERDA)
  leftActionArea: {
    width: 48,
    alignItems: 'flex-start',
    justifyContent: 'center',
  },
  rightActionArea: {
    width: 48,
    alignItems: 'flex-end',
    justifyContent: 'center',
  },
  backButton: { 
    paddingVertical: 5, 
    paddingRight: 5, 
    justifyContent: 'center', 
    alignItems: 'center' 
  },
  centerContainer: { 
    flex: 1, 
    alignItems: 'center', 
    justifyContent: 'center',
    paddingHorizontal: 10,
  },
  titleCenter: { color: "#fff", fontSize: 20, fontWeight: "bold", textAlign: 'center' },

  // COMPONENTES GERAIS
  notification: { width: 48, height: 48, borderRadius: 24, justifyContent: "center", alignItems: "center", backgroundColor: "rgba(255,255,255,0.15)" },
  badge: { position: "absolute", top: 5, right: 5, backgroundColor: "#ff4d67", width: 18, height: 18, borderRadius: 9, justifyContent: "center", alignItems: "center" },
  badgeText: { color: "#fff", fontSize: 10, fontWeight: "bold" },
  curveContainer: { backgroundColor: "#1459b3" },
  curve: { height: 40, backgroundColor: '#FFFFFF', borderTopLeftRadius: 30, borderTopRightRadius: 30 },
=======
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

>>>>>>> Deploys
});