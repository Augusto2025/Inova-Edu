import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function Footer() {
  return (
    <View style={styles.footer}>
      <TouchableOpacity>
        <Text style={styles.text}>🏠</Text>
        <Text style={styles.label}>Home</Text>
      </TouchableOpacity>

      <TouchableOpacity>
        <Text style={styles.text}>📅</Text>
        <Text style={styles.label}>Eventos</Text>
      </TouchableOpacity>

      <TouchableOpacity>
        <Text style={styles.text}>💬</Text>
        <Text style={styles.label}>Fórum</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  footer: {
    position: 'absolute',
    bottom: 0,
    width: '100%',
    backgroundColor: '#1459b3',
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 15,
  },

  text: {
    color: '#fff',
    fontSize: 20,
    textAlign: 'center',
  },

  label: {
    color: '#fff',
    fontSize: 12,
    textAlign: 'center',
  },
});