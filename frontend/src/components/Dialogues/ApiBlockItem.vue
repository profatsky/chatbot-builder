<script setup>
import { reactive } from 'vue';
import KeyValueTable from './KeyValueTable.vue';

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
      <p class="block__clue">
        Выберите метод HTTP-запроса
      </p>
      <div class="answer-type__select">
        <input 
          type="radio" 
          id="GET" 
          value="GET" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label for="GET">GET</label>

        <input 
          type="radio" 
          id="POST" 
          value="POST" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label for="POST">POST</label>

        <input 
          type="radio" 
          id="PUT" 
          value="PUT" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label for="PUT">PUT</label>

        <input 
          type="radio" 
          id="DELETE" 
          value="DELETE" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label for="DELETE">DELETE</label>

        <input 
          type="radio" 
          id="PATCH" 
          value="PATCH" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label for="PATCH">PATCH</label>

        <input 
          type="radio" 
          id="CONNECT" 
          value="CONNECT" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label for="CONNECT">CONNECT</label>

        <input 
          type="radio" 
          id="HEAD" 
          value="HEAD" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label for="HEAD">HEAD</label>

        <input 
          type="radio" 
          id="OPTIONS" 
          value="OPTIONS" 
          v-model="editedBlock.http_method"
          @change="updateBlockHttpMethodEvent"
        >
        <label for="OPTIONS">OPTIONS</label>
      </div>
    </div>

    <div class="block__headers">
      <p class="block__clue">
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
      <p class="block__clue">
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