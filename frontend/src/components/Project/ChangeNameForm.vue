<script setup>
import { ref } from 'vue';

const props = defineProps({
  projectName: {
    type: String,
    required: true,
  }
});

const name = ref('');

const emits = defineEmits(['update-project']);
const updateProjectNameEvent = () => {
  emits('update-project', name);
};

const submitForm = async () => {
  updateProjectNameEvent();
};
</script>

<template>
  <form @submit.prevent="submitForm" class="change-name">
    <h2 class="change-name__title">Изменение названия</h2>
    <AppInput
      v-model="name"
      required 
      placeholder="Введите новое название"
      minlength="1"
      maxlength="256"
      class="change-name__input"
    />
    <AppButton 
      type="submit" 
      size="medium" 
      importance="primary"
      class="change-name__btn"
    >
      Сохранить
    </AppButton>
  </form>
</template>

<style scoped>
.change-name {
  width: 360px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.change-name__title {
  font-size: 28px;
  font-weight: 600px;
  line-height: 32px;
  margin-bottom: 8px;
}

.change-name__input{
  width: 312px;
  background-color: var(--light-gray);
}

.change-name__btn {
  width: 100%;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .change-name {
    width: 280px;
    gap: 12px;
  }

  .change-name__title {
    font-size: 24px;
    line-height: 28px;
    margin-bottom: 6px;
  }

  .change-name__input{
    width: 240px;
  }
}

@media (max-width: 767px) { 
  .change-name {
    width: 200px;
    gap: 8px
  }

  .change-name__title {
    font-size: 16px;
    line-height: 20px;
    margin-bottom: 4px;
  }

  .change-name__input{
    width: 184px;
  }
}
</style>