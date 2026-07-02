import { useState, useEffect } from 'react';
import { Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

export const useEventos = () => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);

    const buscarEventos = async () => {
        try {
            setLoading(true);
            const resposta = await fetch(`${URL_BASE}/eventos`);
            const dados = await resposta.json();
            if (resposta.ok) setEvents(dados);
        } catch (error) {
            Alert.alert("Erro", "Falha ao carregar eventos.");
        } finally {
            setLoading(false);
        }
    };

    const salvarEvento = async (novoEvento, onSuccess) => {
        const idUsuario = await AsyncStorage.getItem('idUsuario');
        const isEdicao = novoEvento.id != null;
        const url = isEdicao ? `${URL_BASE}/eventos/${novoEvento.id}` : `${URL_BASE}/eventos`;
        const method = isEdicao ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...novoEvento, usuario_id: idUsuario })
            });

            if (response.ok) {
                Alert.alert("Sucesso", isEdicao ? "Evento atualizado!" : "Evento criado!");
                onSuccess(); // Executa o que a tela precisar (fechar modal, limpar formulário)
                buscarEventos();
            } else {
                const errorData = await response.json();
                Alert.alert("Erro", errorData.mensagem || "Não foi possível salvar.");
            }
        } catch (error) {
            Alert.alert("Erro", "Falha na conexão.");
        }
    };

    const excluirEvento = async (idEvento, onSuccess) => {
        const idUsuario = await AsyncStorage.getItem('idUsuario');
        try {
            const response = await fetch(`${URL_BASE}/eventos/${idEvento}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ usuario_id: idUsuario })
            });
            if (response.ok) {
                Alert.alert("Sucesso", "Evento removido!");
                onSuccess();
                buscarEventos();
            }
        } catch (error) {
            Alert.alert("Erro", "Não foi possível excluir.");
        }
    };

    useEffect(() => { buscarEventos(); }, []);

    return { events, loading, buscarEventos, salvarEvento, excluirEvento };
};