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
  projectID, name, startMessage, startKeyboardType
) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.put(`/projects/${projectID}`, {
    name: name,
    start_message: startMessage,
    start_keyboard_type: startKeyboardType,
  })
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}

export async function deleteProject(projectID) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.delete(`/projects/${projectID}`)
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}

export async function removePluginFromProject(projectID, pluginID) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.delete(`/projects/${projectID}/plugins/${pluginID}`)
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}
