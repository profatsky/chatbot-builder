<script setup>
import { shallowRef } from 'vue';
import { debounce } from 'lodash';

import TextBlockItem from '@/components/Block/BlockInstance/TextBlockItem.vue';
import ImageBlockItem from '@/components/Block/BlockInstance/ImageBlockItem.vue';
import QuestionBlockItem from '@/components/Block/BlockInstance/QuestionBlockItem.vue';
import CSVBlockItem from '@/components/Block/BlockInstance/CSVBlockItem.vue';
import EmailBlockItem from '@/components/Block/BlockInstance/EmailBlockItem.vue';
import ApiBlockItem from '@/components/Block/BlockInstance/ApiBlockItem.vue';

const props = defineProps({
  block: {
    type: Object,
    required: true,
  },
  questionCounter: {
    type: Number,
    required: true,
  }
});

const emits = defineEmits(['update-block', 'delete-block', 'upload-image']);

const updateTextInBlockEvent = debounce((block) => {
  emits('update-block', block)
}, 3000);

const updateBlockEvent = (block) => {
  emits('update-block', block)
};

const deleteBlockEvent = (block) => {
  emits('delete-block', block)
};

const uploadImageEvent = (block, formData) => {
  emits('upload-image', block, formData)
};

const currentComponent = shallowRef(null);

switch (props.block.type) {
  case 'text_block':
    currentComponent.value = TextBlockItem;
    break;
  case 'image_block':
    currentComponent.value = ImageBlockItem;
    break;
  case 'question_block':
    currentComponent.value = QuestionBlockItem;
    break;
  case 'csv_block':
    currentComponent.value = CSVBlockItem;
    break;
  case 'email_block':
    currentComponent.value = EmailBlockItem;
    break;
  case 'api_block':
    currentComponent.value = ApiBlockItem;
    break;
  default:
    currentComponent.value = null;
    break;
};

</script>

<template>
  <component 
    :is="currentComponent" 
    :block="block"
    @upload-image="uploadImageEvent"
    @update-text-in-block="updateTextInBlockEvent"
    @update-block="updateBlockEvent"
    @delete-block="deleteBlockEvent"
  />
  <div v-if="currentComponent === QuestionBlockItem">
    <div class="user-answer block">
      <div class="block__header">
        <img src="@/assets/icons/blocks/msg-purple.svg" class="block__img">
        <p class="block__type">Ответ от пользователя на вопрос №{{ questionCounter }}</p>
      </div>
      <p class="block__hint block__hint--last">
        Вы можете использовать ответ в сообщениях чат-бота, 
        для этого указывайте в тексте: &ltanswers[{{ questionCounter }}]&gt
      </p>
    </div>
  </div>
</template>

<style>
.block {
  background-color: var(--light-gray);
  border-radius: 16px;
  padding: 24px 28px;
  width: 642px;
  margin-bottom: 28px;
  box-shadow: 0 0 16px 0 rgba(17, 17, 17, 0.04);
  margin-left: auto;
}

.user-answer {
  width: 448px;
  margin-left: 0;
}

.block__close-button {
  background-color: var(--light-gray);
  float: right;
}

.block__close-button img {
  width: 18px;
  height: 18px;
}

.block__header {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  align-items: center;
}

.block__img {
  width: 32px;
  height: 32px;
}

.block__type {
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.75px;
}

.block__hint {
  font-size: 14px;
  font-weight: 400;
  color: var(--body-text);
  letter-spacing: 0.75px;
  line-height: 24px;
  margin-bottom: 8px;
}

.block__hint--last {
  margin-top: 20px;
  margin-bottom: 0;
}

.textarea {
  box-sizing: border-box;
  width: 100%;
  height: 112px;
  resize: none;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .block {
    border-radius: 12px;
    padding: 20px 24px;
    width: 548px;
    margin-bottom: 24px;
  }

  .user-answer {
    width: 448px;
    margin-left: 0;
  }

  .block__close-button img {
    width: 14px;
    height: 14px;
  }

  .block__header {
    gap: 8px;
    margin-bottom: 16px;
  }

  .block__img {
    width: 28px;
    height: 28px;
  }

  .block__type {
    font-size: 14px;
  }

  .block__hint {
    font-size: 14px;
    line-height: 20px;
    margin-bottom: 8px;
  }

  .block__hint--last {
    margin-top: 16px;
    margin-bottom: 0;
  }

  .textarea {
    height: 84px;
  }
}

@media (max-width: 767px) {
  .block {
    border-radius: 8px;
    padding: 10px 12px;
    width: 196px;
    margin-bottom: 20px;
  }

  .user-answer {
    width: 216px;
    margin-left: 0;
  }

  .block__close-button img {
    width: 10px;
    height: 10px;
  }

  .block__header {
    gap: 4px;
    margin-bottom: 8px;
  }

  .block__img {
    width: 18px;
    height: 18px;
  }

  .block__type {
    font-size: 8px;
  }

  .block__hint {
    font-size: 8px;
    line-height: 12px;
    margin-bottom: 4px;
  }

  .block__hint--last {
    margin-top: 8px;
    margin-bottom: 0;
  }

  .textarea {
    height: 64px;
  }
}
</style>