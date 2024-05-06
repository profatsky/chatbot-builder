<script setup>
import { ref } from 'vue';
import { useToast } from 'vue-toast-notification';

const toast = useToast();

const props = defineProps({
  projectName: {
    type: String,
    required: true,
  }
});

const name = ref('')

const emits = defineEmits(['update-project']);
const updateProjectNameEvent = () => {
  emits('update-project', name)
}

const checkNameLength = () => {
  return (name.value.length >=1 && name.value.length <= 256);
}

const submitForm = async () => {
  if (!checkNameLength) {
    toast.error('Длина названия должна быть от 1 до 256 символов!');
    return;
  }
  updateProjectNameEvent();
}
</script>

<template>
  <div class="change-name">
    <h2 class="change-name__title">Изменение названия</h2>
    <form @submit.prevent="submitForm" class="change-name__form">
      <AppInput
        v-model="name"
        required 
        placeholder="Введите новое название"
      />
      <AppButton 
        type="submit" 
        size="medium" 
        importance="primary"
        class="change-name-form__btn"
      >
        Изменить
      </AppButton>
    </form>
  </div>
</template>

<style scoped>
.change-name {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  width: 500px;
}

.change-name__title {
  font-size: 36px;
  font-weight: 600px;
  margin-top: 0;
  margin-bottom: 28px;
}

.input {
  width: 325px;
  background-color: var(--light-gray);
}

.change-name__form {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  width: 370px;
  gap: 16px;
}

.change-name-form__btn {
  margin-top: 20px;
}
</style>