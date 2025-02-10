import axios from 'axios';
import router from '@/router/router.js';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  response => {
    return response;
  },
  async error => {
    const originalRequest = error.config;
    if (error.response) {
      if (error.response.status === 401) {
        localStorage.removeItem('access_token');
        router.push('/');
      } else if (error.response.status === 404) {
        router.push('/not-found');
      } else if (error.response.status === 422 && 
        error.response.data.detail === "Signature has expired") {
        localStorage.removeItem('access_token');
        router.push('/');
      }
    } else {
      router.push('/');
    }
    return Promise.reject(error);
  }
);

export default apiClient;