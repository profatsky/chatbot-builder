<script setup>
import { computed } from 'vue';
import apiClient from '@/api/apiClient';

const props = defineProps({
  dialogueTemplate: {
    type: Object,
    required: true,
  }
});

const emits = defineEmits(['create-dialogue']);
const createDialogueEvent = () => {
  emits('create-dialogue', props.dialogueTemplate)
};

const summary = computed(() => {
  if (props.dialogueTemplate.summary.length > 58) {
    return props.dialogueTemplate.summary.substring(0, 55) + '...';
  }
  return props.dialogueTemplate.summary;
});
</script>

<template>
  <div class="dialogue-template">
    <div class="dialogue-template__img">
      <img :src="`${apiClient.defaults.baseURL}/media/${dialogueTemplate.image_path}`">
    </div>
    <div class="dialogue-template__name">{{ dialogueTemplate.name }}</div>
    <div class="dialogue-template__summary">{{ summary }}</div>
    <div class="dialogue-template__buttons">
      <AppButton 
        size="small" 
        importance="primary"
        @click="createDialogueEvent"
      >
        Создать диалог
      </AppButton>
      <AppButton 
        size="small" 
        importance="secondary"
        @click="$router.push(`/templates/${dialogueTemplate.template_id}`)"
      >
        Подробнее
      </AppButton>
    </div>
  </div>
</template>

<style scoped>
.dialogue-template {
  background-color: var(--light-gray);
  padding: 28px 32px;
  border-radius: 16px;
  margin-bottom: 10px;
  box-shadow: 0 0 16px 0 rgba(17, 17, 17, 0.04);
}

.dialogue-template__img img {
  height: 200px;
}

.dialogue-template__img {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.dialogue-template__name {
  font-size: 20px;
  font-weight: 500;
  letter-spacing: 1px;
  margin-bottom: 12px;
}

.dialogue-template__summary {
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 1px;
  color: var(--body-text);
  margin-bottom: 24px;
}

.dialogue-template__buttons {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (max-width: 768px) {
  .dialogue-template {
    padding: 20px 24px;
  }

  .dialogue-template__img img {
    height: 160px;
  }

  .dialogue-template__name {
    font-size: 18px;
    margin-bottom: 10px;
  }

  .dialogue-template__summary {
    font-size: 14px;
    margin-bottom: 18px;
  }

  .dialogue-template__buttons {
    gap: 12px;
  }
}
</style>