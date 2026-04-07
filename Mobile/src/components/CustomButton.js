import { TouchableOpacity, Text, StyleSheet } from 'react-native';

// criando os parametros title e onPress para o componente, para personalizar o texto do botão e a ação ao clicar
export default function CustomButton({ title, onPress }) {
    return (
        // Permite passar as props title e onPress para o componente, para personalizar o texto do botão e a ação ao clicar
        <TouchableOpacity style={style.button} onPress={onPress}>
            <Text style={style.text}>{title}</Text>
        </TouchableOpacity>
    );
}

// estilos para o botão personalizado
const style = StyleSheet.create({
    button: {
        backgroundColor: '#0e68d6',
        width: '80%',
        padding: 15,
        borderRadius: 8,
        alignItems: 'center',
        marginTop: 10
    },

    text: {
        color: '#ffffff',
        fontSize: 16,
        fontWeight: 'bold'
    }
});