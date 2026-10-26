import { TouchableOpacity, Text, StyleSheet } from 'react-native';

// criando os parametros title e onPress para o componente, para personalizar o texto do botão e a ação ao clicar
export default function CustomButton({ title, onPress, style }) {
    return (
        // Permite passar as props title e onPress para o componente, para personalizar o texto do botão e a ação ao clicar
        <TouchableOpacity style={[buttonStyles.button, style]} onPress={onPress}>
            <Text style={buttonStyles.text}>{title}</Text>
        </TouchableOpacity>
    );
}

// estilos para o botão personalizado
const buttonStyles = StyleSheet.create({
    button: {
        backgroundColor: '#0e68d6',
        width: '100%',
        maxWidth: 450,
        paddingVertical: 14,
        paddingHorizontal: 18,
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