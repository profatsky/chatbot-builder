import { ref } from 'vue';
import apiClient from '@/api/apiClient';

export async function createBlock(projectId, dialogueId, block) {
  const response = ref(null);
  const error = ref(null);

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

export async function updateBlock(projectId, dialogueId, block) {
  const response = ref(null);
  const error = ref(null);

  await apiClient.put(`/projects/${projectId}/dialogues/${dialogueId}/blocks/${block.block_id}`, block)
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
};

export async function deleteBlock(projectId, dialogueId, blockId) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.delete(`/projects/${projectId}/dialogues/${dialogueId}/blocks/${blockId}`)
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
};

export async function uploadImage(projectId, dialogueId, blockId, formData) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.post(
    `/projects/${projectId}/dialogues/${dialogueId}/blocks/${blockId}/upload-image`, 
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    },
  )
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}