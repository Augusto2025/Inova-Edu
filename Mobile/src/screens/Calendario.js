import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { Calendar, LocaleConfig } from 'react-native-calendars';
import { Ionicons } from '@expo/vector-icons'; // Ícones nativos do Expo

// Configuração do calendário para Português
LocaleConfig.locales['pt-br'] = {
  monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
  monthNamesShort: ['Jan.','Fev.','Mar','Abr','Mai','Jun','Jul.','Ago','Set.','Out.','Nov.','Dez.'],
  dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
  dayNamesShort: ['D','S','T','Q','Q','S','S'],
  today: 'Hoje'
};
LocaleConfig.defaultLocale = 'pt-br';

export default function CalendarScreen() {
  const [selected, setSelected] = useState('');

  // Exemplo de dados de eventos
  const events = [
    { id: 1, title: 'Palestra: Inovação na Educação', time: '19 set. de 19:00', local: 'Auditório Central', color: '#4CAF50', icon: 'school' },
    { id: 2, title: 'Prova: Matemática Aplicada', time: '20 set. de 19:00', local: 'Salas 101-103', color: '#FF9800', icon: 'document-text' },
    { id: 3, title: 'Entrega de Projeto: Hackathon', time: '20 set. de 18:00', local: 'Plataforma Online', color: '#1459b3', icon: 'star' },
  ];

  return (
    <View style={styles.container}>
      {/* HEADER AZUL ARREDONDADO */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>CALENDÁRIO</Text>
      </View>

      <ScrollView contentContainerStyle={{ flexGrow: 1, paddingBottom: 100 }}>
        {/* CALENDÁRIO CENTRALIZADO */}
        <View style={styles.calendarContainer}>
          <Calendar
            onDayPress={day => setSelected(day.dateString)}
            markedDates={{
              [selected]: { selected: true, disableTouchEvent: true, selectedColor: '#1459b3' },
              '2023-09-05': { marked: true, dotColor: '#1459b3' },
              '2023-09-12': { marked: true, dotColor: '#1459b3' },
              '2023-09-22': { marked: true, dotColor: '#1459b3' },
            }}
            theme={{
              backgroundColor: '#ffffff',
              calendarBackground: '#ffffff',
              textSectionTitleColor: '#1459b3',
              selectedDayBackgroundColor: '#1459b3',
              selectedDayTextColor: '#ffffff',
              todayTextColor: '#1459b3',
              dayTextColor: '#2d4150',
              arrowColor: '#1459b3',
              monthTextColor: '#1459b3',
              textMonthFontWeight: 'bold',
              textDayHeaderFontWeight: 'bold',
            }}
          />
        </View>

        {/* LISTA DE EVENTOS */}
        <View style={styles.eventSection}>
          <Text style={styles.eventSectionTitle}>Eventos do Mês</Text>
          
          {events.map(event => (
            <View key={event.id} style={styles.eventCard}>
              <View style={[styles.iconContainer, { backgroundColor: event.color }]}>
                <Ionicons name={event.icon} size={24} color="white" />
              </View>
              <View style={styles.eventInfo}>
                <Text style={styles.eventTime}>{event.time}</Text>
                <Text style={styles.eventTitle}>{event.title}</Text>
                <Text style={styles.eventLocal}>{event.local}</Text>
              </View>
            </View>
          ))}
        </View>
      </ScrollView>

      {/* BOTÃO FLUTUANTE (FAB) */}
      <TouchableOpacity style={styles.fab}>
        <Ionicons name="add" size={30} color="white" />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F7FA',
  },
  header: {
    backgroundColor: '#1459b3',
    height: 120,
    justifyContent: 'center',
    alignItems: 'center',
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
    elevation: 5,
  },
  headerTitle: {
    color: '#FFF',
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 20,
  },
  calendarContainer: {
    backgroundColor: '#FFF',
    margin: 15,
    borderRadius: 20,
    padding: 10,
    elevation: 3,
  },
  eventSection: {
    paddingHorizontal: 20,
  },
  eventSectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  eventCard: {
    backgroundColor: '#FFF',
    flexDirection: 'row',
    padding: 15,
    borderRadius: 15,
    marginBottom: 12,
    alignItems: 'center',
    elevation: 2,
  },
  iconContainer: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  eventInfo: {
    flex: 1,
  },
  eventTime: {
    fontSize: 12,
    color: '#666',
  },
  eventTitle: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#333',
  },
  eventLocal: {
    fontSize: 13,
    color: '#888',
  },
  fab: {
    position: 'absolute',
    right: 20,
    bottom: 20,
    backgroundColor: '#1459b3',
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
  }
});