import React from 'react';
import { useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, IconButton } from '@mui/material';
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

    return (
        <AppBar position="static">
            <Toolbar>
                <IconButton edge="start" color="inherit" aria-label="home" onClick={handleLogoClick}>
                    <img src="/logo.png" alt="Vidasan ERP" style={{ height: 40 }} />
                </IconButton>
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    ERP
                </Typography>
                <Button color="inherit" onClick={handleLogout} startIcon={<LogoutIcon />}>
                    Logout
                </Button>
            </Toolbar>
        </AppBar>
    );
};

export default Navbar;
