<script setup>
import { ref, reactive } from 'vue';
import AddTableRowForm from '@/components/Block/BlockInstance/BlockInstancePart/AddTableRowForm.vue';

const props = defineProps({
  keyValueData: {
    type: Object,
    required: true,
  }
});

const editedData = reactive({ ...props.keyValueData });

const emits = defineEmits(['update-data']);
const updateDataEvent = () => {
  emits('update-data', editedData)
};

const showAddRowModal = ref(false);
const openAddRowModal = () => {
  showAddRowModal.value = true;
};
const closeAddRowModal = () => {
  showAddRowModal.value = false;
};

const addOrUpdateRow = (row) => {
  editedData[row.pairKey] = row.pairValue;
  closeAddRowModal();
  updateDataEvent();
};

const deleteRow = (key) => {
  delete editedData[key];
  updateDataEvent();
};
</script>

<template>
  <AppModal 
    v-if="showAddRowModal" @closeModal="closeAddRowModal"
  >
    <AddTableRowForm
      @add-row="addOrUpdateRow"
    />
  </AppModal>
  
  <table>
    <thead>
      <tr>
        <th><slot name="keyColumnTitle"></slot></th>
        <th><slot name="valueColumnTitle"></slot></th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(value, key) in editedData" :key="key">
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

  <AppButton v-if="Object.keys(keyValueData).length <= 25"
    size="small"
    importance="secondary"
    @click="openAddRowModal"
    class="btn"
  >
    Добавить новую строку в таблицу
  </AppButton>
</template>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  overflow: hidden;
  margin-bottom: 12px;
  table-layout: fixed;
}

th:not(:last-child), td:not(:last-child) {
  border: 1px solid var(--gray-lines);
  width: 252px;
}

th:last-child, td:last-child {
  background: none;
  border: 0;
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
  padding: 10px;
}

.btn {
  width: 100%;
}

@media (min-width: 768px) and (max-width: 1169px) {
  th:not(:last-child), td:not(:last-child) {
    border: 1px solid var(--gray-lines);
    width: 226px;
  }

  th {
    font-size: 14px;
    line-height: 32px;
  }

  td {
    font-size: 14px;
    line-height: 28px;
  }
}
</style>