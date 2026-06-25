import React, { useState, useEffect, useContext } from 'react';
import { 
  View, 
  Text, 
  ScrollView, 
  TouchableOpacity, 
  TextInput, 
  Modal, 
  ActivityIndicator, 
  Alert, 
  StyleSheet // 1. IMPORTAÇÃO CORRIGIDA AQUI
} from 'react-native';
import { Calendar } from 'react-native-calendars';
import { Ionicons } from '@expo/vector-icons';
import Header from '../components/Header';
import { COLORS } from '../components/Cores'; 
import styles from '../styles/Evento';
import AsyncStorage from '@react-native-async-storage/async-storage';

import { useEventos } from '../hooks/eventos';
import { ThemeContext } from '../context/ThemeContext';

export default function CalendarScreen() {
  // 2. PUXANDO AS VARIÁVEIS GLOBAIS DE ACESSIBILIDADE E TEMA
  const { theme, fontSizeScale } = useContext(ThemeContext);

  const { events, loading, salvarEvento, excluirEvento } = useEventos();

  const [selected, setSelected] = useState('');
  const [modalVisible, setModalVisible] = useState(false);
  const [eventSelected, setEventSelected] = useState(null);
  const [modalAddVisible, setModalAddVisible] = useState(false);
  const [novoEvento, setNovoEvento] = useState({ title: '', date: '', time: '', local: '', description: '' });
  
  const [idUsuarioLogado, setIdUsuarioLogado] = useState(null);
  const [isProfessor, setIsProfessor] = useState(false);

  useEffect(() => {
    const carregarDadosUsuario = async () => {
      const id = await AsyncStorage.getItem('idUsuario');
      const tipoUsuario = await AsyncStorage.getItem('tipo');
      
      setIdUsuarioLogado(id);
      if (tipoUsuario === 'Professor') setIsProfessor(true);
    };
    carregarDadosUsuario();
  }, []);

  const handleSalvar = () => {
      salvarEvento(novoEvento, () => {
          setModalAddVisible(false);
          setNovoEvento({ title: '', date: '', time: '', local: '', description: '' });
      });
  };

  const habilitarEdicao = (evento) => {
      setNovoEvento({
          id: evento.id, 
          title: evento.title,
          date: evento.date,
          time: evento.time,
          local: evento.local,
          description: evento.description
      });
      setModalVisible(false); 
      setModalAddVisible(true); 
  };

  const confirmarExclusao = (idEvento) => {
      Alert.alert("Confirmar", "Deseja realmente excluir este evento?", [
          { text: "Cancelar" },
          { text: "Sim", onPress: () => excluirEvento(idEvento, () => setModalVisible(false)) }
      ]);
  };

  const getEventStatusColor = (eventDate) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const evDate = new Date(eventDate + 'T00:00:00'); 
    
    if (evDate.getTime() === today.getTime()) return '#FFD700'; 
    return evDate > today ? '#4CAF50' : '#F44336'; 
  };

  const obterInfoData = (dataStr) => {
    if (!dataStr) return { dia: '00', mes: 'IND' };
    const partes = dataStr.split('-'); 
    const meses = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'];
    const mesIndex = parseInt(partes[1], 10) - 1;
    return { dia: partes[2], mes: meses[mesIndex] || 'ERR' };
  };

  const handleOpenEvent = (dateString) => {
      const foundEvent = events.find(e => e.date === dateString);
      if (foundEvent) {
          setEventSelected(foundEvent);
          setModalVisible(true);
      }
      setSelected(dateString);
  };

  const mapearMarcacoesCalendario = () => {
    const marcacoes = {};
    events.forEach(ev => {
      marcacoes[ev.date] = { marked: true, dotColor: getEventStatusColor(ev.date) };
    });
    if (selected) {
      marcacoes[selected] = { ...marcacoes[selected], selected: true, selectedColor: '#1459b3' };
    }
    return marcacoes;
  };

  return (
    // 3. MESCLANDO O ESTILO EXTERNO COM O FUNDO DINÂMICO
    <View style={[styles.container, { backgroundColor: theme.background }]}>
      <Header nomeTela={"Calendário"} />

      {isProfessor && (
          <TouchableOpacity style={styles.fab} onPress={() => setModalAddVisible(true)}>
              <Ionicons name="add" size={28} color="white" />
          </TouchableOpacity>
      )}

      {loading ? (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <ActivityIndicator size="large" color="#1459b3" />
          <Text style={{ marginTop: 10, color: theme.text, fontSize: 16 * fontSizeScale }}>Buscando cronograma...</Text>
        </View>
      ) : (
        <ScrollView contentContainerStyle={{ flexGrow: 1, paddingBottom: 100 }}>
          
          <View style={styles.calendarContainer}>
            <Calendar
              onDayPress={day => handleOpenEvent(day.dateString)}
              markedDates={mapearMarcacoesCalendario()}
              // 4. ADAPTANDO AS CORES DO COMPONENTE CALENDÁRIO AO MODO ESCURO
              theme={{
                calendarBackground: theme.card,
                textSectionTitleColor: theme.text,
                dayTextColor: theme.text,
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
            <Text style={[styles.eventSectionTitle, { color: theme.text, fontSize: 18 * fontSizeScale }]}>
              Eventos Cadastrados
            </Text>
            
            {events.length === 0 ? (
              <Text style={{ textAlign: 'center', color: '#94A3B8', marginTop: 20, fontStyle: 'italic', fontSize: 14 * fontSizeScale }}>
                Nenhum evento agendado no momento.
              </Text>
            ) : (
              events.map(event => {
                const statusColor = getEventStatusColor(event.date);
                const infoData = obterInfoData(event.date);
                
                return (
                  <TouchableOpacity 
                    key={event.id} 
                    // 5. MUDANDO O FUNDO E BORDA DO CARD DINAMICAMENTE
                    style={[styles.eventCard, { backgroundColor: theme.card, borderColor: theme.border }]} 
                    onPress={() => handleOpenEvent(event.date)}
                  >
                    <View style={[styles.dateBadge, { borderColor: statusColor }]}>
                       <View style={[styles.dateBadgeTop, { backgroundColor: statusColor }]}>
                          <Text style={styles.monthText}>{infoData.mes}</Text>
                       </View>
                       <View style={[styles.dateBadgeBottom, { backgroundColor: theme.card }]}>
                          <Text style={[styles.dayText, { color: theme.text }]}>{infoData.dia}</Text>
                       </View>
                    </View>

                    <View style={styles.eventInfo}>
                      <Text style={[styles.eventTitle, { color: theme.text, fontSize: 16 * fontSizeScale }]} numberOfLines={1}>
                        {event.title}
                      </Text>
                      <Text style={[styles.eventTimeInfo, { color: '#94A3B8', fontSize: 14 * fontSizeScale }]}>
                        <Ionicons name="time-outline" size={14 * fontSizeScale} /> {event.time} • {event.local}
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

      {/* Modal de Cadastro/Edição */}
      <Modal visible={modalAddVisible} transparent animationType="slide">
          <View style={styles.modalOverlay}>
              <View style={[styles.modalContent, { backgroundColor: theme.card }]}>
                  <View style={[styles.modalHeader, { backgroundColor: '#1459b3' }]}>
                    <Text style={[styles.modalTitle, { fontSize: 20 * fontSizeScale }]}>
                      {novoEvento.id ? "Editar Evento" : "Novo Evento"}
                    </Text>
                    <TouchableOpacity onPress={() => {
                          setNovoEvento({ title: '', date: '', time: '', local: '', description: '' });
                          setModalAddVisible(false);
                      }}>
                          <Ionicons name="close-circle" size={30} color="white" />
                    </TouchableOpacity>
                  </View>

                  <View style={styles.modalBody}>
                      {/* Adaptando os TextInputs para não ficarem invisíveis no Modo Escuro */}
                      <TextInput 
                        value={novoEvento.title} 
                        placeholder="Título" 
                        placeholderTextColor="#94A3B8"
                        style={[styles.input, { backgroundColor: theme.background, color: theme.text, fontSize: 16 * fontSizeScale }]} 
                        onChangeText={t => setNovoEvento({...novoEvento, title: t})} 
                      />
                      <TextInput 
                        value={novoEvento.date} 
                        placeholder="Data (AAAA-MM-DD)" 
                        placeholderTextColor="#94A3B8"
                        style={[styles.input, { backgroundColor: theme.background, color: theme.text, fontSize: 16 * fontSizeScale }]} 
                        onChangeText={t => setNovoEvento({...novoEvento, date: t})} 
                      />
                      <TextInput 
                        value={novoEvento.time} 
                        placeholder="Hora (HH:MM)" 
                        placeholderTextColor="#94A3B8"
                        style={[styles.input, { backgroundColor: theme.background, color: theme.text, fontSize: 16 * fontSizeScale }]} 
                        onChangeText={t => setNovoEvento({...novoEvento, time: t})} 
                      />
                      <TextInput 
                        value={novoEvento.local} 
                        placeholder="Local" 
                        placeholderTextColor="#94A3B8"
                        style={[styles.input, { backgroundColor: theme.background, color: theme.text, fontSize: 16 * fontSizeScale }]} 
                        onChangeText={t => setNovoEvento({...novoEvento, local: t})} 
                      />
                      <TextInput 
                          value={novoEvento.description}
                          placeholder="Descrição" 
                          placeholderTextColor="#94A3B8"
                          style={[styles.input, { height: 80, textAlignVertical: 'top', backgroundColor: theme.background, color: theme.text, fontSize: 16 * fontSizeScale }]} 
                          multiline 
                          onChangeText={t => setNovoEvento({...novoEvento, description: t})} 
                      />
                      
                      <TouchableOpacity style={styles.saveBtn} onPress={handleSalvar}>
                          <Text style={[styles.saveBtnText, { fontSize: 16 * fontSizeScale }]}>Salvar Evento</Text>
                      </TouchableOpacity>
                  </View>
              </View>
          </View>
      </Modal>

      {/* Modal de Detalhes */}
      <Modal animationType="slide" transparent={true} visible={modalVisible} onRequestClose={() => setModalVisible(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: theme.card }]}>
            <View style={[styles.modalHeader, { backgroundColor: eventSelected ? getEventStatusColor(eventSelected.date) : '#1459b3' }]}>
              <Text style={[styles.modalTitle, { fontSize: 20 * fontSizeScale }]}>{eventSelected?.title}</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Ionicons name="close-circle" size={30} color="white" />
              </TouchableOpacity>
            </View>
            
            <View style={styles.modalBody}>
              <View style={styles.modalInfoRow}>
                <Ionicons name="calendar-outline" size={20 * fontSizeScale} color="#1459b3" />
                <Text style={[styles.modalInfoText, { color: theme.text, fontSize: 16 * fontSizeScale }]}>Data: {eventSelected?.date.split('-').reverse().join('/')}</Text>
              </View>
              <View style={styles.modalInfoRow}>
                <Ionicons name="time-outline" size={20 * fontSizeScale} color="#1459b3" />
                <Text style={[styles.modalInfoText, { color: theme.text, fontSize: 16 * fontSizeScale }]}>Horário: {eventSelected?.time}</Text>
              </View>
              <View style={styles.modalInfoRow}>
                <Ionicons name="location-outline" size={20 * fontSizeScale} color="#1459b3" />
                <Text style={[styles.modalInfoText, { color: theme.text, fontSize: 16 * fontSizeScale }]}>Local: {eventSelected?.local}</Text>
              </View>
              
              <Text style={[styles.descriptionTitle, { color: theme.text, fontSize: 18 * fontSizeScale }]}>Descrição:</Text>
              <Text style={[styles.descriptionText, { color: theme.text, fontSize: 16 * fontSizeScale }]}>{eventSelected?.description || "Sem descrição informada."}</Text>

              {isProfessor && parseInt(idUsuarioLogado) === parseInt(eventSelected?.usuario_id) &&(
                  <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 20 }}>
                      <TouchableOpacity 
                          style={[styles.closeButton, { backgroundColor: '#FF9800', flex: 0.48 }]} 
                          onPress={() => habilitarEdicao(eventSelected)}
                      >
                          <Text style={[styles.closeButtonText, { fontSize: 16 * fontSizeScale }]}>Editar</Text>
                      </TouchableOpacity>

                      <TouchableOpacity 
                          style={[styles.closeButton, { backgroundColor: '#d32f2f', flex: 0.48 }]} 
                          onPress={() => confirmarExclusao(eventSelected.id)}
                      >
                          <Text style={[styles.closeButtonText, { fontSize: 16 * fontSizeScale }]}>Excluir</Text>
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