'use client';
import AppLayout from '@/components/Layout/AppLayout';
import { Container, Typography, Paper, Grid, Card, CardContent, CardHeader, Avatar } from '@mui/material';
import AssessmentIcon from '@mui/icons-material/Assessment';
import CodeIcon from '@mui/icons-material/Code';
import SecurityIcon from '@mui/icons-material/Security';
import React from 'react';
import Link from 'next/link'

export default function WelcomePage() {
    return (
        <AppLayout>

            <Container maxWidth="lg" sx={{ py: 4 }}>
                <Paper elevation={0} sx={{ p: { xs: 2, sm: 4 }, mb: 4, backgroundColor: 'transparent' }}>
                    <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ fontWeight: 700 }}>
                        Welcome to the ADK Agent Interface
                    </Typography>
                    <Typography variant="h6" color="text.secondary" align="center">
                        A powerful, secure, and intuitive platform to interact with specialized Google Cloud agents.
                    </Typography>
                </Paper>

                <Grid container spacing={4} justifyContent="center">
                    <Grid size={{ sm: 12, md: 6}}>
                        <Card sx={{ height: '100%' }}>
                            <CardHeader
                                avatar={
                                    <Avatar sx={{ bgcolor: 'primary.main' }}>
                                        <AssessmentIcon />
                                    </Avatar>
                                }
                                title="Sales Reporting Agent"
                            />
                            <CardContent>
                                <Link href="/adk/concord_sql_agent">
                                <Typography variant="body1" color="text.secondary">
                                    Navigate to the <strong>Sales Reports</strong> page to engage with our sales agent. Ask for quarterly summaries, regional performance, or product breakdowns to get instant, data-driven answers through a conversational interface.
                                </Typography>
                                </Link>
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid size={{ sm: 12, md: 6}}>
                        <Card sx={{ height: '100%' }}>
                            <CardHeader
                                avatar={
                                    <Avatar sx={{ bgcolor: 'secondary.main' }}>
                                        <CodeIcon />
                                    </Avatar>
                                }
                                title="Interactive SQL Agent"
                            />
                            <CardContent>
                                <Typography variant="body1" color="text.secondary">
                                    The <strong>SQL Chat</strong> page connects you to a BigQuery expert. Describe the data you need in plain English. The agent will generate, validate, and provide results from the underlying SQL query for you.
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid size={{sm: 12, md: 6}}>
                        <Card sx={{ mt: 2, border: '1px solid', borderColor: 'divider' }}>
                            <CardHeader
                                avatar={
                                    <Avatar sx={{ bgcolor: 'success.main' }}>
                                        <SecurityIcon />
                                    </Avatar>
                                }
                                title="Secure & Professional"
                            />
                            <CardContent>
                                <Typography variant="body1" color="text.secondary">
                                    Built on Next.js with MUI for a professional look and feel. Authentication is handled seamlessly and securely via Google Cloud IAP for corporate environments, with a standard OAuth fallback for other scenarios.
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                </Grid>
            </Container>
        </AppLayout>
    );
}
