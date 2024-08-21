import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser, resetPasswordRequest } from '../actions/authentication';
import { TextField, Button, Container, Typography, Box, Alert, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';

const LoginPage = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);
    const [resetPasswordDialog, setResetPasswordDialog] = useState(false);
    const [resetEmail, setResetEmail] = useState('');
    const [resetSuccess, setResetSuccess] = useState(null);

    // Handle input changes for the login form
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    // Handle login form submission
    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        // Call the login action
        loginUser(formData)
            .then((response) => {
                const user = response.data;

                // Check if user is verified
                if (!user.user_verified) {
                    setError('User is not verified.');
                    setLoading(false);
                    return;
                }

                // Store the token and user in localStorage
                localStorage.setItem('token', user.token);
                localStorage.setItem('user', JSON.stringify(user)); // Save user object
                console.log(user);

                // Proceed with login success
                setSuccess(true);
                setLoading(false);
                setError(null);
                navigate('/siparis');  // Redirect to home page after login
            })
            .catch((error) => {
                setLoading(false);
                setError(error.response ? error.response.data.detail : 'Login failed');
            });
    };

    // Handle password reset request
    const handleResetPassword = () => {
        resetPasswordRequest(resetEmail)
            .then((response) => {
                setResetSuccess(true);
                setResetPasswordDialog(false);
            })
            .catch((error) => {
                setResetSuccess(false);
                setError(error.response ? error.response.data.detail : 'Password reset request failed');
            });
    };

    return (
        <Container maxWidth="sm">
            <Box sx={{ mt: 5 }}>
                <Typography variant="h4" gutterBottom>
                    Login
                </Typography>

                {error && <Alert severity="error">{error}</Alert>}
                {success && <Alert severity="success">Login successful!</Alert>}

                <form onSubmit={handleSubmit}>
                    <TextField
                        label="Email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        fullWidth
                        margin="normal"
                        required
                        type="email"
                    />
                    <TextField
                        label="Password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        fullWidth
                        margin="normal"
                        required
                        type="password"
                    />

                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        fullWidth
                        disabled={loading}
                        sx={{ mt: 2 }}
                    >
                        {loading ? 'Logging in...' : 'Login'}
                    </Button>

                    {/* Reset Password Button */}
                    <Button
                        variant="text"
                        color="secondary"
                        fullWidth
                        onClick={() => setResetPasswordDialog(true)}
                        sx={{ mt: 2 }}
                    >
                        Forgot Password?
                    </Button>

                    {/* Sign Up Button */}
                    <Button
                        variant="outlined"
                        color="primary"
                        fullWidth
                        onClick={() => navigate('/signup')}  // Navigate to signup page
                        sx={{ mt: 2 }}
                    >
                        Sign Up
                    </Button>
                </form>
            </Box>

            {/* Reset Password Dialog */}
            <Dialog open={resetPasswordDialog} onClose={() => setResetPasswordDialog(false)}>
                <DialogTitle>Reset Password</DialogTitle>
                <DialogContent>
                    <TextField
                        label="Enter your email"
                        type="email"
                        fullWidth
                        value={resetEmail}
                        onChange={(e) => setResetEmail(e.target.value)}
                        margin="normal"
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setResetPasswordDialog(false)} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={handleResetPassword} color="primary">
                        Send Reset Link
                    </Button>
                </DialogActions>
            </Dialog>

            {/* Display success message if password reset email is sent */}
            {resetSuccess && <Alert severity="success">Password reset email sent successfully!</Alert>}
            {resetSuccess === false && <Alert severity="error">Failed to send reset email!</Alert>}
        </Container>
    );
};

export default LoginPage;
