import React, { useState, useEffect, useRef } from "react";
import { View, StyleSheet, Text, Modal, Animated, Easing, useWindowDimensions } from "react-native";
import { useIsFocused } from "@react-navigation/native";

const Logo = require('../../assets/LOGOBRANCO.png');

export default function SplashScreen() {
    const isFocused = useIsFocused();
    const { width } = useWindowDimensions();
    const [isLoading, setIsLoading] = useState(true);
    const logoSize = Math.min(160, Math.max(100, width * 0.4));

    // Animadores de escala e opacidade
    const scaleAnim = useRef(new Animated.Value(1)).current;
    const opacityAnim = useRef(new Animated.Value(0.8)).current;

    useEffect(() => {
        if (isFocused) {
            setIsLoading(true);

            // Animação de pulso contínuo
            const pulse = Animated.loop(
                Animated.sequence([
                    Animated.parallel([
                        Animated.timing(scaleAnim, {
                            toValue: 1.15,
                            duration: 800,
                            easing: Easing.inOut(Easing.ease),
                            useNativeDriver: true,
                        }),
                        Animated.timing(opacityAnim, {
                            toValue: 1,
                            duration: 800,
                            useNativeDriver: true,
                        }),
                    ]),
                    Animated.parallel([
                        Animated.timing(scaleAnim, {
                            toValue: 1,
                            duration: 800,
                            easing: Easing.inOut(Easing.ease),
                            useNativeDriver: true,
                        }),
                        Animated.timing(opacityAnim, {
                            toValue: 0.7,
                            duration: 800,
                            useNativeDriver: true,
                        }),
                    ]),
                ])
            );

            pulse.start();

            // ⏱️ Definido para 6 segundos (6000 ms)
            const timer = setTimeout(() => {
                pulse.stop();
                setIsLoading(false);
            }, 6000);

            return () => {
                pulse.stop();
                clearTimeout(timer);
            };
        }
    }, [isFocused]);

    if (!isLoading) return null;

    return (
        <Modal transparent={true} visible={true} animationType="fade">
            <View style={styles.container}>
                <Animated.Image 
                    source={Logo} 
                    style={[
                        styles.logo, 
                        { 
                            width: logoSize,
                            height: logoSize,
                            transform: [{ scale: scaleAnim }],
                            opacity: opacityAnim,
                        }
                    ]} 
                />
                
                {/* 🌟 Mensagem de boas-vindas atualizada */}
                <Text style={styles.welcomeText}>Bem-vindo ao</Text>
                <Text style={styles.titleText}>Repositório de Projetos</Text>
            </View>
        </Modal>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#1459b3',
        alignItems: 'center',
        justifyContent: 'center',
        paddingHorizontal: 20,
    },
    logo: { 
        marginBottom: 24,
        resizeMode: 'contain',
    },
    welcomeText: { 
        color: '#ffffff', 
        fontSize: 18, 
        fontWeight: 'normal',
        opacity: 0.9,
    },
    titleText: { 
        color: '#ffffff', 
        fontSize: 22, 
        fontWeight: 'bold',
        textAlign: 'center',
        marginTop: 4,
    },
});