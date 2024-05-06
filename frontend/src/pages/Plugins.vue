<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toast-notification';

import { getPlugins, addPluginToProject } from '@/api/plugins';
import { getUserProjects } from '@/api/projects';

import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import AddPluginForm from '@/components/Plugin/AddPluginForm.vue';
import PluginList from '@/components/Plugin/PluginList.vue';

const toast = useToast();
const plugins = ref([]);
const isPluginsLoading = ref(true);
const projects = ref([]);
const chosenPlugin = ref({});

onMounted(async () => {
  const { response, error } = await getPlugins();
  if (error.value) {
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    isPluginsLoading.value = false;
    const responseData = response.value.data;
    plugins.value = responseData;
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

const handleAddPluginEvent = async (plugin) => {
  const { response, error } = await getUserProjects();
  if (error.value) {
    toast.error('Что-то пошло не так...')
  } else {
    const responseData = response.value.data;
    const filteredProjects = responseData.filter(proj => {
      return !proj.plugins.some(plug => plug.plugin_id === plugin.plugin_id);
    });
    projects.value = filteredProjects;
    chosenPlugin.value = plugin;
  }
  openProjectsListForm()
};

const handleChooseProjectEvent = async (project) => {
  const { response, error } = await addPluginToProject(project.project_id, chosenPlugin.value.plugin_id);
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
    <AddPluginForm
      :projects="projects"
      @choose-project="handleChooseProjectEvent"
    />
  </AppModal>

  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="page__content">
        <div class="page__header">
          <h1 class="header__title">Плагины</h1>
        </div>
        <p class="page__hint">
          Плагины - это готовые программные модули, которые легко интегрируются в чат-ботов. Плагины добавляют новый функционал, который невозможно создать с нуля без навыков программирования.
        </p>
        <PluginList
          v-if="!isPluginsLoading"
          :plugins="plugins"
          @add-plugin="handleAddPluginEvent"
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