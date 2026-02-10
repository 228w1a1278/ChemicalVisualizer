import axios from 'axios';

const API_URL = 'https://chemicalvisualizer-4c97.onrender.com/api';

const API = axios.create({ baseURL: API_URL});

export const uploadFile = (formData) => API.post('/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
});

export const getSummary = () => API.get('/summary/');
export const getHistory = () => API.get('/history/');
