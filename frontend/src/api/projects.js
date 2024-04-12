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

export async function updateProject(
  project_id, name, start_message, start_keyboard_type
) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.put(`/projects/${project_id}`, {
    name: name,
    start_message: start_message,
    start_keyboard_type: start_keyboard_type,
  })
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}
