import { TextInput, StyleSheet } from "react-native";

export default function CustomInput({ style: customStyle, placeholderTextColor = '#64748B', selectionColor = '#1459b3', ...props }) {
    return (
        <TextInput
            style={[styles.input, customStyle]}
            placeholderTextColor={placeholderTextColor}
            selectionColor={selectionColor}
            keyboardAppearance="light"
            {...props}
        />
    );
}

const styles = StyleSheet.create({
    input: {
        width: '100%',
        borderWidth: 1,
        padding: 15,
        marginTop: 15,
        borderRadius: 8,
        borderColor: '#cccccc',
        backgroundColor: '#fff',
        color: '#1E293B',
    }
});