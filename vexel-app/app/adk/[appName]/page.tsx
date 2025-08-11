// File: app/adk/[appName]/page.tsx
'use client';

import React, { useState, useEffect, useCallback, use } from 'react';
import { Box, CircularProgress, Typography, Alert } from '@mui/material';
import ChatInterface from '@/components/Chat/ChatInterface';
import axios from "axios";
import { Part_Output } from '@/lib/adk-client'

// Helper to format the app name for display
const formatAgentName = (appName: string) => {
    return appName
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
};

export default function AdkChatPage({ params }: { params: { appName: string } }) {
    const { appName } = use(params);
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [initialMessages, setInitialMessages] = useState<Part_Output[]>([]);

    // 1. Create a session when the component mounts
    useEffect(() => {
        const createSession = async () => {
            try {
                setError(null);
                setIsLoading(true);
                axios.post(`/api/adk/${appName}/session`).then(r => {
                    console.log(r)
                    if (r.data) {
                        setInitialMessages(r.data);
                    }
                    setSessionId(r.data.id);
                }).catch(e => {
                    setError(e.response.data.message);
                });

            } catch (err: any) {
                const errorMessage = err.response?.data?.message || 'Failed to create a new session.';
                setError(errorMessage);
                console.error("Session creation failed:", err);
            } finally {
                setIsLoading(false);
            }
        };

        if (appName) {
            createSession().then(() => {
                setIsLoading(false);
            });
        }
    }, [appName, setInitialMessages]);

    // 2. Delete the session when the user navigates away
    useEffect(() => {
        const deleteSession = () => {
            if (sessionId) {
                // Use fetch with keepalive for reliability on page unload
                fetch(`/api/adk/${appName}?sessionId=${sessionId}`, {
                    method: 'DELETE',
                    keepalive: true,
                });
            }
        };

        window.addEventListener('beforeunload', deleteSession);
        return () => {
            window.removeEventListener('beforeunload', deleteSession);
            // Also call delete on component unmount for SPA navigation
            deleteSession(); 
        };
    }, [sessionId, appName]);

    // 3. Define the function to get the agent's response
    const getAgentResponse = useCallback(async (history: any[]): Promise<any> => {
        if (!sessionId) {
            throw new Error("Session not initialized. Please refresh the page.");
        }
        try {
            const response = await axios.post(`/api/adk/${appName}`, { history, sessionId });

            return response.data;
        } catch (err: any) {
            const errorMessage = err.response?.data?.message || 'The agent returned an error.';
            throw new Error(errorMessage);
        }
    }, [appName, sessionId]);

    if (isLoading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                <CircularProgress />
                <Typography sx={{ ml: 2 }}>Initializing Session...</Typography>
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={{ p: 4 }}>
                <Alert severity="error">
                    <Typography variant="h6">Failed to load agent</Typography>
                    <Typography>{error}</Typography>
                </Alert>
            </Box>
        );
    }

    return (
        <ChatInterface
            agentName={`${formatAgentName(appName)} Agent`}
            agentDescription={`This is an interactive chat with the ${appName} agent.`}
            getAgentResponse={getAgentResponse}
            initialMessages={initialMessages}
        />
    );
}
