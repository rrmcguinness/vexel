// File: components/ThemeRegistry/ThemeContext.tsx
'use client';
import { createContext, useState, useMemo, ReactNode, useContext } from 'react';
import { createTheme, Theme } from '@mui/material/styles';
import { lightThemeOptions, darkThemeOptions } from './themes';

interface ThemeContextType {
    mode: 'light' | 'dark';
    toggleColorMode: () => void;
    theme: Theme;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeContextProvider = ({ children }: { children: ReactNode }) => {
    const [mode, setMode] = useState<'light' | 'dark'>('light');

    const toggleColorMode = () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
    };

    const theme = useMemo(
        () => (mode === 'light' ? createTheme(lightThemeOptions) : createTheme(darkThemeOptions)),
        [mode]
    );

    return (
        <ThemeContext.Provider value={{ mode, toggleColorMode, theme }}>
            {children}
        </ThemeContext.Provider>
    );
};

export const useThemeContext = () => {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useThemeContext must be used within a ThemeContextProvider');
    }
    return context;
};

