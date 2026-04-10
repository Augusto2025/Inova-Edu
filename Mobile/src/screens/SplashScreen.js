import { useEffect } from "react";
import { View, StyleSheet, Text } from "react-native";
import { Image  } from "react-native";

const Logo = require('../../assets/LOGOBRANCO.png');

export default function SplashScreen({ navigation }) {
    useEffect(() => {
        setTimeout(() => {
        navigation.replace('Login');
        }, 3000);
    }, []);

    return (
        <View style={styles.container}>
            <Image source={Logo} style={styles.logo} />
            <Text style={styles.text}>Carregando...</Text>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#1459b3',
        alignItems: 'center',
        justifyContent: 'center',
    },
    text: {
        color: '#ffffff',
        fontSize: 24,
        fontWeight: 'bold',
    },
});