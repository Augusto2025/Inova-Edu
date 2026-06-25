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
import { useNavigation } from "@react-navigation/native";
import Skeleton from "./Skeleton";

// IMPORTAÇÃO DA SUA FOTO LOCAL
import FotoPerfilLocal from "../../assets/pascal.jpg"; 

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
    <View style={styles.wrapper}>
      <View style={styles.logoRow} />

      <View style={styles.header}>
        
        {/* SE FOR PERFIL (HOME): Usa o layout padrão estendido na linha */}
        {exibirPerfil ? (
          <View style={styles.homeProfileRow}>
            <View style={styles.profileContainer}>
              {carregando ? (
                <Skeleton width={52} height={52} borderRadius={26} style={{ marginRight: 12 }} />
              ) : (
                <Image source={FotoPerfilLocal} style={styles.profileImageHome} />
              )}

              <View style={styles.rightHeaderText}>
                {carregando ? (
                  <View style={{ gap: 6, justifyContent: 'center', height: 52 }}>
                    <Skeleton width={110} height={16} borderRadius={4} />
                    <Skeleton width={150} height={12} borderRadius={4} />
                  </View>
                ) : (
                  <>
                    <Text style={styles.title} numberOfLines={1}>{nomeTela}</Text>
                    <Text style={styles.courseSubtitle} numberOfLines={1}>
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
                <Skeleton width={140} height={20} borderRadius={4} />
              ) : (
                <Text style={styles.titleCenter} numberOfLines={1}>{nomeTela}</Text>
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
      </View>

      {exibirCurva && (
        <View style={styles.curveContainer}>
          <View style={styles.curve} />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
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
});