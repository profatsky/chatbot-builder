<script setup>
import { ref, toRefs, reactive, onMounted } from 'vue';
import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import ProjectList from '@/components/Projects/ProjectList.vue';
import { getUserProjects } from '@/api/projects';
import {useToast} from 'vue-toast-notification';
import { createProject, updateProject, deleteProject } from '@/api/projects';

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
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    const index = projects.value.findIndex(
      project => project.project_id === editedProject.project_id
    );
    if (index !== -1) {
      projects.value[index] = editedProject;
      toast.success('Данные о чат-боте обновлены');
    }
  }
};

const handleDeleteProjectEvent = async (projectID) => {
  const { response, error } = await deleteProject(projectID);
  if (error.value) {
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    projects.value = projects.value.filter(p => p.project_id !== projectID);
    toast.success('Чат-бот успешно удален');
  }
};

const handleCreateProjectEvent = async () => {
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
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    const responseData = response.value.data;
    projects.value.push(responseData);
    toast.success('Новый чат-бот успешно создан');
  }
};

onMounted(async () => {
  const { response, error } = await getUserProjects();
  if (error.value) {
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    isProjectsLoading.value = false;
    const responseData = response.value.data;
    projects.value = responseData;
    console.log(projects.value)
  }
});
</script>

<template>
  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="page-content">
        <div class="page-header">
          <h1 class="content__title">Чат-боты</h1>
          <AppButton
            size="large" 
            importance="secondary"
            @click="handleCreateProjectEvent"
          >
            Создать чат-бота
          </AppButton>
        </div>
        <ProjectList
          :projects="projects"
          v-if="!isProjectsLoading"
          @update-project="handleUpdateProjectEvent"
          @delete-project="handleDeleteProjectEvent"
        />
      </div>
    </div>
  </main>
</template>

<style scoped>
.page-content {
  margin-left: 120px;
}

.page-header {
  margin: 48px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

</style>