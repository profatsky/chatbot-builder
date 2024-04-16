<script setup>
import { reactive } from 'vue';

const props = defineProps({
  block: {
    type: Object,
    required: true,
  }
});

const editedBlock = reactive({ ...props.block })

const emits = defineEmits(['update-block', 'delete-block']);

const updateBlockTextMessageEvent = () => {
  emits('update-block', editedBlock)
};

const deleteBlockEvent = () => {
  emits('delete-block', editedBlock)
};


</script>

<template>
  <div class="block">
    <button 
      @click="deleteBlockEvent" 
      class="close-button"
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
.block {
  background-color: var(--light-gray);
  border-radius: 16px;
  padding: 24px 28px;
  width: 642px;
}

.close-button {
  background-color: var(--light-gray);
  float: right;
}

.block__header {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  align-items: center;
}

.block__type {
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.75px;
}

.textarea {
  box-sizing: border-box;
  width: 100%;
  height: 112px;
  resize: none;
}

</style>