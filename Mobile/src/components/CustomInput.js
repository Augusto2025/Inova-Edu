import { TextInput, StyleSheet } from "react-native";

export default function CustomInput(props) {
    return (
        <TextInput
        style={style.input}
        // Permite passar todas as props para a proxima camada, como placeholder, value, onChangeText, etc.
        {...props}
        />
    );
}

const style = StyleSheet.create({
    input: {
        width: '80%',
        borderWidth: 1,
        padding: 15,
        margin: 15,
        borderRadius: 8,
        borderColor: '#cccccc',
    }
})