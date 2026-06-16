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
import Skeleton from "./Skeleton";

// 1. IMPORTE A SUA FOTO LOCAL AQUI (Ajuste o caminho se sua pasta for diferente)
import FotoPerfilLocal from "../../assets/pascal.jpg"; 

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
    <View style={styles.wrapper}>
      <View style={styles.logoRow} />

      <View style={styles.header}>
        <View style={styles.left}>
          {exibirPerfil ? (
            <View style={styles.profileContainer}>
              
              {/* Mantemos o Skeleton se a tela toda estiver carregando dados */}
              {carregando ? (
                <Skeleton width={52} height={52} borderRadius={26} style={{ marginRight: 12 }} />
              ) : (
                /* 2. ALTERADO AQUI: Agora passa a foto importada direto */
                <Image source={FotoPerfilLocal} style={styles.profileImage} />
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
          ) : (
            <View style={styles.noProfileContainer}>
              {carregando ? (
                <Skeleton width={140} height={20} borderRadius={4} />
              ) : (
                <Text style={styles.title} numberOfLines={1}>{nomeTela}</Text>
              )}
            </View>
          )}
        </View>

        {carregando ? (
          <Skeleton width={48} height={48} borderRadius={24} style={{ alignSelf: 'center' }} />
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
  logoRow: { paddingTop: 70, backgroundColor: "#1459b3", height: 60 },
  header: { paddingTop: 5, paddingBottom: 19, paddingHorizontal: 22, flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start", backgroundColor: "#1459b3" },
  left: { flex: 1, marginRight: 10 },
  profileContainer: { flexDirection: "row", alignItems: "center" },
  profileImage: { width: 52, height: 52, borderRadius: 26, marginRight: 12, borderWidth: 2, borderColor: "#fff" },
  rightHeaderText: { flex: 1 },
  noProfileContainer: { flexDirection: "column", justifyContent: "center", height: 52 },
  title: { color: "#fff", fontSize: 22, fontWeight: "bold" },
  courseSubtitle: { color: "#dfe6ff", fontSize: 12, marginTop: 2, fontWeight: "500" },
  notification: { width: 48, height: 48, borderRadius: 24, justifyContent: "center", alignItems: "center", backgroundColor: "rgba(255,255,255,0.15)", alignSelf: "center" },
  badge: { position: "absolute", top: 5, right: 5, backgroundColor: "#ff4d67", width: 18, height: 18, borderRadius: 9, justifyContent: "center", alignItems: "center" },
  badgeText: { color: "#fff", fontSize: 10, fontWeight: "bold" },
  curveContainer: { backgroundColor: "#1459b3" },
  curve: { height: 45, backgroundColor: '#FFFFFF', borderTopLeftRadius: 30, borderTopRightRadius: 30 },
});