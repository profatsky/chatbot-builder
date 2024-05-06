<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toast-notification';
import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import PluginList from '@/components/Plugin/PluginList.vue';
import { getPlugins } from '@/api/plugins';

const toast = useToast();

const plugins = ref([]);

const isPluginsLoading = ref(true);

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
</script>

<template>
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