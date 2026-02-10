import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:8000/api' });

export const uploadFile = (formData) => API.post('/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
});

export const getSummary = () => API.get('/summary/');
export const getHistory = () => API.get('/history/');
