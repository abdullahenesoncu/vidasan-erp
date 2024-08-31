// actions/machine.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL + '/api/vidasan'; // Adjust the base URL as needed

// Get token from localStorage
const getToken = () => localStorage.getItem('token');

// API actions for Machine
export const listMachines = () => {
    return axios.get(`${API_URL}/machines/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const createMachine = (machineData) => {
    return axios.post(`${API_URL}/machines/`, machineData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const getMachine = (id) => {
    return axios.get(`${API_URL}/machines/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const updateMachine = (id, machineData) => {
    return axios.put(`${API_URL}/machines/${id}/`, machineData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const deleteMachine = (id) => {
    return axios.delete(`${API_URL}/machines/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const fetchMachineLogs = (machineId = null) => {
    const url = machineId ? `${API_URL}/machine-logs/${machineId}/` : `${API_URL}/machine-logs/`;
    return axios.get(url, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};