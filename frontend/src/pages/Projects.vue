<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toast-notification';
import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import ProjectList from '@/components/Project/ProjectList.vue';
import { createProject, getUserProjects, updateProject, deleteProject, getCode } from '@/api/projects';

const toast = useToast();
const projects = ref([]);
const isProjectsLoading = ref(true);

const handleUpdateProjectEvent = async (editedProject) => {
  const { response, error } = await updateProject(
    editedProject.project_id,
    editedProject.name,
    editedProject.start_message,
    editedProject.start_keyboard_type
  );
  if (error.value) {
    toast.error('Что-то пошло не так...');
  } else {
    const index = projects.value.findIndex(
      project => project.project_id === editedProject.project_id
    );
    if (index !== -1) {
      projects.value[index] = editedProject;
    }
  }
};

const handleDeleteProjectEvent = async (projectId) => {
  const { response, error } = await deleteProject(projectId);
  if (error.value) {
    toast.error('Что-то пошло не так...');
  } else {
    projects.value = projects.value.filter(p => p.project_id !== projectId);
    toast.success('Чат-бот успешно удален');
  }
};

const handleCreateProjectEvent = async () => {
  if (projects.value.length >= 5) {
    toast.error('У вас максимальное количество чат-ботов!');
    return;
  };

  const project = {
    name: 'Новый чат-бот',
    start_message: '',
    start_keyboard_type: 'reply_keyboard',
  };

  const { response, error } = await createProject(
    project.name, 
    project.start_message, 
    project.start_keyboard_type
  );

  if (error.value) {
    toast.error('Что-то пошло не так...');
  } else {
    const responseData = response.value.data;
    projects.value.push(responseData);
    toast.success('Новый чат-бот успешно создан');
  }
};

const handleDownloadCodeEvent = async (projectId) => {
  const { response, error } = await getCode(projectId);

  if (error.value) {
    toast.error('Что-то пошло не так...');
  } else {
    const url = window.URL.createObjectURL(new Blob([response.value.data]));
    const link = document.createElement('a');

    link.href = url;
    link.setAttribute('download', 'bot.zip');
    document.body.appendChild(link);
    link.click();
  }
};

onMounted(async () => {
  const { response, error } = await getUserProjects();
  if (error.value) {
    toast.error('Что-то пошло не так...')
  } else {
    isProjectsLoading.value = false;
    const responseData = response.value.data;
    projects.value = responseData;
  }
});
</script>

<template>
  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="page__content">
        <div class="page__header">
          <h1 class="header__title">Чат-боты</h1>
          <AppButton
            size="medium" 
            importance="secondary"
            @click="handleCreateProjectEvent"
          >
            Создать чат-бота
          </AppButton>
        </div>
        <div class="page__hint">
          Чат-боты для Telegram - это автоматизированные собеседники, которые выполняют различные задачи: отвечают на вопросы, продают товары, предоставляют информацию и т.д.
        </div>
        <ProjectList
          v-if="!isProjectsLoading"
          :projects="projects"
          @update-project="handleUpdateProjectEvent"
          @delete-project="handleDeleteProjectEvent"
          @download-code="handleDownloadCodeEvent"
        />
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

.page__hint {
  font-size: 16px;
  font-weight: 500;
  line-height: 28px;
  letter-spacing: 0.75px;
  color: var(--body-text);
  margin-bottom: 28px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .page__header {
    margin: 28px 0px 20px 0px;
  }

  .header__title {
    font-size: 24px;
    line-height: 28px;
  }

  .page__hint {
    font-size: 14px;
    line-height: 18px;
    margin-bottom: 20px;
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

  .page__hint {
    font-size: 8px;
    line-height: 10px;
    letter-spacing: 0px;
    margin-bottom: 12px;
    width: 100%;
  }
}
</style>