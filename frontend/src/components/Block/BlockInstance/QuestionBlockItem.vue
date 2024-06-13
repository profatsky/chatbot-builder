<script setup>
import { reactive } from 'vue';

const props = defineProps({
  block: {
    type: Object,
    required: true,
  }
});

const editedBlock = reactive({ ...props.block });

const emits = defineEmits(['update-text-in-block', 'update-block', 'delete-block']);

const updateBlockTextMessageEvent = () => {
  emits('update-text-in-block', editedBlock)
};

const updateBlockAnswerTypeEvent = () => {
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
      class="block__close-button"
    >
      <img src="@/assets/icons/close.svg">
    </button>
    <div class="block__header">
      <img src="@/assets/icons/blocks/question-purple.svg">
      <p class="block__type">Вопрос</p>
    </div>
    <AppTextarea
      v-model="editedBlock.message_text"
      placeholder="Введите текст вопроса"
      class="textarea" 
      required
      @input="updateBlockTextMessageEvent"
      maxlength="4096"
    />
    <div class="block__answer-type">
      <p class="block__hint">
        Выберите тип ответа, ожидаемый от пользователя
      </p>
      <div class="answer-type__select">
        <input 
          type="radio" 
          :id="`any${editedBlock.block_id}`" 
          value="any" 
          v-model="editedBlock.answer_type"
          @change="updateBlockAnswerTypeEvent"
        >
        <label :for="`any${editedBlock.block_id}`">Любой</label>

        <input 
          type="radio" 
          :id="`text${editedBlock.block_id}`" 
          value="text" 
          v-model="editedBlock.answer_type"
          @change="updateBlockAnswerTypeEvent"
        >
        <label :for="`text${editedBlock.block_id}`">Текст</label>

        <input 
          type="radio" 
          :id="`int${editedBlock.block_id}`" 
          value="int" 
          v-model="editedBlock.answer_type"
          @change="updateBlockAnswerTypeEvent"
        >
        <label :for="`int${editedBlock.block_id}`">Число</label>

        <input 
          type="radio" 
          :id="`email${editedBlock.block_id}`" 
          value="email" 
          v-model="editedBlock.answer_type"
          @change="updateBlockAnswerTypeEvent"
        >
        <label :for="`email${editedBlock.block_id}`">Электронная почта</label>

        <input 
          type="radio" 
          :id="`phone_number${editedBlock.block_id}`" 
          value="phone_number" 
          v-model="editedBlock.answer_type"
          @change="updateBlockAnswerTypeEvent"
        >
        <label :for="`phone_number${editedBlock.block_id}`">Номер телефона</label>
      </div>
    </div>
  </div>
</template>

<style scoped>
.textarea {
  margin-bottom: 20px;
}

input[type="radio"] {
  display: none;
}

input[type="radio"] + label {
  display: inline-block;
  padding: 7px 16px;
  margin-right: 8px ;
  border: 2px solid var(--primary);
  border-radius: 20px;
  cursor: pointer;
  font-size: 12px;
  color: var(--primary);
  font-weight: 500;
}

input[type="radio"]:checked + label {
  background-color: var(--primary);
  color: var(--main-white);
}

@media (min-width: 768px) and (max-width: 1169px) {
  input[type="radio"] + label {
    font-size: 10px;
    padding: 5px 16px;
    margin-right: 6px;
  }
}
</style>