import { useState, useEffect, useRef } from 'react';
import { Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { URL_BASE } from '../config/backend';

export const useEventos = () => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [salvando, setSalvando] = useState(false);
    const salvandoRef = useRef(false);

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
        if (salvandoRef.current) return;
        salvandoRef.current = true;
        setSalvando(true);

        try {
        const idUsuario = await AsyncStorage.getItem('idUsuario');

        // Validação básica
        if (!novoEvento.title?.trim()) {
            Alert.alert("Erro", "Preencha o nome do evento");
            return;
        }
        if (!novoEvento.date?.trim()) {
            Alert.alert("Erro", "Preencha a data do evento");
            return;
        }
        if (!novoEvento.time?.trim()) {
            Alert.alert("Erro", "Preencha o horário do evento");
            return;
        }
        if (!novoEvento.local?.trim()) {
            Alert.alert("Erro", "Preencha o local do evento");
            return;
        }

        const isEdicao = novoEvento.id != null;
        const url = isEdicao
            ? `${URL_BASE}/eventos/${novoEvento.id}`
            : `${URL_BASE}/eventos`;

        const method = isEdicao ? 'PUT' : 'POST';

        // Converte DD/MM/AAAA -> AAAA-MM-DD
        let dataFormatada = novoEvento.date;

        if (dataFormatada.includes("/")) {
            const [dia, mes, ano] = dataFormatada.split("/");
            dataFormatada = `${ano}-${mes}-${dia}`;
        }

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ...novoEvento,
                    date: dataFormatada,
                    usuario_id: idUsuario
                })
            });

            if (response.ok) {
                Alert.alert(
                    "Sucesso",
                    isEdicao ? "Evento atualizado!" : "Evento criado!"
                );

                onSuccess();
                buscarEventos();

            } else {
                const errorData = await response.json();

                console.log("Status:", response.status);
                console.log("Erro Backend:", errorData);

                Alert.alert(
                    "Erro",
                    errorData.detalhe ||
                    errorData.mensagem ||
                    JSON.stringify(errorData)
                );
            }

        } catch (error) {
            console.log("Erro ao salvar evento:", error);
            Alert.alert("Erro", error.message);
        } finally {
            salvandoRef.current = false;
            setSalvando(false);
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

            const data = await response.json().catch(() => ({}));

            if (response.ok) {
                Alert.alert('Sucesso', data.mensagem || 'Evento removido!');
                onSuccess?.();
                await buscarEventos();
                return;
            }

            Alert.alert('Erro', data.mensagem || 'Não foi possível excluir o evento.');
        } catch (error) {
            console.error('Erro ao excluir evento:', error);
            Alert.alert('Erro', 'Não foi possível excluir o evento.');
        }
    };

    useEffect(() => { buscarEventos(); }, []);

    return { events, loading, salvando, buscarEventos, salvarEvento, excluirEvento };
};