<script setup>
import { reactive } from 'vue';

const props = defineProps({
  block: {
    type: Object,
    required: true,
  }
});

const editedBlock = reactive({ ...props.block })

const emits = defineEmits(['update-text-in-block', 'delete-block']);

const updateBlockTextMessageEvent = () => {
  emits('update-text-in-block', editedBlock)
};

const deleteBlockEvent = () => {
  emits('delete-block', editedBlock)
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
      <img src="@/assets/icons/blocks/msg-purple.svg">
      <p class="block__type">Текст</p>
    </div>
    <AppTextarea
      v-model="editedBlock.message_text"
      placeholder="Введите текст"
      class="textarea" 
      required
      @input="updateBlockTextMessageEvent"
    />
  </div>
</template>

<style scoped>
.textarea {
  box-sizing: border-box;
  width: 100%;
  height: 112px;
  resize: none;
}
</style>