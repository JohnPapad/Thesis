import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://localhost:8000/web_app/',            // to be changed
    headers: {'Content-Type': 'application/json'}
});

instance.interceptors.request.use(function (config) {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `JWT ${token}`;
    }
    return config;
});

export default instance;