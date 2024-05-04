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

const updateBlockTextEvent = () => {
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
      <img src="@/assets/icons/blocks/email-purple.svg">
      <p class="block__type">Email письмо</p>
    </div>
    <AppInput
      class="input"
      v-model="editedBlock.subject"
      placeholder="Введите тему письма"
      required
      @input="updateBlockTextEvent"
    />
    <AppTextarea
      class="textarea" 
      v-model="editedBlock.text"
      placeholder="Введите текст письма"
      required
      @input="updateBlockTextEvent"
    />
    <AppInput
      class="input"
      v-model="editedBlock.recipient_email"
      placeholder="Введите почту получателя"
      required
      @input="updateBlockTextEvent"
    />
  </div>
</template>

<style scoped>
.textarea {
  box-sizing: border-box;
  width: 100%;
  height: 112px;
  resize: none;
  margin: 20px 0;
}

.input {
  box-sizing: border-box;
  width: 100%;
  resize: none;
}
</style>