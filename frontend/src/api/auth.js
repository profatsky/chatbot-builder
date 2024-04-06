import { ref } from 'vue';
import apiClient from '@/api/apiClient';

export async function registerUser(email, password) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.post('/register', {
    email: email, 
    password: password
  })
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}

export async function loginUser(email, password) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.post('/login', {
    email: email, 
    password: password
  })
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}