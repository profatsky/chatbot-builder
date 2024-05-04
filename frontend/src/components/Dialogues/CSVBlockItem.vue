<script setup>
import { ref, reactive } from 'vue';
import AddTableRowForm from '@/components/Dialogues/AddTableRowForm.vue';
import KeyValueTable from '@/components/Dialogues/KeyValueTable.vue';

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
const updateBlockTableEvent = (data) => {
  editedBlock.data = data;
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

      <KeyValueTable
        :key-value-data="editedBlock.data"
        @update-data="updateBlockTableEvent"
      >
        <template v-slot:keyColumnTitle>Столбец</template>
        <template v-slot:valueColumnTitle>Данные</template>
      </KeyValueTable>
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
</style>