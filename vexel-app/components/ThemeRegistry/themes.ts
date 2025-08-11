// File: components/ThemeRegistry/themes.ts
import { ThemeOptions } from '@mui/material/styles';
import { Roboto } from 'next/font/google';

// Initialize the Roboto font, a standard for Material Design.
const roboto = Roboto({
    weight: ['300', '400', '500', '700'],
    subsets: ['latin'],
    display: 'swap',
});

// A common base for both themes to avoid repetition.
const baseThemeOptions: ThemeOptions = {
    typography: {
        fontFamily: roboto.style.fontFamily,
        h1: { fontWeight: 700 },
        h2: { fontWeight: 700 },
        h3: { fontWeight: 700 },
        h4: { fontWeight: 600 },
        h5: { fontWeight: 500 },
        button: {
            textTransform: 'none', // For a more modern, less "shouty" UI
            fontWeight: '500',
        }
    },
    shape: {
        borderRadius: 8, // A slightly larger border radius for a modern look
    },
};

// --- LIGHT THEME ---
export const lightThemeOptions: ThemeOptions = {
    ...baseThemeOptions,
    palette: {
        mode: 'light',
        primary: {
            main: '#0D47A1', // A deep, professional blue
            light: '#5472d3',
            dark: '#002171',
        },
        secondary: {
            main: '#C2185B', // A vibrant magenta for secondary actions
        },
        background: {
            default: '#F4F6F8', // A very light grey for the background
            paper: '#FFFFFF', // Pure white for surfaces like cards and drawers
        },
        text: {
            primary: '#212121',
            secondary: '#616161',
        },
        success: { main: '#2e7d32' },
        warning: { main: '#ed6c02' },
        error: { main: '#d32f2f' },
    },
    components: {
        MuiAppBar: {
            styleOverrides: {
                root: {
                    backgroundColor: '#FFFFFF',
                    color: '#212121',
                    boxShadow: '0px 1px 4px rgba(0, 0, 0, 0.08)',
                },
            },
        },
        MuiDrawer: {
            styleOverrides: {
                paper: {
                    backgroundColor: '#FFFFFF',
                    borderRight: 'none',
                }
            }
        },
        MuiButton: {
            styleOverrides: {
                contained: {
                    boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
                    '&:hover': {
                        boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.15)',
                    }
                }
            }
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.05)',
                    border: '1px solid #E0E0E0'
                }
            }
        }
    }
};

// --- DARK THEME ---
export const darkThemeOptions: ThemeOptions = {
    ...baseThemeOptions,
    palette: {
        mode: 'dark',
        primary: {
            main: '#90CAF9', // A lighter, accessible blue for dark mode
        },
        secondary: {
            main: '#F48FB1', // A lighter pink for dark mode
        },
        background: {
            default: '#121212', // Material Design standard dark background
            paper: '#1E1E1E', // Standard dark surface color
        },
        text: {
            primary: '#E0E0E0',
            secondary: '#BDBDBD',
        },
        success: { main: '#66bb6a' },
        warning: { main: '#ffa726' },
        error: { main: '#f44336' },
    },
    components: {
        MuiAppBar: {
            styleOverrides: {
                root: {
                    backgroundColor: '#1E1E1E',
                    backgroundImage: 'none', // Remove gradient from dark mode AppBar
                },
            },
        },
        MuiDrawer: {
            styleOverrides: {
                paper: {
                    backgroundColor: '#1E1E1E',
                }
            }
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    border: '1px solid #424242',
                }
            }
        }
    }
};

