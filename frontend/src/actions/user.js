// actions/user.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL + '/api/auth'; // Adjust the base URL as needed

// Get token from localStorage
const getToken = () => localStorage.getItem('token');

// API actions for User
export const listUsers = () => {
    return axios.get(`${API_URL}/users/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const createUser = (userData) => {
    return axios.post(`${API_URL}/users/`, userData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const getUser = (id) => {
    return axios.get(`${API_URL}/users/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const updateUser = (id, userData) => {
    return axios.put(`${API_URL}/users/${id}/`, userData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const deleteUser = (id) => {
    return axios.delete(`${API_URL}/users/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};
