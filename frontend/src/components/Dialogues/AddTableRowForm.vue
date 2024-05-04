<script setup>
import { reactive } from 'vue';

const row = reactive({
  pairKey: '', 
  pairValue: ''
});

const emits = defineEmits(['add-row']);
const addTableRowEvent = () => {
  emits('add-row', row)
};

const submitForm = () => {
  addTableRowEvent();
};

</script>

<template>
  <div class="add-row">
    <h2 class="add-row__title">Добавить строку в таблицу</h2>
    <form @submit.prevent="submitForm" class="add-row__form">
      <AppInput
        v-model="row.pairKey"
        required
        placeholder="Введите название столбца"
        class="form__input"
      />
      <AppInput
        v-model="row.pairValue"
        required
        placeholder="Введите значение столбца"
        class="form__input"
      />
      <AppButton
        type="submit"
        size="medium"
        importance="primary"
        class="form__btn"
      >
        Добавить
      </AppButton>
    </form>
  </div>
</template>

<style scoped>
.add-row {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  width: 500px;
}

.add-row__title {
  font-size: 20px;
  font-weight: 600px;
  margin-top: 0;
  margin-bottom: 28px;
}

.add-row__form {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  width: 370px;
  gap: 16px;
}

.form__input {
  width: 325px;
  background-color: var(--light-gray);
}

.form__btn {
  margin-top: 24px;
}
</style>