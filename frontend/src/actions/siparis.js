// actions/siparis.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL + '/api/vidasan';

// Get token from localStorage
const getToken = () => localStorage.getItem('token');

// API actions for Siparis
export const listSiparis = () => {
    return axios.get(`${API_URL}/siparis/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const createSiparis = (siparisData) => {
    return axios.post(`${API_URL}/siparis/`, siparisData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const getSiparis = (id) => {
    return axios.get(`${API_URL}/siparis/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const updateSiparis = (id, siparisData) => {
    return axios.put(`${API_URL}/siparis/${id}/`, siparisData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const deleteSiparis = (id) => {
    return axios.delete(`${API_URL}/siparis/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};


// API actions for SiparisFile
export const listSiparisFiles = (siparisId) => {
    return axios.get(`${API_URL}/siparis/${siparisId}/siparis-file/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const createSiparisFile = (siparisId, fileData) => {
    return axios.post(`${API_URL}/siparis/${siparisId}/siparis-file/`, fileData, {
        headers: {
            'Authorization': `Token ${getToken()}`,
            'Content-Type': 'multipart/form-data'
        }
    });
};

export const deleteSiparisFile = (siparisId, id) => {
    return axios.delete(`${API_URL}/siparis/${siparisId}/siparis-file/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const getNextStep = (id) => {
    return axios.get(`${API_URL}/siparis/${id}/next-step/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const goNextStep = (id) => {
    return axios.get(`${API_URL}/siparis/${id}/go-next-step/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const downloadWorkOrderExcel = (siparisId) => {
    return axios.get(`${API_URL}/work-order/${siparisId}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`,
        },
        responseType: 'blob' // Set responseType to 'blob' to handle binary data
    }).then(response => {
        // Create a link element to download the Excel file
        const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'work_order.xlsx'); // Set default file name
        document.body.appendChild(link);
        link.click();
        link.remove(); // Clean up
        window.URL.revokeObjectURL(url); // Release the object URL
    }).catch(error => {
        console.error('Error downloading work order Excel:', error);
    });
};

// Get SiparisActivity by Siparis ID
export const getSiparisActivity = (siparisId) => {
    return axios.get(`${API_URL}/siparis/${siparisId}/activity/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

// Update SiparisActivity by Siparis ID
export const updateSiparisActivity = (siparisId, activityData) => {
    return axios.put(`${API_URL}/siparis/${siparisId}/activity/`, activityData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};