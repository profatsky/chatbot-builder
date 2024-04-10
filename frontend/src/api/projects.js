import { ref } from 'vue';
import apiClient from '@/api/apiClient';

export async function getUserProjects() {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.get('/projects')
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}