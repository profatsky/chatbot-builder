import { ref } from 'vue';
import apiClient from '@/api/apiClient';

export async function createDialogue(projectID, triggerEventType, triggerValue) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.post(`/projects/${projectID}/dialogues`, {
    project_id: projectID,
    trigger: {
      event_type: triggerEventType,
      value: triggerValue,
    }
  })
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
};

export async function updateDialogueTrigger(
  projectID, 
  dialogueID, 
  triggerEventType, 
  triggerValue
) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.put(`/projects/${projectID}/dialogues/${dialogueID}`, {
    project_id: projectID, 
    dialogue_id: dialogueID, 
    event_type: triggerEventType, 
    value: triggerValue,
  })
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
}

export async function deleteDialogue(projectID, dialogueID) {
  const response = ref(null);
  const error = ref(null);
  
  await apiClient.delete(`/projects/${projectID}/dialogues/${dialogueID}`)
  .then(res => response.value = res)
  .catch(err => error.value = err);

  return { response, error };
};