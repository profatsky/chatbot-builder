<script setup>
import { ref, onBeforeMount, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toast-notification';

import { getPlugin, addPluginToProject } from '@/api/plugins';
import { getUserProjects } from '@/api/projects';

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
            size="medium"
            importance="secondary"
            @click="openProjectsListForm"
          >
            Добавить
          </AppButton>
        </div>
        <p class="plugin__description" v-html="plugin.description"></p>
      </div>
    </div>
  </main>
</template>

<style scoped>
.page__header {
  margin: 32px 0px 28px 0px;
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

:deep() code {
  background-color: var(--light-gray);
}

@media (min-width: 768px) and (max-width: 1169px) {
  .page__header {
    margin: 28px 0px 24px 0px;
  }

  .header__title {
    font-size: 24px;
    line-height: 28px;
  }

  :deep() p {
    font-size: 14px;
    line-height: 18px;
    margin-bottom: 12px;
  }

  :deep() li {
    font-size: 14px;
    line-height: 18px;
    margin: 0px 0px 8px 16px;
  }
}

@media (max-width: 767px) {
  .page__header {
    margin: 18px 0px 14px 0px;
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