'use client';

import React from 'react';
import { Box, Paper } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { coy, a11yDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { Event_Output } from '@/lib/adk-client';

const CodeBlock = ({ node, inline, className, children, ...props }: any) => {
    const theme = useTheme();
    const match = /language-(\w+)/.exec(className || '');

    return !inline && match ? (
        <SyntaxHighlighter
            style={theme.palette.mode === 'dark' ? a11yDark : coy}
            language={match[1]}
            PreTag="div"
            {...props}
        >
            {String(children).replace(/\n$/, '')}
        </SyntaxHighlighter>
    ) : (
        <code className={className} {...props} style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '2px 4px', borderRadius: '4px' }}>
            {children}
        </code>
    );
};


interface ChatBubbleProps {
    message: {
        role: 'user' | 'agent' | 'system' | 'model';
        content: string | undefined | null;
    };
}

export default function ChatBubble({ message }: ChatBubbleProps) {
    const theme = useTheme();
    const isUser = message.role === 'user';
    const isSystem = message.role === 'system' || message.role === 'agent' || message.role === 'model';

    const align = isUser ? 'flex-end' : 'flex-start';
    const bgColor = isSystem
        ? theme.palette.error.dark
        : (isUser ? theme.palette.primary.main : theme.palette.background.paper);
    const textColor = isSystem
        ? theme.palette.error.contrastText
        : (isUser ? theme.palette.primary.contrastText : theme.palette.text.primary);

    return (
        <Box sx={{ display: 'flex', justifyContent: align, my: 1 }}>
            <Paper
                elevation={1}
                sx={{
                    p: 1.5,
                    maxWidth: '80%',
                    bgcolor: bgColor,
                    color: textColor,
                    borderRadius: isUser ? '20px 20px 5px 20px' : '20px 20px 20px 5px',
                    overflowWrap: 'break-word',
                }}
            >
                <Markdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                        code({node, className, children, ...props}) {
                            const match = /language-(\w+)/.exec(className || '')
                            return match ? (
                                <SyntaxHighlighter
                                    style={theme.palette.mode === 'dark' ? a11yDark : coy}
                                    language={match[1]}
                                    PreTag="div"
                                >{String(children).replace(/\n$/, '')}</SyntaxHighlighter>
                            ) : (
                                <code className={className} {...props} style={{backgroundColor: 'rgba(255,255,255,0.1)', padding: '2px 4px', borderRadius: '4px'}}>
                                    {children}
                                </code>
                            )
                        }
                    }}
                >
                    {message.content}
                </Markdown>
            </Paper>
        </Box>
    );
}
