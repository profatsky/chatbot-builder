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
  for (let key in body) {
    if (!isNaN(body[key])) {
      body[key] = Number(body[key]);
    } else {
      body[key] = body[key].replace(/"/g, '');
    }
  }
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
      <img src="@/assets/icons/blocks/request-purple.svg" class="block__img">
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
        Укажите заголовки запроса
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
        Укажите содержимое тела запроса. Строковые значения необходимо указывать в двойных кавычках
      </p>

      <KeyValueTable
        :key-value-data="editedBlock.body"
        @update-data="updateBlockBodyEvent"
      >
        <template v-slot:keyColumnTitle>Ключ</template>
        <template v-slot:valueColumnTitle>Значение</template>
      </KeyValueTable>
    </div>
  
    <p class="block__hint block__hint--last">
      Вы можете отправить в тексте сообщения значение из ответа от API, для этого указывайте в тексте: &ltresponse[“ключ”]&gt. Например: &ltresponse[“id”]&gt
    </p>
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
  padding: 5px 16px;
  margin-right: 8px ;
  margin-bottom: 12px;

  border: 2px solid var(--primary);
  border-radius: 20px;
  
  font-size: 12px;  
  font-weight: 500;
  line-height: 18px;
  color: var(--primary);

  cursor: pointer;
}

input[type="radio"]:checked + label {
  background-color: var(--primary);
  color: var(--main-white);
}

@media (min-width: 768px) and (max-width: 1169px) {
  .input {
    margin-bottom: 16px;
  }

  .block__headers {
    margin-bottom: 16px;
  }

  input[type="radio"] + label {
    font-size: 10px;
    padding: 3px 16px;
    margin-right: 6px ;
    margin-bottom: 8px;
  }
}

@media (max-width: 767px) {
  .input {
    margin-bottom: 8px;
  }

  .block__headers {
    margin-bottom: 8px;
  }

  input[type="radio"] + label {
    font-size: 8px;
    line-height: 12px;
    padding: 2px 14px;
    margin-right: 4px;
    margin-bottom: 6px;
  }
}
</style>