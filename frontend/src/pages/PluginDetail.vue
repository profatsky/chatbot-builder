<script setup>
import { ref, onBeforeMount, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toast-notification';

import { getPlugin, addPluginToProject } from '@/api/plugins';
import { getUserProjects } from '@/api/projects';
import apiClient from '@/api/apiClient';

import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import ProjectRowForm from '@/components/Project/ProjectRow/ProjectRowForm.vue';

const toast = useToast();
const route = useRoute();
const router = useRouter();
const plugin = ref({});
const projects = ref([]);

onBeforeMount(async () => {
  const { response, error } = await getPlugin(route.params.pluginId);
  if (error.value) {
    router.push('/plugins');
  } else {
    const responseData = response.value.data;
    plugin.value = responseData;
  }
});

onMounted(async () => {
  const { response, error } = await getUserProjects();
  if (error.value) {
    toast.error('Что-то пошло не так...')
  } else {
    const responseData = response.value.data;
    const filteredProjects = responseData.filter(proj => {
      return !proj.plugins.some(plug => plug.plugin_id === plugin.value.plugin_id);
    });
    projects.value = filteredProjects;
  }
});

const showProjectsListModal = ref(false);
const openProjectsListForm = () => {
  if (projects.value.length > 0) {
    showProjectsListModal.value = true;
  } else {
    toast.error('Этот плагин добавлен во все ваши проекты!')
  }
};
const closeProjectsListModal = () => {
  showProjectsListModal.value = false;
};

const handleChooseProjectEvent = async (project) => {
  const { response, error } = await addPluginToProject(project.project_id, plugin.value.plugin_id);
  if (error.value) {
    toast.error('Что-то пошло не так...')
  } else {
    projects.value = projects.value.filter(p => p.project_id !== project.project_id);
    toast.success('Плагин добавлен в проект');
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
      Добавить плагин в проект
    </ProjectRowForm>
  </AppModal>

  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="page__content">
        <div class="page__header">
          <h1 class="header__title">Плагин «{{ plugin.name }}»</h1>
          <AppButton
            size="large"
            importance="secondary"
            @click="openProjectsListForm"
          >
            Добавить в проект
          </AppButton>
        </div>
        <div class="plugin">
          <p class="plugin__description">
            {{ plugin.description }}
          </p>
          <div class="plugin__img">
            <img :src="`${apiClient.defaults.baseURL}/media/${plugin.image_path}`">
          </div>
        </div>
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

.plugin {
  display: flex;
  justify-content: space-between;
  gap: 64px;
}

.plugin__description {
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.75px;
  color: var(--body-text);
}

.plugin__img img {
  height: 200px;
}

.plugin__img {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}
</style>