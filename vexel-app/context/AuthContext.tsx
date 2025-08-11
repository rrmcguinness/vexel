"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";

interface User {
    name: string;
    email: string;
    picture?: string;
}

interface AuthContextType {
    user: User | null;
    loading: boolean;
    login: () => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const verifySession = async () => {
            try {
                const response = await fetch('/api/auth/session');
                if (response.ok) {
                    const data = await response.json();
                    setUser(data.user);
                } else {
                    setUser(null);
                }
            } catch (error) {
                console.error('Failed to verify session:', error);
                setUser(null);
            } finally {
                setLoading(false);
            }
        };
        verifySession();
    }, []);

    const login = () => {
        window.location.href = '/api/auth/login';
    };

    const logout = async () => {
        try {
            await fetch('/api/auth/logout');
            setUser(null);
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    // Render children immediately and let the middleware handle redirects.
    // The context will update with user/loading state once the session check is complete.
    return (
        <AuthContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};