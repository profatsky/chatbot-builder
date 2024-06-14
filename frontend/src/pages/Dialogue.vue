<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toast-notification';

import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import BlockList from '@/components/Block/BlockList.vue';
import BlockTypeList from '@/components/Block/BlockType/BlockTypeList.vue';
import blockObjects from '@/components/Block/blocks'

import msgPurpleIcon from '@/assets/icons/blocks/msg-purple.svg';
import imgPurpleIcon from '@/assets/icons/blocks/img-purple.svg';
import questionPurpleIcon from '@/assets/icons/blocks/question-purple.svg';
import csvPurpleIcon from '@/assets/icons/blocks/csv-purple.svg';
import emailPurpleIcon from '@/assets/icons/blocks/email-purple.svg';
import requestPurpleIcon from '@/assets/icons/blocks/request-purple.svg';

import { getBlocks, createBlock, updateBlock, deleteBlock, uploadImage } from '@/api/blocks';

const blockTypes = ref([
  { value: 'textBlock', name: 'Текст', imgPath: msgPurpleIcon },
  { value: 'imageBlock', name: 'Изображение', imgPath: imgPurpleIcon },
  { value: 'questionBlock', name: 'Вопрос', imgPath: questionPurpleIcon },
  { value: 'csvBlock', name: 'Сохранить в CSV', imgPath: csvPurpleIcon },
  { value: 'emailBlock', name: 'Email письмо', imgPath: emailPurpleIcon },
  { value: 'apiBlock', name: 'API запрос', imgPath: requestPurpleIcon }
]);

const toast = useToast();
const route = useRoute();
const router = useRouter();

const blocks = ref([]);

const isBlocksLoading = ref(true);

const handleAddBlockEvent = async (blockType) => {
  if (blocks.value.length >= 15) {
    toast.error('В этом диалоге максимальное количество блоков!');
    return;
  };

  const newBlock = { ...blockObjects[blockType.value] };
  newBlock.sequence_number = blocks.value.length + 1;

  const { response, error } = await createBlock(
    route.params.projectId,
    route.params.dialogueId,
    newBlock
  );
  if (error.value) {
    toast.error('Что-то пошло не так...')
  } else {
    const responseData = response.value.data;
    blocks.value.push(responseData);
    toast.success('Новый блок успешно добавлен')
  }
};

const handleUpdateBlockEvent = async (editedBlock) => {
  const { response, error } = await updateBlock(
    route.params.projectId,
    route.params.dialogueId,
    editedBlock
  );
  if (error.value) {
    toast.error('Что-то пошло не так...')
  } else {
    const responseData = response.value.data;
    const index = blocks.value.findIndex(
      b => b.block_id === editedBlock.block_id
    );
    if (index !== -1) {
      blocks.value[index] = responseData;
      toast.success('Данные о блоке обновлены');
    }
  }
};

const handleDeleteBlockEvent = async (block) => {
  const { response, error } = await deleteBlock(
    route.params.projectId,
    route.params.dialogueId,
    block.block_id
  );

  if (error.value) {
    toast.error('Что-то пошло не так...')
  } else {
    await getBlocksFromApi();
    toast.success('Блок успешно удален')
  }
}

const handleUploadImageEvent = async (editedBlock, formData) => {
  const { response, error } = await uploadImage(
    route.params.projectId,
    route.params.dialogueId,
    editedBlock.block_id,
    formData,
  );

  if (error.value) {
    toast.error('Что-то пошло не так...')
  } else {
    const responseData = response.value.data;
    const index = blocks.value.findIndex(
      b => b.block_id === editedBlock.block_id
    );
    blocks.value[index] = responseData;
    router.go();
  }
};

const getBlocksFromApi = async () => {
  const { response, error } = await getBlocks(
    route.params.projectId,
    route.params.dialogueId
  );

  if (error.value) {
    toast.error('Что-то пошло не так...')
  } else {
    isBlocksLoading.value = false;
    const responseData = response.value.data;
    blocks.value = responseData;
  }
};

const showBlockTypesModal = ref(false);

const openBlockTypesModal = () => {
  showBlockTypesModal.value = true;
};

const closeBlockTypesModal = () => {
  showBlockTypesModal.value = false;
};

onMounted(async () => await getBlocksFromApi());
</script>

<template>
  <SidebarNavigation/>
  <main>
    <AppModal 
      v-if="showBlockTypesModal" @closeModal="closeBlockTypesModal"
    >
        <p class="hint">Чтобы добавить блок, нажмите на него</p>
        <BlockTypeList
          :blockTypes="blockTypes"
          @add-block="handleAddBlockEvent"
        />
    </AppModal>
    <div class="container">
      <div class="page__content">
        <div class="page__header">
          <h1 class="header__title">Диалог</h1>
          <AppButton
            class="add-block-btn"
            @click="openBlockTypesModal"
          >
            Добавить новый блок
          </AppButton>
        </div>
        <p class="page__hint">
          Диалоги - это сценарии общения чат-бота с пользователями. Каждый диалог состоит из различных блоков: отправить текст, отправить изображение, спросить у пользователя имя и т.д.
        </p>
        <div class="workspace">
          <BlockList
            v-if="!isBlocksLoading"
            :blocks="blocks"
            @upload-image="handleUploadImageEvent"
            @update-block="handleUpdateBlockEvent"
            @delete-block="handleDeleteBlockEvent"
            class="block-list"
          />
          <div class="block-types-column">
            <p class="hint">Чтобы добавить блок, нажмите на него</p>
            <BlockTypeList
              :blockTypes="blockTypes"
              @add-block="handleAddBlockEvent"
            />
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.page__header {
  margin: 40px 0px 28px 0px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header__title {
  font-size: 32px;
  line-height: 40px;
}

.add-block-btn {
  display: none
}

.page__hint {
  font-size: 16px;
  font-weight: 500;
  line-height: 28px;
  letter-spacing: 0.75px;
  color: var(--body-text);
  margin-bottom: 28px;
}

.workspace {
  display: flex;
  justify-content: space-between;
  gap: 64px;
}

.block-list {
  display: flex;
  flex-direction: column;
  width: 972px;
}

.block-types-column {
  width: 196px;
}

.hint {
  font-size: 16px;
  font-weight: 400;
  color: var(--body-text);
  letter-spacing: 0.75px;
  margin-bottom: 12px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .page__header {
    margin: 28px 0px 20px 0px;
  }

  .header__title {
    font-size: 24px;
    line-height: 28px;
  }

  .page__hint {
    font-size: 14px;
    line-height: 18px;
    margin-bottom: 20px;
  }

  .add-block-btn {
    display: block;
  }
  .block-types-column {
    display: none;
  }
}

@media (max-width: 767px) {
  .page__header {
    margin: 18px 0px 12px 0px;
  }

  .header__title {
    font-size: 16px;
    line-height: 20px;
  }

  .page__hint {
    font-size: 8px;
    line-height: 10px;
    letter-spacing: 0px;
    margin-bottom: 12px;
    width: 100%;
  }

  .add-block-btn {
    display: block;
  }
  .block-types-column {
    display: none;
  }
}
</style>