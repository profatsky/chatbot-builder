import { ref } from 'vue';
import apiClient from '@/api/apiClient';

export async function getUserProfile() {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.get('/users/me')
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}