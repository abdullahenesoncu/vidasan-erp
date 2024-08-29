import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, IconButton, Box, Menu, MenuItem } from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import { logoutUser } from './actions/authentication';

const Navbar = () => {
    const navigate = useNavigate();
    const [anchorEl, setAnchorEl] = useState(null);

    const handleLogout = () => {
        logoutUser()  // Call logout API
            .then(() => {
                localStorage.removeItem('token');  // Remove token from localStorage
                localStorage.removeItem('user');   // Remove user from localStorage
                navigate('/login');  // Redirect to login page
            })
            .catch((error) => {
                console.error('Error during logout:', error);
            });
    };

    const handleLogoClick = () => {
        navigate('/'); // Redirect to the home page
    };

    const handleNavigate = (path) => {
        navigate(path); // Navigate to the specified path
        setAnchorEl(null); // Close the menu after selection
    };

    const handleMenuClick = (event) => {
        setAnchorEl(event.currentTarget); // Open the menu
    };

    const handleMenuClose = () => {
        setAnchorEl(null); // Close the menu
    };

    return (
        <AppBar position="static">
            <Toolbar>
                <IconButton edge="start" color="inherit" aria-label="home" onClick={handleLogoClick}>
                    <img src="/logo.png" alt="Vidasan ERP" style={{ height: 40 }} />
                </IconButton>
                <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
                    <Button color="inherit" onClick={handleMenuClick}>
                        Siparis
                    </Button>
                    <Menu
                        anchorEl={anchorEl}
                        open={Boolean(anchorEl)}
                        onClose={handleMenuClose}
                    >
                        <MenuItem onClick={() => handleNavigate('/siparis')}>Tüm Siparişler</MenuItem>
                        <MenuItem onClick={() => handleNavigate('/siparis-press')}>Press Durumu</MenuItem>
                        <MenuItem onClick={() => handleNavigate('/siparis-byck')}>Byck Durumu</MenuItem>
                        <MenuItem onClick={() => handleNavigate('/siparis-ovalama')}>Ovalama Durumu</MenuItem>
                        <MenuItem onClick={() => handleNavigate('/siparis-sementasyon')}>Sementasyon Durumu</MenuItem>
                        <MenuItem onClick={() => handleNavigate('/siparis-kaplama')}>Kaplama Durumu</MenuItem>
                        <MenuItem onClick={() => handleNavigate('/siparis-ambalaj')}>Ambalaj Durumu</MenuItem>
                        <MenuItem onClick={() => handleNavigate('/siparis-upcoming')}>Yaklaşan Siparişler</MenuItem>
                        <MenuItem onClick={() => handleNavigate('/siparis-completed')}>Tamamlanan Siparişler</MenuItem>
                    </Menu>
                    <Button color="inherit" onClick={() => handleNavigate('/machine')}>
                        Makine
                    </Button>
                </Box>
                <Button color="inherit" onClick={handleLogout} startIcon={<LogoutIcon />}>
                    Logout
                </Button>
            </Toolbar>
        </AppBar>
    );
};

export default Navbar;
