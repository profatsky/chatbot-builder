<script setup>
import { reactive } from 'vue';

const row = reactive({
  pairKey: '', 
  pairValue: ''
});

const emits = defineEmits(['add-row']);
const addTableRowEvent = () => {
  emits('add-row', row);
};

const submitForm = () => {
  addTableRowEvent();
};
</script>

<template>
  <form @submit.prevent="submitForm" class="add-row">
    <h2 class="add-row__title">Добавить строку в таблицу</h2>
    <AppInput
      v-model="row.pairKey"
      required
      placeholder="Значение для левого столбца"
      class="add-row__input"
    />
    <AppInput
      v-model="row.pairValue"
      required
      placeholder="Значение для правого столбца"
      class="add-row__input"
    />
    <AppButton
      type="submit"
      size="medium"
      importance="primary"
      class="add-row__btn"
    >
      Добавить
    </AppButton>
  </form>
</template>

<style scoped>
.add-row {
  width: 360px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.add-row__title {
  font-size: 28px;
  font-weight: 600px;
  line-height: 32px;
  margin-bottom: 8px;
  text-align: center;
}

.add-row__input {
  width: 312px;
  background-color: var(--light-gray);
}

.add-row__btn {
  width: 100%;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .add-row {
    width: 280px;
    gap: 12px;
  }

  .add-row__title {
    font-size: 24px;
    line-height: 28px;
    margin-bottom: 6px;
  }

  .add-row__input{
    width: 240px;
  }
}

@media (max-width: 767px) { 
  .add-row {
    width: 200px;
    gap: 8px
  }

  .add-row__title {
    font-size: 16px;
    line-height: 20px;
    margin-bottom: 4px;
  }

  .add-row__input{
    width: 184px;
  }
}
</style>