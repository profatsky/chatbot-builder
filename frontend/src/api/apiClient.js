import axios from 'axios';

axios.defaults.withCredentials = true

async function refreshTokens() {
  await apiClient.post('/refresh')
};

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

apiClient.interceptors.response.use(
  response => {
    return response;
  },
  async error => {
    const originalRequest = error.config;

    if (error.response.status === 422 && 
      error.response.data.detail === "Signature has expired") {
      await refreshTokens();
      return axios(originalRequest);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;