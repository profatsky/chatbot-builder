import { ref } from 'vue';
import apiClient from '@/api/apiClient';

export async function deleteDialogue(projectID, dialogueID) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.delete(`/projects/${projectID}/dialogues/${dialogueID}`)
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}