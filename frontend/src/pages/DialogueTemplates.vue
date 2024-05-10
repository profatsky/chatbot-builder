<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toast-notification';

import { getDialogueTemplates, createDialogueFromTemplate } from '@/api/dialogueTemplates.js'
import { getUserProjects } from '@/api/projects.js';

import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import createDialogueFromTemplateForm from '@/components/DialogueTemplate/createDialogueFromTemplateForm.vue';
import DialogueTemplateList from '@/components/DialogueTemplate/DialogueTemplateList.vue';

const toast = useToast();
const dialogueTemplates = ref([]);
const isDialogueTemplatesLoading = ref(true);
const projects = ref([]);
const chosenDialogueTemplate = ref({});

onMounted(async () => {
  const { response, error } = await getDialogueTemplates();
  if (error.value) {
    toast.error('Что-то пошло не так...');
  } else {
    isDialogueTemplatesLoading.value = false;
    dialogueTemplates.value = response.value.data;
  }
});

const showProjectsListModal = ref(false);
const openProjectsListForm = () => {
  showProjectsListModal.value = true;
};
const closeProjectsListModal = () => {
  showProjectsListModal.value = false;
};

const handleCreateDialogueFromTemplateEvent = async (dialogueTemplate) => {
  const { response, error } = await getUserProjects();
  if (error.value) {
    toast.error('Что-то пошло не так...');
  } else {
    const responseData = response.value.data;
    if (responseData.length === 0) {
      toast.error('Вы еще не создали ни одного чат-бота!')
    } else {
      projects.value = responseData;
      chosenDialogueTemplate.value = dialogueTemplate;
      openProjectsListForm();
    }
  }
};

const handleChooseProjectEvent = async (project) => {
  const { response, error } = await createDialogueFromTemplate(project.project_id, chosenDialogueTemplate.value.template_id);
  if (error.value) {
    toast.error('Что-то пошло не так...')
  } else {
    toast.success('Диалог создан с помощью шаблона');
  }
  closeProjectsListModal();
};
</script>

<template>
  <AppModal
    v-if="showProjectsListModal"
    @close-modal="closeProjectsListModal"
  >
    <createDialogueFromTemplateForm
      :projects="projects"
      @choose-project="handleChooseProjectEvent"
    />
  </AppModal>

  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="page__content">
        <div class="page__header">
          <h1 class="header__title">Шаблоны диалогов</h1>
        </div>
        <p class="page__hint">
          Шаблоны помогают быстро добавить в чат-бота заготовленный диалог, решающий определенную задачу. При необходимости вы  можете изменить содержимое созданного из шаблона диалога под свои нужды.
        </p>
        <DialogueTemplateList
          v-if="!isDialogueTemplatesLoading"
          :dialogue-templates="dialogueTemplates"
          @create-dialogue="handleCreateDialogueFromTemplateEvent"
        />
      </div>
    </div>
  </main>
</template>

<style scoped>
.page__content {
  margin-left: 120px;
}

.page__header {
  margin: 48px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page__hint {
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.75px;
  color: var(--body-text);
  margin-bottom: 28px;
}
</style>