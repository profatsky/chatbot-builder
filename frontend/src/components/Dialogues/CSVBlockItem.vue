<script setup>
import { ref, reactive } from 'vue';
import AddTableRowForm from '@/components/Dialogues/AddTableRowForm.vue';

const props = defineProps({
  block: {
    type: Object,
    required: true,
  }
});

const editedBlock = reactive({ ...props.block });

const emits = defineEmits(['update-text-in-block', 'update-block', 'delete-block']);
const updateBlockFileNameEvent = () => {
  emits('update-text-in-block', editedBlock)
};
const updateBlockTableEvent = () => {
  emits('update-block', editedBlock)
};
const deleteBlockEvent = () => {
  emits('delete-block', editedBlock)
};


const showAddRowModal = ref(false);
const openAddRowModal = () => {
  showAddRowModal.value = true;
};
const closeAddRowModal = () => {
  showAddRowModal.value = false;
};

const addRow = (row) => {
  editedBlock.data[row.pairKey] = row.pairValue;
  closeAddRowModal();
  updateBlockTableEvent();
};

const deleteRow = (key) => {
  delete editedBlock.data[key];
  updateBlockTableEvent();
};

</script>

<template>
  <div class="block">
    
    <AppModal 
      v-if="showAddRowModal" @closeModal="closeAddRowModal"
    >
      <AddTableRowForm
        @add-row="addRow"
      />
    </AppModal>

    <button 
      @click="deleteBlockEvent" 
      class="block__close-button"
    >
      <img src="@/assets/icons/close.svg">
    </button>
    <div class="block__header">
      <img src="@/assets/icons/blocks/csv-purple.svg">
      <p class="block__type">Сохранить в CSV</p>
    </div>
    <AppInput
      v-model="editedBlock.file_path"
      placeholder="Введите название файла"
      class="input" 
      required
      @input="updateBlockFileNameEvent"
    />
    <div class="block__saving-data">
      <p class="block__clue">
        Укажите данные для сохранения в файл
      </p>

      <table>
        <thead>
          <tr>
            <th>Название колонки</th>
            <th>Данные</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(value, key) in editedBlock.data" :key="key">
            <td>{{ key }}</td>
            <td>{{ value }}</td>
            <td>
              <img 
                src="@/assets/icons/remove-gray.svg" 
                align="center"
                class="remove-icon"
                @click="deleteRow(key)"
              >
            </td>
          </tr>
        </tbody>
      </table>

      <AppButton
        size="small"
        importance="secondary"
        @click="openAddRowModal"
        class="btn"
      >
        Добавить новую строку в таблицу
      </AppButton>
    </div>
  </div>
</template>

<style scoped>
.input {
  box-sizing: border-box;
  width: 100%;
  resize: none;
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  overflow: hidden;
  margin-bottom: 12px;
}

th, td {
  border: 1px solid var(--gray-lines);
}

th {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.75px;
  line-height: 32px;
  text-align: center;
  color: var(--body-text);

  background-color: var(--light-gray);
  padding: 12px;
}

td {
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0.75px;
  line-height: 28px;
  text-align: center;
  color: var(--body-text);

  background-color: var(--main-white);
  max-width: 273px;
  padding: 12px;
}

.btn {
  width: 100%;
}

</style>