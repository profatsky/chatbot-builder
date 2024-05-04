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
    />
    <div class="block__answer-type">
      <p class="block__clue">
        Выберите тип ответа, ожидаемый от пользователя
      </p>
      <div class="answer-type__select">
        <input 
          type="radio" 
          id="any" 
          value="any" 
          v-model="editedBlock.answer_type"
          @change="updateBlockAnswerTypeEvent"
        >
        <label for="any">Любой</label>

        <input 
          type="radio" 
          id="text" 
          value="text" 
          v-model="editedBlock.answer_type"
          @change="updateBlockAnswerTypeEvent"
        >
        <label for="text">Текст</label>

        <input 
          type="radio" 
          id="int" 
          value="int" 
          v-model="editedBlock.answer_type"
          @change="updateBlockAnswerTypeEvent"
        >
        <label for="int">Число</label>

        <input 
          type="radio" 
          id="email" 
          value="email" 
          v-model="editedBlock.answer_type"
          @change="updateBlockAnswerTypeEvent"
        >
        <label for="email">Электронная почта</label>

        <input 
          type="radio" 
          id="phone_number" 
          value="phone_number" 
          v-model="editedBlock.answer_type"
          @change="updateBlockAnswerTypeEvent"
        >
        <label for="phone_number">Номер телефона</label>
      </div>
      <p class="block__clue block__clue--last">
        Вы можете использовать ответ на вопрос в других блоках. <br>
        Для этого указывайте answer[номер ответа]. Например: answer[1]
      </p>
    </div>
  </div>
</template>

<style scoped>
.textarea {
  box-sizing: border-box;
  width: 100%;
  height: 112px;
  resize: none;
  margin-bottom: 20px;
}

.answer-type__select {
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

.block__clue--last {
  margin-bottom: 0;
}
</style>