<script setup>
import { reactive } from 'vue';
import apiClient from '@/api/apiClient';

const props = defineProps({
  block: {
    type: Object,
    required: true,
  }
});

const editedBlock = reactive({ ...props.block });

const emits = defineEmits(['upload-image', 'delete-block']);

const deleteBlockEvent = () => {
  emits('delete-block', editedBlock)
};

const uploadFileEvent = (file) => {
  const formData = new FormData();
  formData.append('image', file);
  emits('upload-image', editedBlock, formData)
};

</script>

<template>
  <div class="block">
    <button 
      @click="deleteBlockEvent" 
      class="block__close-button"
    >
      <img src="@/assets/icons/close.svg">
    </button>
    <div class="block__header">
      <img src="@/assets/icons/blocks/img-purple.svg">
      <p class="block__type">Изображение</p>
    </div>
    <p class="block__hint">
      Поддерживаются форматы png, jpg, jpeg
    </p>
    <img 
      v-if="editedBlock.image_path" 
      :src="`${apiClient.defaults.baseURL }/media/${editedBlock.image_path}`"
      class="block__image"
    >

    <AppFileInput 
      size="small" 
      importance="secondary"
      @upload-file="uploadFileEvent"
    >
      Загрузить изображение
    </AppFileInput>
  </div>
</template>

<style scoped>
.block {
  width: 342px;
}

.block__image {
  width: 342px;
  object-fit: cover;
  margin-bottom: 12px;
}
</style>