import { ref } from 'vue';
import apiClient from '@/api/apiClient';

export async function createProject(name, startMessage, startKeyboardType) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.post('/projects', {
    name: name,
    start_message: startMessage,
    start_keyboard_type: startKeyboardType,
  })
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}

export async function getUserProjects() {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.get('/projects')
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}

export async function updateProject(
  projectId, name, startMessage, startKeyboardType
) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.put(`/projects/${projectId}`, {
    name: name,
    start_message: startMessage,
    start_keyboard_type: startKeyboardType,
  })
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}

export async function deleteProject(projectId) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.delete(`/projects/${projectId}`)
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}

export async function removePluginFromProject(projectId, pluginId) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.delete(`/projects/${projectId}/plugins/${pluginId}`)
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}

export async function getCode(projectId) {
  const response = ref(null);
  const error = ref(null);

  await apiClient.get(`/projects/${projectId}/code`, {
    responseType: 'blob'
  })
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}