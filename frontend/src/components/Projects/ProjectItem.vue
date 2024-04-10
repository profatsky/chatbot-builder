<script setup>
import { ref, reactive } from 'vue';

const keyboardTypes = ref([
  {label: 'Inline Keyboard', value: 'inline_keyboard'},
  {label: 'Reply Keyboard', value: 'reply_keyboard'},
]);
const selectedKeyboardType = ref(keyboardTypes.value[0]);

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
});

const editedProject = reactive({ ...props.project })

const emits = defineEmits(['update-project']);

function updateProject() {
  emits('update-project', editedProject)
}
</script>

<template>
  <div class="project">
    <div class="project__management">
      <div class="project__header">
        <div class="project__name">
          <img src="@/assets/icons/telegram-purple.svg">
          <h2 class="name__text">{{ project.name }}</h2>
        </div>
        <AppButton size="small" importance="secondary">Сохранить</AppButton>
      </div>
      <div class="project__actions">
        <div class="action">
          <img src="@/assets/icons/export-gray.svg">
          <div>Получить код</div>
        </div>
        <div class="action">
          <img src="@/assets/icons/pencil-gray.svg">
          <div>Изменить название</div>
        </div>
        <div class="action">
          <img src="@/assets/icons/remove-gray.svg">
          <div>Удалить чат-бота</div>
        </div>
      </div>
      <AppTextarea 
        v-model="editedProject.start_message"
        placeholder="Введите текст приветственного сообщения"
        class="textarea" 
        required
        @input="updateProject"
      />
      <div class="project__keyboard">
        <p class="clue">Выберите тип кнопок для главного меню</p>
        <AppSelect 
          v-model="editedProject.start_keyboard_type"
          :options="keyboardTypes"
          required
          @change="updateProject"
        />
      </div>
    </div>
    <div class="dialogues">
        <h3 class="dialogues__title">Диалоги (0/15)</h3>
        <AppButton 
          size="large" 
          importance="secondary"
        >
          Добавить диалог
        </AppButton>
      </div>
      <div class="plugins">
        <h3 class="plugins__title">Плагины (0/15)</h3>
        <AppButton 
          size="large" 
          importance="secondary"
        >
          Добавить плагин
        </AppButton>
      </div>
  </div>
</template>

<style scoped>
.textarea {
  box-sizing: border-box;
  width: 100%;
  height: 112px;
  resize: none;
}

.project {
  background-color: var(--light-gray);
  padding: 44px 48px;
  
  border-radius: 16px;
}

.project__management {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.project__header {
  display: flex;
  justify-content: space-between;
}

.project__name {
  display: flex;
  align-items: center;
  gap: 12px;

  text-wrap: nowrap;
}

.name__text {
  font-size: 20px;
  font-weight: 500px;
  letter-spacing: 1px;
}

.project__actions {
  display: flex;
  gap: 60px;

  color: var(--body-text);
  font-size: 16px;
  letter-spacing: 0.75px;
  line-height: 34px;
}

.action {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.clue {
  font-size: 16px;
  font-weight: 500;
  color: var(--body-text);
  letter-spacing: 0.75px;
  line-height: 28px;
  margin-bottom: 12px;
}

.dialogues,
.plugins {
  margin-top: 40px;
}

.dialogues__title,
.plugins__title {
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 3px;
  line-height: 32px;
  color: var(--primary);
  text-transform: uppercase;
  margin-bottom: 24px;
}

</style>