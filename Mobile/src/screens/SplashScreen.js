import React, { useState, useEffect } from "react";
import { View, StyleSheet, Text, Image } from "react-native";
import { useIsFocused } from "@react-navigation/native"; // <-- O segredo está aqui

const Logo = require('../../assets/LOGOBRANCO.png');

export default function SplashScreen() {
    const isFocused = useIsFocused(); // Detecta automaticamente se a tela está ativa
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (isFocused) {
            setIsLoading(true);
            const timer = setTimeout(() => setIsLoading(false), 1200);
            return () => clearTimeout(timer);
        }
    }, [isFocused]);

    if (!isLoading) return null; // Se terminou de carregar, some da tela

    return (
        <View style={styles.container}>
            <Image source={Logo} style={styles.logo} />
            <Text style={styles.text}>Carregando...</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        ...StyleSheet.absoluteFillObject, // Cobre a tela inteira sozinho
        backgroundColor: '#1459b3',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 9999, // Fica por cima de tudo
    },
    logo: { width: 150, height: 150, marginBottom: 20 },
    text: { color: '#ffffff', fontSize: 24, fontWeight: 'bold' },
});