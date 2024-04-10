<script setup>
import { ref, onMounted } from 'vue';
import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import ProjectList from '@/components/Projects/ProjectList.vue';
import { getUserProjects } from '@/api/projects';
import {useToast} from 'vue-toast-notification';

const toast = useToast();

const projects = ref([])

const isProjectsLoading = ref(true);

function updateProject(updatedProject) {
  const index = projects.value.findIndex(
    project => project.project_id === updatedProject.project_id
  );
  if (index !== -1) {
    projects.value[index] = updatedProject;
  }
  console.log(projects)
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
          @update-project="updateProject"
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