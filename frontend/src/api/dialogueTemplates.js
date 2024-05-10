import { ref } from 'vue';
import apiClient from '@/api/apiClient';

export async function getDialogueTemplates() {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.get('/templates')
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}

export async function getDialogueTemplate(templateId) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.get(`/templates/${templateId}`)
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}

export async function createDialogueFromTemplate(projectId, templateId) {
  const response = ref(null);
  const error = ref(null);

  await apiClient.post(`/projects/${projectId}/templates`, { template_id: templateId })
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}