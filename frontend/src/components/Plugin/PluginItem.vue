<script setup>
import { computed } from 'vue';
import apiClient from '@/api/apiClient';

const props = defineProps({
  plugin: {
    type: Object,
    required: true
  }
});

const emits = defineEmits(['add-plugin']);
const addPluginEvent = () => {
  emits('add-plugin', props.plugin)
};

const summary = computed(() => {
  if (props.plugin.summary.length > 58) {
    return props.plugin.summary.substring(0, 55) + '...';
  }
  return props.plugin.summary;
});
</script>

<template>
  <div class="plugin">
    <div class="plugin__img">
      <img :src="`${apiClient.defaults.baseURL}/media/${plugin.image_path}`">
    </div>
    <div class="plugin__name">{{ plugin.name }}</div>
    <div class="plugin__summary">{{ summary }}</div>
    <div class="plugin__buttons">
      <AppButton 
        size="small" 
        importance="primary"
        @click="addPluginEvent"
      >
        Добавить
      </AppButton>
      <AppButton 
        size="small" 
        importance="secondary"
        @click="$router.push(`/plugins/${plugin.plugin_id}`)"
      >
        Подробнее
      </AppButton>
    </div>
  </div>
</template>

<style scoped>
.plugin {
  background-color: var(--light-gray);
  padding: 28px 32px;
  border-radius: 16px;
  margin-bottom: 10px;
  box-shadow: 0 0 16px 0 rgba(17, 17, 17, 0.04);
}

.plugin__img img {
  height: 200px;
}

.plugin__img {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.plugin__name {
  font-size: 20px;
  font-weight: 500;
  letter-spacing: 1px;
  margin-bottom: 12px;
}

.plugin__summary {
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 1px;
  color: var(--body-text);
  margin-bottom: 24px;
}

.plugin__buttons {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .plugin {
    padding: 20px 24px;
    margin-bottom: 4px;
  }

  .plugin__img img {
    height: 160px;
  }

  .plugin__name {
    font-size: 18px;
    margin-bottom: 10px;
  }

  .plugin__summary {
    font-size: 14px;
    margin-bottom: 18px;
  }

  .plugin__buttons {
    gap: 12px;
  }
}

@media (max-width: 767px) {
  .plugin {
    width: 160px;
    padding: 12px 18px;
    margin: 0;
    border-radius: 12px;
  }

  .plugin__img {
    margin-bottom: 12px;
  }

  .plugin__img img {
    height: 100px;
  }

  .plugin__name {
    font-size: 12px;
    margin-bottom: 8px;
  }

  .plugin__summary {
    font-size: 8px;
    margin-bottom: 8px;
  }

  .plugin__buttons {
    width: 160px;
    gap: 6px;
  }
}
</style>