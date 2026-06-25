import React, { createContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
    const [isDarkMode, setIsDarkMode] = useState(false);
    // 1.0 = Normal, 1.2 = Grande, 1.4 = Muito Grande
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

    const toggleDarkMode = async () => {
        const newValue = !isDarkMode;
        setIsDarkMode(newValue);
        await AsyncStorage.setItem('isDarkMode', JSON.stringify(newValue));
    };

    // Altera o tamanho da fonte em ciclo (Normal -> Grande -> Muito Grande -> Normal)
    const alterarTamanhoFonte = async () => {
        let novaEscala = 1.0;
        if (fontSizeScale === 1.0) novaEscala = 1.2;
        else if (fontSizeScale === 1.2) novaEscala = 1.4;
        else novaEscala = 1.0;

        setFontSizeScale(novaEscala);
        await AsyncStorage.setItem('fontSizeScale', JSON.stringify(novaEscala));
    };

    // Retorna o texto amigável do tamanho atual
    const obterNomeTamanhoFonte = () => {
        if (fontSizeScale === 1.0) return "Normal";
        if (fontSizeScale === 1.2) return "Grande";
        return "Muito Grande";
    };

    const theme = {
        background: isDarkMode ? '#121212' : '#F8FAFC',
        card: isDarkMode ? '#1E1E1E' : '#FFFFFF',
        text: isDarkMode ? '#E2E8F0' : '#1E293B',
        primary: '#1459b3',
        border: isDarkMode ? '#2D3748' : '#EEE',
    };

    return (
        <ThemeContext.Provider value={{ 
            isDarkMode, 
            toggleDarkMode, 
            fontSizeScale, 
            alterarTamanhoFonte, 
            obterNomeTamanhoFonte, 
            theme 
        }}>
            {children}
        </ThemeContext.Provider>
    );
};