import axios from 'axios';
import { refreshTokens } from '@/api/auth.js';
import router from '@/router/router.js';

axios.defaults.withCredentials = true;

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

apiClient.interceptors.response.use(
  response => {
    return response;
  },
  async error => {
    const originalRequest = error.config;

    if (error.response) {
      if (error.response.status === 401) {
        router.push('/');
      } else if (error.response.status === 404) {
        router.push('/not-found')
      } else if (error.response.status === 422 && 
        error.response.data.detail === "Signature has expired") {
        await refreshTokens();
        return axios(originalRequest);
      }
    } else {
      router.push('/');
    }

    return Promise.reject(error);
  }
);

export default apiClient;