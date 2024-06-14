<script setup>
import { reactive } from 'vue';

const props = defineProps({
  block: {
    type: Object,
    required: true,
  }
});

const editedBlock = reactive({ ...props.block });

const emits = defineEmits(['update-text-in-block', 'delete-block']);

const updateBlockTextMessageEvent = () => {
  emits('update-text-in-block', editedBlock);
};

const deleteBlockEvent = () => {
  emits('delete-block', editedBlock);
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
      <img src="@/assets/icons/blocks/msg-purple.svg" class="block__img">
      <p class="block__type">Текст</p>
    </div>
    <p class="block__hint">
      Чтобы обратиться к пользователю чат-бота по имени в Telegram, указывайте в тексте: &ltusername&gt
    </p>
    <AppTextarea
      v-model="editedBlock.message_text"
      placeholder="Введите текст"
      class="textarea" 
      required
      @input="updateBlockTextMessageEvent"
      maxlength="4096"
    />
  </div>
</template>

<style scoped>
</style>