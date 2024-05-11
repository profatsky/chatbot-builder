<script setup>
import { ref, onBeforeMount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toast-notification';

import { getDialogueTemplate, createDialogueFromTemplate } from '@/api/dialogueTemplates';
import { getUserProjects } from '@/api/projects';
import apiClient from '@/api/apiClient';

import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import ProjectRowForm from '@/components/Project/ProjectRow/ProjectRowForm.vue'

const toast = useToast();
const route = useRoute();
const router = useRouter();
const dialogueTemplate = ref({});
const projects = ref([]);

onBeforeMount(async () => {
  const { response, error } = await getDialogueTemplate(route.params.templateId);
  if (error.value) {
    router.push('/templates');
  } else {
    const responseData = response.value.data;
    dialogueTemplate.value = responseData;
  }
});

const showProjectsListModal = ref(false);
const openProjectsListForm = () => {
  showProjectsListModal.value = true;
};
const closeProjectsListModal = () => {
  showProjectsListModal.value = false;
};

const handleCreateDialogueFromTemplateEvent = async () => {
  const { response, error } = await getUserProjects();
  if (error.value) {
    toast.error('Что-то пошло не так...');
  } else {
    const responseData = response.value.data;
    if (responseData.length === 0) {
      toast.error('Вы еще не создали ни одного чат-бота!')
    } else {
      projects.value = responseData;
      openProjectsListForm();
    }
  }
};

const handleChooseProjectEvent = async (project) => {
  const { response, error } = await createDialogueFromTemplate(project.project_id, dialogueTemplate.value.template_id);
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
    @closeModal="closeProjectsListModal"
  >
    <ProjectRowForm
      :projects="projects"
      @choose-project="handleChooseProjectEvent"
    >
      Добавить диалог в проект
    </ProjectRowForm>
  </AppModal>

  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="page__content">
        <div class="page__header">
          <h1 class="header__title">Шаблон «{{ dialogueTemplate.name }}»</h1>
          <AppButton
            size="large"
            importance="secondary"
            @click="handleCreateDialogueFromTemplateEvent"
          >
            Создать диалог
          </AppButton>
        </div>
        <div class="dialogue-template">
          <p class="dialogue-template__description">
            {{ dialogueTemplate.description }}
          </p>
          <div class="dialogue-template__img">
            <img :src="`${apiClient.defaults.baseURL}/media/${dialogueTemplate.image_path}`">
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.page__header {
  margin: 48px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialogue-template {
  display: flex;
  justify-content: space-between;
  gap: 64px;
}

.dialogue-template__description {
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.75px;
  color: var(--body-text);
}

.dialogue-template__img img {
  height: 200px;
}

.dialogue-template__img {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}
</style>