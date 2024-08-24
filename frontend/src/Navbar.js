import React from 'react';
import { useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, IconButton, Box } from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import { logoutUser } from './actions/authentication';

const Navbar = () => {
    const navigate = useNavigate();

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
    };

    return (
        <AppBar position="static">
            <Toolbar>
                <IconButton edge="start" color="inherit" aria-label="home" onClick={handleLogoClick}>
                    <img src="/logo.png" alt="Vidasan ERP" style={{ height: 40 }} />
                </IconButton>
                <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
                    <Button color="inherit" onClick={() => handleNavigate('/siparis')}>
                        Siparis
                    </Button>
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
