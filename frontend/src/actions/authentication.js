import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL + '/api/auth';

// Get token from localStorage
const getToken = () => localStorage.getItem('token');

// User Signup
export const signupUser = (signupData) => {
    return axios.post(`${API_URL}/signup/`, signupData);
};

// User Login
export const loginUser = (loginData) => {
    return axios.post(`${API_URL}/login/`, loginData);
};

// User Logout
export const logoutUser = () => {
    return axios.post(
        `${API_URL}/logout/`,
        {},
        {
            headers: {
                'Authorization': `Token ${getToken()}`
            }
        }
    );
};

// Change Password
export const changePassword = (passwordData) => {
    return axios.put(
        `${API_URL}/change-password/`,
        passwordData,
        {
            headers: {
                'Authorization': `Token ${getToken()}`
            }
        }
    );
};

// Reset Password Request
export const resetPasswordRequest = (email) => {
    return axios.get(`${API_URL}/reset-password-request/`, {
        params: { email }
    });
};

// Reset Password
export const resetPassword = (resetData) => {
    return axios.post(`${API_URL}/reset-password/`, resetData);
};


// Fetch Users
export const fetchUsers = () => {
    return axios.get(`${API_URL}/users/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

// Update User
export const updateUser = (userId, updatedData) => {
    return axios.patch(
        `${API_URL}/users/${userId}/`, 
        updatedData, 
        {
            headers: {
                'Authorization': `Token ${getToken()}`
            }
        }
    );
};