"use client";

import React from 'react';
import AppHeader from "./AppHeader";
import {Box} from "@mui/material";

const AppLayout = ({ children }: { children: React.ReactNode }) => {
    const [drawerOpen, setDrawerOpen] = React.useState(false)

    const handleDrawerToggle = () => {
        setDrawerOpen(!drawerOpen)
    }

    return (
        <Box>
            <AppHeader drawerWidth={0} handleDrawerToggle={handleDrawerToggle} />
            <main>
                {children}
            </main>
        </Box>
    );
};

export default AppLayout;
