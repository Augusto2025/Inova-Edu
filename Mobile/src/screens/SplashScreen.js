import React, { useState, useEffect } from "react";
import { View, StyleSheet, Text, Image, Modal } from "react-native"; // 🌟 Adicionado o Modal aqui
import { useIsFocused } from "@react-navigation/native";

const Logo = require('../../assets/LOGOBRANCO.png');

export default function SplashScreen() {
    const isFocused = useIsFocused();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (isFocused) {
            setIsLoading(true);
            const timer = setTimeout(() => setIsLoading(false), 1200);
            return () => clearTimeout(timer);
        }
    }, [isFocused]);

    if (!isLoading) return null; // Se terminou, desmonta o componente

    return (
        /* 🌟 O Modal cria uma camada isolada e indestrutível por cima de TUDO */
        <Modal transparent={true} visible={true} animationType="fade">
            <View style={styles.container}>
                <Image source={Logo} style={styles.logo} />
                <Text style={styles.text}>Carregando...</Text>
            </View>
        </Modal>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1, // 🌟 O Modal já cobre a tela inteira, então o flex: 1 resolve perfeitamente
        backgroundColor: '#1459b3',
        alignItems: 'center',
        justifyContent: 'center',
    },
    logo: { width: 150, height: 150, marginBottom: 20 },
    text: { color: '#ffffff', fontSize: 24, fontWeight: 'bold' },
});