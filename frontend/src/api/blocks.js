import { ref } from 'vue';
import apiClient from '@/api/apiClient';

export async function createBlock(projectId, dialogueId, block) {
  const response = ref(null);
  const error = ref(null);
  console.log(block);
  await apiClient.post(`/projects/${projectId}/dialogues/${dialogueId}/blocks`, block)
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
};

export async function getBlocks(projectId, dialogueId) {
  const response = ref(null);
  const error = ref(null);

  await apiClient.get(`/projects/${projectId}/dialogues/${dialogueId}/blocks`)
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
};
