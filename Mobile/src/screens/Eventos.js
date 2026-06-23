import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity,  TextInput,Modal, ActivityIndicator, Alert } from 'react-native';
import { Calendar } from 'react-native-calendars';
import { Ionicons } from '@expo/vector-icons';
import Header from '../components/Header';
import { COLORS } from '../components/Cores';
import styles from '../styles/Evento';
import AsyncStorage from '@react-native-async-storage/async-storage';

const URL_BASE = process.env.EXPO_PUBLIC_URL_BACKEND.replace('/login', '');

export default function CalendarScreen() {
  const [selected, setSelected] = useState('');
  const [modalVisible, setModalVisible] = useState(false);
  const [eventSelected, setEventSelected] = useState(null);
  
  // Estados para dados dinâmicos do banco
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  // Adicione estes estados no topo do seu componente
  const [modalAddVisible, setModalAddVisible] = useState(false);
  const [novoEvento, setNovoEvento] = useState({ title: '', date: '', time: '', local: '', description: '' });
  const [idUsuarioLogado, setIdUsuarioLogado] = useState(null);
  const [isProfessor, setIsProfessor] = useState(false);

  // Função para salvar
  const salvarEvento = async () => {
      // 1. Pega o ID do usuário logado
      const idUsuario = await AsyncStorage.getItem('idUsuario');

      if (!idUsuario) {
          Alert.alert("Erro", "Usuário não identificado. Faça login novamente.");
          return;
      }

      try {
          const response = await fetch(`${URL_BASE}/eventos`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                  ...novoEvento,
                  usuario_id: idUsuario
              })
          });
          
          if (response.ok) {
              Alert.alert("Sucesso", "Evento criado!");
              setModalAddVisible(false);
              buscarEventos();
          }
      } catch (error) {
          Alert.alert("Erro", "Falha ao salvar evento.");
      }
  };

  const verificarCargo = async () => {
      const tipoUsuario = await AsyncStorage.getItem('tipo'); // Buscará o valor 'professor' ou 'aluno'
      console.log("Tipo do usuário logado:", tipoUsuario);

      if (tipoUsuario === 'Professor') {
          setIsProfessor(true);
      }
  };

  const confirmarExclusao = (idEvento) => {
      Alert.alert("Confirmar", "Deseja realmente excluir este evento?", [
          { text: "Cancelar" },
          { text: "Sim", onPress: () => excluirEvento(idEvento) }
      ]);
  };

  const excluirEvento = async (idEvento) => {
      const idUsuario = await AsyncStorage.getItem('idUsuario');
      try {
          const response = await fetch(`${URL_BASE}/eventos/${idEvento}`, {
              method: 'DELETE',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ usuario_id: idUsuario })
          });

          if (response.ok) {
              Alert.alert("Sucesso", "Evento removido!");
              setModalVisible(false);
              buscarEventos();
          }
      } catch (error) {
          Alert.alert("Erro", "Não foi possível excluir.");
      }
  };

  useEffect(() => {
    const carregarDados = async () => {
      const id = await AsyncStorage.getItem('idUsuario');
      setIdUsuarioLogado(id);
      verificarCargo();
      buscarEventos();
    };
    carregarDados();
  }, []);

  const buscarEventos = async () => {
    try {
      setLoading(true);
      const resposta = await fetch(`${URL_BASE}/eventos`);
      const dados = await resposta.json();
      
      if (resposta.ok && Array.isArray(dados)) {
        setEvents(dados);
      } else {
        Alert.alert("Erro", dados.mensagem || "Não foi possível carregar os eventos.");
      }
    } catch (error) {
      Alert.alert("Erro de conexão", "Falha ao conectar com o servidor de eventos.");
    } finally {
      setLoading(false);
    }
  };

  const getEventStatusColor = (eventDate) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const evDate = new Date(eventDate + 'T00:00:00'); // Evita problemas de fuso horário local
    
    if (evDate.getTime() === today.getTime()) return '#FFD700'; // Hoje (Amarelo)
    return evDate > today ? '#4CAF50' : '#F44336'; // Futuro (Verde) : Passado (Vermelho)
  };

  // Extrai dinamicamente o Dia e o Mês por extenso para o Badge visual
  const obterInfoData = (dataStr) => {
    if (!dataStr) return { dia: '00', mes: 'IND' };
    const partes = dataStr.split('-'); // [YYYY, MM, DD]
    const meses = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'];
    const mesIndex = parseInt(partes[1], 10) - 1;
    return {
      dia: partes[2],
      mes: meses[mesIndex] || 'ERR'
    };
  };

  const handleOpenEvent = (dateString) => {
      const foundEvent = events.find(e => e.date === dateString);
      if (foundEvent) {
          console.log("Evento Selecionado:", foundEvent); // VEJA ISSO NO TERMINAL DO VS CODE
          setEventSelected(foundEvent);
          setModalVisible(true);
      }
      setSelected(dateString);
  };

  // Monta o objeto de marcações do calendário unindo os pontos do banco com o dia selecionado
  const mapearMarcacoesCalendario = () => {
    const marcacoes = {};
    
    // Adiciona uma bolinha colorida em cada dia que possui evento cadastrado
    events.forEach(ev => {
      marcacoes[ev.date] = { 
        marked: true, 
        dotColor: getEventStatusColor(ev.date) 
      };
    });

    // Mantém o destaque visual azul do dia que o usuário clicou por último
    if (selected) {
      marcacoes[selected] = {
        ...marcacoes[selected],
        selected: true,
        selectedColor: '#1459b3'
      };
    }

    return marcacoes;
  };

  return (
    <View style={styles.container}>
      <Header nomeTela={"Calendário"} />

      {/* Botão flutuante para adicionar evento */}
      {isProfessor && (
              <TouchableOpacity style={styles.fab} onPress={() => setModalAddVisible(true)}>
                  <Ionicons name="add" size={28} color="white" />
              </TouchableOpacity>
          )}

      {loading ? (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <ActivityIndicator size="large" color="#1459b3" />
          <Text style={{ marginTop: 10, color: '#1459b3' }}>Buscando cronograma...</Text>
        </View>
      ) : (
        
        <ScrollView contentContainerStyle={{ flexGrow: 1, paddingBottom: 100 }}>
          <View style={styles.calendarContainer}>
            <Calendar
              onDayPress={day => handleOpenEvent(day.dateString)}
              markedDates={mapearMarcacoesCalendario()}
              theme={{
                todayBackgroundColor: '#1459b3',
                todayTextColor: '#ffffff',
                arrowColor: '#1459b3',
                monthTextColor: '#1459b3',
                textMonthFontWeight: 'bold',
                selectedDayBackgroundColor: '#1459b3',
              }}
            />
          </View>


          <View style={styles.eventSection}>
            <Text style={styles.eventSectionTitle}>Eventos Cadastrados</Text>
            
            {events.length === 0 ? (
              <Text style={{ textAlign: 'center', color: '#94A3B8', marginTop: 20, fontStyle: 'italic' }}>
                Nenhum evento agendado no momento.
              </Text>
            ) : (
              events.map(event => {
                const statusColor = getEventStatusColor(event.date);
                const infoData = obterInfoData(event.date);
                
                return (
                  <TouchableOpacity 
                    key={event.id} 
                    style={styles.eventCard} 
                    onPress={() => handleOpenEvent(event.date)}
                  >
                    <View style={[styles.dateBadge, { borderColor: statusColor }]}>
                       <View style={[styles.dateBadgeTop, { backgroundColor: statusColor }]}>
                          <Text style={styles.monthText}>{infoData.mes}</Text>
                       </View>
                       <View style={styles.dateBadgeBottom}>
                          <Text style={[styles.dayText, { color: '#333' }]}>{infoData.dia}</Text>
                       </View>
                    </View>

                    <View style={styles.eventInfo}>
                      <Text style={styles.eventTitle} numberOfLines={1}>{event.title}</Text>
                      <Text style={styles.eventTimeInfo}>
                        <Ionicons name="time-outline" size={12} /> {event.time} • {event.local}
                      </Text>
                    </View>
                    <View style={[styles.statusDot, { backgroundColor: statusColor }]} />
                  </TouchableOpacity>
                );
              })
            )}
          </View>
        </ScrollView>
      )}

      {/* Modal de Cadastro */}
      <Modal visible={modalAddVisible} transparent animationType="slide">
          <View style={styles.modalOverlay}>
              <View style={styles.modalContent}>
                  {/* Header seguindo o padrão */}
                  <View style={[styles.modalHeader, { backgroundColor: '#1459b3' }]}>
                      <Text style={styles.modalTitle}>Novo Evento</Text>
                      <TouchableOpacity onPress={() => setModalAddVisible(false)}>
                          <Ionicons name="close-circle" size={30} color="white" />
                      </TouchableOpacity>
                  </View>

                  {/* Body seguindo o padrão */}
                  <View style={styles.modalBody}>
                      <TextInput placeholder="Título" style={styles.input} onChangeText={t => setNovoEvento({...novoEvento, title: t})} />
                      <TextInput placeholder="Data (AAAA-MM-DD)" style={styles.input} onChangeText={t => setNovoEvento({...novoEvento, date: t})} />
                      <TextInput placeholder="Hora (HH:MM)" style={styles.input} onChangeText={t => setNovoEvento({...novoEvento, time: t})} />
                      <TextInput placeholder="Local" style={styles.input} onChangeText={t => setNovoEvento({...novoEvento, local: t})} />
                      <TextInput 
                          placeholder="Descrição" 
                          style={[styles.input, { height: 80, textAlignVertical: 'top' }]} 
                          multiline 
                          onChangeText={t => setNovoEvento({...novoEvento, description: t})} 
                      />
                      
                      <TouchableOpacity style={styles.saveBtn} onPress={salvarEvento}>
                          <Text style={styles.saveBtnText}>Cadastrar Evento</Text>
                      </TouchableOpacity>
                  </View>
              </View>
          </View>
      </Modal>

      {/* MODAL DE DETALHES */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={[styles.modalHeader, { backgroundColor: eventSelected ? getEventStatusColor(eventSelected.date) : '#1459b3' }]}>
              <Text style={styles.modalTitle}>{eventSelected?.title}</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Ionicons name="close-circle" size={30} color="white" />
              </TouchableOpacity>
            </View>
            
            <View style={styles.modalBody}>
              <View style={styles.modalInfoRow}>
                <Ionicons name="calendar-outline" size={20} color="#1459b3" />
                <Text style={styles.modalInfoText}>Data: {eventSelected?.date.split('-').reverse().join('/')}</Text>
              </View>
              <View style={styles.modalInfoRow}>
                <Ionicons name="time-outline" size={20} color="#1459b3" />
                <Text style={styles.modalInfoText}>Horário: {eventSelected?.time}</Text>
              </View>
              <View style={styles.modalInfoRow}>
                <Ionicons name="location-outline" size={20} color="#1459b3" />
                <Text style={styles.modalInfoText}>Local: {eventSelected?.local}</Text>
              </View>
              
              <Text style={styles.descriptionTitle}>Descrição:</Text>
              <Text style={styles.descriptionText}>{eventSelected?.description || "Sem descrição informada."}</Text>
              
              {/* <TouchableOpacity 
                style={styles.closeButton} 
                onPress={() => setModalVisible(false)}
              >
                <Text style={styles.closeButtonText}>Fechar</Text>
              </TouchableOpacity> */}
              {/* Dentro do modal de detalhes, onde você exibe os dados: */}
              {parseInt(idUsuarioLogado) === eventSelected?.usuario_id && (
                  <TouchableOpacity 
                      style={[styles.closeButton, { backgroundColor: '#FF9800' }]} 
                      onPress={() => habilitarEdicao(eventSelected)}
                  >
                      <Text style={styles.closeButtonText}>Editar Evento</Text>
                  </TouchableOpacity>
              )}
              {/* Dentro do modal de detalhes, abaixo da descrição: */}
              {isProfessor && parseInt(idUsuarioLogado) === parseInt(eventSelected?.usuario_id) &&(
                  <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 20 }}>
                      
                      {/* Botão Editar */}
                      <TouchableOpacity 
                          style={[styles.closeButton, { backgroundColor: '#FF9800', flex: 0.48 }]} 
                          onPress={() => habilitarEdicao(eventSelected)}
                      >
                          <Text style={styles.closeButtonText}>Editar</Text>
                      </TouchableOpacity>

                      {/* Botão Excluir */}
                      <TouchableOpacity 
                          style={[styles.closeButton, { backgroundColor: '#d32f2f', flex: 0.48 }]} 
                          onPress={() => confirmarExclusao(eventSelected.id)}
                      >
                          <Text style={styles.closeButtonText}>Excluir</Text>
                      </TouchableOpacity>
                  </View>
              )}
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}