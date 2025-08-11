// File: components/Chat/ChatInterface.tsx
'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Box, TextField, Button, Paper, CircularProgress, Typography, Alert } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ChatBubble from './ChatBubble';
import { Part_Output, Part_Input} from '@/lib/adk-client'

interface ChatInterfaceProps {
    agentName: string;
    agentDescription: string;
    getAgentResponse: (history: Part_Output[]) => Promise<Part_Output[]>;
    initialMessages: Part_Output[];
}

export default function ChatInterface({ agentName, agentDescription, getAgentResponse, initialMessages }: ChatInterfaceProps) {
    const [messages, setMessages] = useState<Part_Output[]>(initialMessages);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        console.log("Messages:", messages);
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        setError(null);
        const userMessage: Part_Input = {
            text: input,
            role: 'user'
        };

        const newMessages = [...messages, userMessage as Part_Output];
        setMessages(newMessages);
        setInput('');
        setIsLoading(true);

        try {
            const agentMessage = await getAgentResponse(newMessages);
            setMessages(prev => [...prev, ...agentMessage]);
        } catch (err: any) {
            const errorMessageContent = err.message || 'Sorry, there was an error communicating with the agent.';
            setError(errorMessageContent);

            const errorMessage: Part_Output = {
                text: errorMessageContent,
            }
            setMessages(prev => [...prev, errorMessage]);
            console.error("Agent request failed:", err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Paper elevation={3} sx={{ height: 'calc(100vh - 120px)', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
                <Typography variant="h5">{agentName}</Typography>
                <Typography variant="body2" color="text.secondary">{agentDescription}</Typography>
            </Box>
            <Box sx={{ flexGrow: 1, overflowY: 'auto', p: 2 }}>
                {messages.map((msg, index) => (
                    <div key={`message-key-${index}`} ref={index === messages.length - 1 ? scrollRef : null}>
                        <ChatBubble message={ {role: 'agent', content: msg.text }} />
                    </div>
                ))}
                {isLoading && (
                    <Box sx={{ display: 'flex', justifyContent: 'flex-start', m: 1 }}>
                        <CircularProgress size={24} />
                    </Box>
                )}
            </Box>
            {error && <Alert severity="error" sx={{ m: 2 }}>{error}</Alert>}
            <Box
                component="form"
                sx={{ p: 2, borderTop: 1, borderColor: 'divider', display: 'flex', gap: 1 }}
                onSubmit={(e) => { e.preventDefault(); handleSend(); }}
            >
                <TextField
                    fullWidth
                    variant="outlined"
                    placeholder="Type your message..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    disabled={isLoading}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleSend();
                        }
                    }}
                />
                <Button variant="contained" type="submit" endIcon={<SendIcon />} disabled={isLoading || !input.trim()}>
                    Send
                </Button>
            </Box>
        </Paper>
    );
}

