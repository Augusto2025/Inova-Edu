import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Modal, Pressable } from 'react-native';
import { Calendar, LocaleConfig } from 'react-native-calendars';
import { Ionicons } from '@expo/vector-icons';
import Header from '../components/Header';
import { COLORS } from '../components/Cores';
import styles from '../styles/Evento';

export default function CalendarScreen() {
  const [selected, setSelected] = useState('');
  const [modalVisible, setModalVisible] = useState(false);
  const [eventSelected, setEventSelected] = useState(null);

  // Dados com horário e descrição
  const events = [
    { id: 1, title: 'Palestra: Inovação', date: '2026-04-10', day: '10', month: 'ABR', time: '19:00', local: 'Auditório', description: 'Uma palestra incrível sobre as novas tecnologias no setor educacional em 2026.' },
    { id: 2, title: 'Reunião de Pais', date: '2026-04-01', day: '01', month: 'ABR', time: '08:30', local: 'Sala 05', description: 'Alinhamento semestral com os responsáveis sobre o desempenho dos alunos.' },
    { id: 3, title: 'Entrega de Notas', date: '2026-03-25', day: '25', month: 'MAR', time: '14:00', local: 'Online', description: 'Publicação oficial das notas no portal do aluno.' },
  ];

  const getEventStatusColor = (eventDate) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const evDate = new Date(eventDate);
    evDate.setHours(0, 0, 0, 0);

    if (evDate.getTime() === today.getTime()) return '#FFD700';
    return evDate > today ? '#4CAF50' : '#F44336';
  };

  // Função para abrir o modal ao clicar no dia ou card
  const handleOpenEvent = (dateString) => {
    const foundEvent = events.find(e => e.date === dateString);
    if (foundEvent) {
      setEventSelected(foundEvent);
      setModalVisible(true);
    }
    setSelected(dateString);
  };

  return (
    <View style={styles.container}>
      <Header nomeTela={"Calendário"} />

      <ScrollView contentContainerStyle={{ flexGrow: 1, paddingBottom: 100 }}>
        <View style={styles.calendarContainer}>
          <Calendar
            onDayPress={day => handleOpenEvent(day.dateString)}
            markedDates={{
              [selected]: { selected: true, selectedColor: '#1459b3' },
              '2026-05-10': { marked: true, dotColor: '#4CAF50' },
              '2026-05-01': { marked: true, dotColor: '#FFD700' },
            }}
            theme={{
              // Círculo azul no dia de hoje
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
          <Text style={styles.eventSectionTitle}>Eventos do Mês</Text>
          
          {events.map(event => {
            const statusColor = getEventStatusColor(event.date);
            return (
              <TouchableOpacity 
                key={event.id} 
                style={styles.eventCard} 
                onPress={() => handleOpenEvent(event.date)}
              >
                <View style={[styles.dateBadge, { borderColor: statusColor }]}>
                   <View style={[styles.dateBadgeTop, { backgroundColor: statusColor }]}>
                      <Text style={styles.monthText}>{event.month}</Text>
                   </View>
                   <View style={styles.dateBadgeBottom}>
                      <Text style={[styles.dayText, { color: '#333' }]}>{event.day}</Text>
                   </View>
                </View>

                <View style={styles.eventInfo}>
                  <Text style={styles.eventTitle}>{event.title}</Text>
                  <Text style={styles.eventTimeInfo}>
                    <Ionicons name="time-outline" size={12} /> {event.time} • {event.local}
                  </Text>
                </View>
                <View style={[styles.statusDot, { backgroundColor: statusColor }]} />
              </TouchableOpacity>
            );
          })}
        </View>
      </ScrollView>

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
              <Text style={styles.descriptionText}>{eventSelected?.description}</Text>
              
              <TouchableOpacity 
                style={styles.closeButton} 
                onPress={() => setModalVisible(false)}
              >
                <Text style={styles.closeButtonText}>Fechar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}
