// File: app/login/page.tsx
'use client';

import React, { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { Container, Paper, Typography, Button, Box, CircularProgress, Alert } from '@mui/material';
import GoogleIcon from '@mui/icons-material/Google';

export default function LoginPage() {
    const { user, isLoading } = useAuth();
    const router = useRouter();
    const searchParams = useSearchParams();
    const error = searchParams.get('error');

    useEffect(() => {
        // If the auth state is not loading and a user is logged in,
        // redirect them to the home page.
        if (!isLoading && user) {
            router.replace('/');
        }
    }, [user, isLoading, router]);

    const handleLogin = () => {
        // Redirect to the backend login endpoint. This is a security best practice.
        window.location.href = '/api/auth/login';
    };

    // While the session is being verified, display a loading indicator.
    // This prevents a "flash" of the login page for authenticated users
    // who are being redirected.
    if (isLoading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress />
                <Typography sx={{ ml: 2 }}>Verifying session...</Typography>
            </Box>
        );
    }

    // If the user is not logged in and the auth state is no longer loading,
    // display the login page.
    if (!user) {
        return (
            <Container component="main" maxWidth="xs">
                <Paper
                    elevation={6}
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        padding: { xs: 3, sm: 4 },
                        borderRadius: 2,
                    }}
                >
                    <Typography component="h1" variant="h4" sx={{ mb: 1, fontWeight: 'bold' }}>
                        Sign In
                    </Typography>
                    <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 3 }}>
                        Use your Google account to access the Agent Portal.
                    </Typography>

                    {error && (
                        <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
                            {error}
                        </Alert>
                    )}

                    <Button
                        type="button"
                        fullWidth
                        variant="contained"
                        startIcon={<GoogleIcon />}
                        onClick={handleLogin}
                        size="large"
                        sx={{ mt: 2, mb: 2, textTransform: 'none', fontSize: '1rem' }}
                    >
                        Sign In with Google
                    </Button>
                </Paper>
            </Container>
        );
    }

    // If the user is authenticated, render nothing while the redirect occurs.
    return null;
}
