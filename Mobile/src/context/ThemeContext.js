import React, { createContext, useState, useEffect, useContext, useCallback, useMemo } from 'react'; // Importado useContext
import AsyncStorage from '@react-native-async-storage/async-storage';

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
    const [isDarkMode, setIsDarkMode] = useState(false);
    const [fontSizeScale, setFontSizeScale] = useState(1.0);

    useEffect(() => {
        const loadSettings = async () => {
            const savedTheme = await AsyncStorage.getItem('isDarkMode');
            const savedFont = await AsyncStorage.getItem('fontSizeScale');
            if (savedTheme !== null) setIsDarkMode(JSON.parse(savedTheme));
            if (savedFont !== null) setFontSizeScale(JSON.parse(savedFont));
        };
        loadSettings();
    }, []);

    const toggleDarkMode = useCallback(async () => {
        const newValue = !isDarkMode;
        setIsDarkMode(newValue);
        await AsyncStorage.setItem('isDarkMode', JSON.stringify(newValue));
    }, [isDarkMode]);

    const alterarTamanhoFonte = useCallback(async () => {
        let novaEscala = 1.0;
        if (fontSizeScale === 1.0) novaEscala = 1.2;
        else if (fontSizeScale === 1.2) novaEscala = 1.4;
        else novaEscala = 1.0;

        setFontSizeScale(novaEscala);
        await AsyncStorage.setItem('fontSizeScale', JSON.stringify(novaEscala));
    }, [fontSizeScale]);

    const obterNomeTamanhoFonte = useCallback(() => {
        if (fontSizeScale === 1.0) return "Normal";
        if (fontSizeScale === 1.2) return "Grande";
        return "Muito Grande";
    }, [fontSizeScale]);

    const theme = useMemo(() => ({
        background: isDarkMode ? '#121212' : '#F8FAFC',
        card: isDarkMode ? '#1E1E1E' : '#FFFFFF',
        text: isDarkMode ? '#E2E8F0' : '#1E293B',
        primary: '#1459b3',
        border: isDarkMode ? '#2D3748' : '#EEE',
    }), [isDarkMode]);

    const value = useMemo(() => ({
        isDarkMode,
        toggleDarkMode,
        fontSizeScale,
        alterarTamanhoFonte,
        obterNomeTamanhoFonte,
        theme
    }), [isDarkMode, toggleDarkMode, fontSizeScale, alterarTamanhoFonte, obterNomeTamanhoFonte, theme]);

    return (
        <ThemeContext.Provider value={value}>
            {children}
        </ThemeContext.Provider>
    );
};

// ADICIONE ESTA LINHA ABAIXO:
export const useTheme = () => useContext(ThemeContext);