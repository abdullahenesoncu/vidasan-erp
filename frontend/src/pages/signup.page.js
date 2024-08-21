import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signupUser } from '../actions/authentication';
import { TextField, Button, Container, Typography, Box, Alert } from '@mui/material';

const SignupPage = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        name: '',
        password: '',
        confirmPassword: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    // Handle input changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    // Handle form submission
    const handleSubmit = (e) => {
        e.preventDefault();

        // Validate password match
        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        setLoading(true);
        setError(null);

        const signupData = {
            name: formData.name,
            email: formData.email,
            password: formData.password,
        };

        // Call the signup action
        signupUser(signupData)
            .then((response) => {
                setSuccess(true);
                setLoading(false);
                setError(null);
                navigate('/login');  // Redirect to login page after successful signup
            })
            .catch((error) => {
                setLoading(false);
                setError(error.response ? error.response.data.detail : 'Something went wrong');
            });
    };

    return (
        <Container maxWidth="sm">
            <Box sx={{ mt: 5 }}>
                <Typography variant="h4" gutterBottom>
                    Sign Up
                </Typography>

                {error && <Alert severity="error">{error}</Alert>}
                {success && <Alert severity="success">Signup successful!</Alert>}

                <form onSubmit={handleSubmit}>
                    <TextField
                        label="Name/Surname"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        fullWidth
                        margin="normal"
                        required
                        type="text"
                    />
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
                    <TextField
                        label="Confirm Password"
                        name="confirmPassword"
                        value={formData.confirmPassword}
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
                        {loading ? 'Signing up...' : 'Sign Up'}
                    </Button>
                </form>
            </Box>
        </Container>
    );
};

export default SignupPage;
