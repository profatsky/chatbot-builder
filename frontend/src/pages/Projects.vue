<script setup>
import { ref, onMounted } from 'vue';
import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import ProjectList from '@/components/Projects/ProjectList.vue';
import { getUserProjects } from '@/api/projects';
import {useToast} from 'vue-toast-notification';
import { updateProject } from '@/api/projects';

const toast = useToast();

const projects = ref([])

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
    }

    toast.success('Данные о чат-боте обновлены');
  }
}

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
        <h1 class="content__title">Чат-боты</h1>
        <ProjectList
          :projects="projects"
          v-if="!isProjectsLoading"
          @update-project="handleUpdateProjectEvent"
        />
      </div>
    </div>
  </main>
</template>

<style scoped>
.page-content {
  margin-left: 120px;
}

.content__title {
  margin: 48px 0;
}
</style>