import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL + '/api/vidasan';

// Get token from localStorage
const getToken = () => {
    return localStorage.getItem('token');
};

// Kaplama API actions
export const listKaplama = () => {
    return axios.get(`${API_URL}/kaplama/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const createKaplama = (kaplamaData) => {
    return axios.post(`${API_URL}/kaplama/`, kaplamaData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const getKaplama = (id) => {
    return axios.get(`${API_URL}/kaplama/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const updateKaplama = (id, kaplamaData) => {
    return axios.put(`${API_URL}/kaplama/${id}/`, kaplamaData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const deleteKaplama = (id) => {
    return axios.delete(`${API_URL}/kaplama/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

// Patch API actions
export const listPatch = () => {
    return axios.get(`${API_URL}/patch/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const createPatch = (patchData) => {
    return axios.post(`${API_URL}/patch/`, patchData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const getPatch = (id) => {
    return axios.get(`${API_URL}/patch/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const updatePatch = (id, patchData) => {
    return axios.put(`${API_URL}/patch/${id}/`, patchData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const deletePatch = (id) => {
    return axios.delete(`${API_URL}/patch/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

// Isil Islem API actions
export const listIsilIslem = () => {
    return axios.get(`${API_URL}/isil-islem/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const createIsilIslem = (isilIslemData) => {
    return axios.post(`${API_URL}/isil-islem/`, isilIslemData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const getIsilIslem = (id) => {
    return axios.get(`${API_URL}/isil-islem/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const updateIsilIslem = (id, isilIslemData) => {
    return axios.put(`${API_URL}/isil-islem/${id}/`, isilIslemData, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};

export const deleteIsilIslem = (id) => {
    return axios.delete(`${API_URL}/isil-islem/${id}/`, {
        headers: {
            'Authorization': `Token ${getToken()}`
        }
    });
};
