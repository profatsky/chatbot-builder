<script setup>
import { reactive } from 'vue';
import KeyValueTable from '@/components/Block/BlockInstance/BlockInstancePart/KeyValueTable.vue';

const props = defineProps({
  block: {
    type: Object,
    required: true,
  }
});

const editedBlock = reactive({ ...props.block })

const emits = defineEmits(['update-text-in-block', 'update-block', 'delete-block']);

const updateBlockTextEvent = () => {
  emits('update-text-in-block', editedBlock)
};

const updateBlockHttpMethodEvent = () => {
  emits('update-block', editedBlock)
};

const updateBlockHeadersEvent = (headers) => {
  editedBlock.headers = headers;
  emits('update-block', editedBlock)
};

const updateBlockBodyEvent = (body) => {
  editedBlock.body = body;
  emits('update-block', editedBlock)
}

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
      <img src="@/assets/icons/blocks/request-purple.svg">
      <p class="block__type">API запрос</p>
    </div>

    <AppInput
      class="input"
      v-model="editedBlock.url"
      placeholder="Введите ссылку"
      required
      @input="updateBlockTextEvent"
    />

    <div class="block__http-method">
      <p class="block__hint">
        Выберите метод HTTP-запроса
      </p>
      <div class="answer-type__select">
        <input 
          type="radio" 
          :id="`GET${editedBlock.block_id}`" 
          value="GET" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label :for="`GET${editedBlock.block_id}`">GET</label>

        <input 
          type="radio" 
          :id="`POST${editedBlock.block_id}`" 
          value="POST" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label :for="`POST${editedBlock.block_id}`">POST</label>

        <input 
          type="radio" 
          :id="`PUT${editedBlock.block_id}`" 
          value="PUT" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label :for="`PUT${editedBlock.block_id}`">PUT</label>

        <input 
          type="radio" 
          :id="`DELETE${editedBlock.block_id}`" 
          value="DELETE" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label :for="`DELETE${editedBlock.block_id}`">DELETE</label>

        <input 
          type="radio" 
          :id="`PATCH${editedBlock.block_id}`" 
          value="PATCH" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label :for="`PATCH${editedBlock.block_id}`">PATCH</label>

        <input 
          type="radio" 
          :id="`CONNECT${editedBlock.block_id}`" 
          value="CONNECT" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label :for="`CONNECT${editedBlock.block_id}`">CONNECT</label>

        <input 
          type="radio" 
          :id="`HEAD${editedBlock.block_id}`" 
          value="HEAD" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label :for="`HEAD${editedBlock.block_id}`">HEAD</label>

        <input 
          type="radio" 
          :id="`OPTIONS${editedBlock.block_id}`" 
          value="OPTIONS" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label :for="`OPTIONS${editedBlock.block_id}`">OPTIONS</label>
      </div>
    </div>

    <div class="block__headers">
      <p class="block__hint">
        Укажите заголовки
      </p>

      <KeyValueTable
        :key-value-data="editedBlock.headers"
        @update-data="updateBlockHeadersEvent"
      >
        <template v-slot:keyColumnTitle>Заголовок</template>
        <template v-slot:valueColumnTitle>Значение</template>
      </KeyValueTable>
    </div>

    <div class="block__request-body">
      <p class="block__hint">
        Введите пары “ключ-значение” для тела запроса. Строковые значения указывайте в кавычках.
      </p>

      <KeyValueTable
        :key-value-data="editedBlock.body"
        @update-data="updateBlockBodyEvent"
      >
        <template v-slot:keyColumnTitle>Ключ</template>
        <template v-slot:valueColumnTitle>Значение</template>
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

.block__http-method {
  margin-bottom: 8px;
}

.block__headers {
  margin-bottom: 20px;
}

input[type="radio"] {
  display: none;
}

input[type="radio"] + label {
  display: inline-block;
  padding: 7px 16px;
  margin-right: 8px ;
  margin-bottom: 12px;
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
</style>