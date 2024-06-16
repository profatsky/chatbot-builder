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
            size="medium"
            importance="secondary"
            @click="handleCreateDialogueFromTemplateEvent"
          >
            Добавить
          </AppButton>
        </div>
        <p class="dialogue-template__description" v-html="dialogueTemplate.description"></p>
      </div>
    </div>
  </main>
</template>

<style scoped>
.page__header {
  margin: 32px 0px 20px 0px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header__title {
  font-size: 32px;
  line-height: 40px;
}

:deep() p {
  font-size: 16px;
  line-height: 24px;
  color: var(--body-text);
  margin-bottom: 12px;
}

:deep() li {
  font-size: 16px;
  line-height: 24px;
  color: var(--body-text);
  margin: 0px 0px 8px 20px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .page__header {
    margin: 28px 0px 20px 0px;
  }

  .header__title {
    font-size: 24px;
    line-height: 28px;
  }

  :deep() p {
    font-size: 12px;
    line-height: 20px;
    margin-bottom: 8px;
  }

  :deep() li {
    font-size: 12px;
    line-height: 20px;
    margin: 0px 0px 6px 16px;
  }
}

@media (max-width: 767px) {
  .page__header {
    margin: 18px 0px 12px 0px;
  }

  .header__title {
    font-size: 16px;
    line-height: 20px;
  }

  :deep() p {
    font-size: 12px;
    line-height: 16px;
    color: var(--body-text);
    margin-bottom: 8px;
  }

  :deep() li {
    font-size: 12px;
    line-height: 16px;
    margin: 0px 0px 6px 16px;
  }
}
</style>