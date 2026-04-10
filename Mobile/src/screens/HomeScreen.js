import React, { useState } from 'react';
import logo from '../../assets/LOGOBRANCO.png';
import * as ImagePicker from 'expo-image-picker';

import { View, Text, StyleSheet, Image, TextInput, ScrollView, TouchableOpacity } from 'react-native';

export default function HomeScreen() {

    const [foto, setFoto] = useState(null);

    async function escolherImagem() {
        const resultado = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            quality: 1,
        });

        if (!resultado.canceled) {
            setFoto(resultado.assets[0].uri);
        }
    }

    return (
        <ScrollView style={styles.container}>

            {/* HEADER */}
            <View style={styles.header}>
                <Image source={logo} style={styles.image} />
                <Text style={styles.nome1}>InovaEdu</Text>

                <View style={styles.user}>

                    <TouchableOpacity onPress={escolherImagem}>
                        {foto ? (
                            <Image source={{ uri: foto }} style={styles.avatar} />
                        ) : (
                            <View style={styles.avatarFallback}>
                                <Text style={styles.letra}>A</Text>
                            </View>
                        )}
                    </TouchableOpacity>

                    <Text style={styles.nome}>Alcides</Text>
                </View>
            </View>

            {/* CARD REPOSITORIOS */}
            <View style={styles.card1}>
                <Text style={styles.titulo}>Repositórios recente</Text>

                <TextInput
                    placeholder="Buscar repositórios, arquivos"
                    style={styles.input}
                />

                <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                    <TouchableOpacity style={styles.tag}>
                        <Text>Inova Edu</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.tag}>
                        <Text>Python</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.tag}>
                        <Text>React</Text>
                    </TouchableOpacity>
                </ScrollView>
            </View>

            {/* CARD FORUM */}
            <View style={styles.card}>
                <Text style={styles.titulo}>💬 Destaque do fórum</Text>
                <Text style={styles.texto}>3 novas respostas no tópico.</Text>
                <Text style={styles.sub}>#Cores css</Text>
            </View>

            {/* CARD EVENTOS */}
            <View style={styles.card}>
                <Text style={styles.titulo}>📅 Eventos próximos</Text>
                <Text style={styles.texto}>Semana S</Text>
                <Text style={styles.sub}>Amanhã, 10h</Text>
            </View>

            {/* AJUDA */}
            <TouchableOpacity style={styles.card}>
                <Text style={styles.titulo}>🤖 Precisa de ajuda?</Text>
            </TouchableOpacity>

        </ScrollView>


    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#cfe0e8',
    },

    header: {
        backgroundColor: '#1459b3',
        padding: 20,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },

    user: {
        alignItems: 'center',
    },

    avatar: {
        width: 50,
        height: 50,
        top: 40,
        borderRadius: 25,
        borderWidth: 1,
        borderColor: 'white',
    },

    nome: {
        color: 'white',
        marginTop: 45,
    },

    card: {
        backgroundColor: '#e6e6e6',
        margin: 15,
        padding: 15,
        borderRadius: 15,

        // Android
        elevation: 6,

        // iOS
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 3 },
        shadowOpacity: 0.2,
        shadowRadius: 3,
    },

    titulo: {
        fontSize: 16,
        fontWeight: 'bold',
        marginBottom: 10,
    },

    texto: {
        fontSize: 14,
    },

    sub: {
        fontSize: 12,
        color: 'gray',
    },

    input: {
        backgroundColor: 'white',
        borderRadius: 20,
        paddingHorizontal: 15,
        marginBottom: 10,
        height: 45,
    },

    tag: {
        backgroundColor: '#d9d9d9',
        padding: 15,
        borderRadius: 10,
        marginRight: 10,
    },

    card1: {
        backgroundColor: '#e6e6e6',
        margin: 15,
        padding: 20,
        borderRadius: 15,
        elevation: 4,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 3 },
        shadowOpacity: 0.2,
        shadowRadius: 4,


    },

    image: {
        width: 60,
        height: 80,
        resizeMode: 'contain',
        tintColor: 'white',
        top: 13,
    },

    nome1: {
        color: 'white',
        marginTop: 25,
        marginRight: 190,
        fontSize: 17,
    },

    // 🔥 NOVOS (avatar fallback)
    avatarFallback: {
        width: 50,
        height: 50,
        borderRadius: 25,
        backgroundColor: '#6c63ff',
        justifyContent: 'center',
        alignItems: 'center',
        top: 40,
    },

    letra: {
        color: 'white',
        fontSize: 18,
        fontWeight: 'bold',
    },
});