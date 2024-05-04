<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toast-notification';

import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import BlockList from '@/components/Dialogues/BlockList.vue';
import BlockTypeList from '@/components/Dialogues/BlockTypeList.vue';
import emptyBlocks from '@/components/Dialogues/blocks'
import msgPurpleIcon from '@/assets/icons/blocks/msg-purple.svg';
import imgPurpleIcon from '@/assets/icons/blocks/img-purple.svg';
import questionPurpleIcon from '@/assets/icons/blocks/question-purple.svg';
import csvPurpleIcon from '@/assets/icons/blocks/csv-purple.svg';
import emailPurpleIcon from '@/assets/icons/blocks/email-purple.svg';
import requestPurpleIcon from '@/assets/icons/blocks/request-purple.svg';
import { getBlocks, createBlock, updateBlock, deleteBlock } from '@/api/blocks';

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

const blocks = ref([]);

const isBlocksLoading = ref(true);

const handleAddBlockEvent = async (blockType) => {
  const newBlock = { ...emptyBlocks[blockType.value] };
  newBlock.sequence_number = blocks.value.length + 1;

  const { response, error } = await createBlock(
    route.params.projectId,
    route.params.dialogueId,
    newBlock
  );
  if (error.value) {
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
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
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
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
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    await getBlocksFromApi();
    toast.success('Блок успешно удален')
  }
}

const getBlocksFromApi = async () => {
  const { response, error } = await getBlocks(
    route.params.projectId,
    route.params.dialogueId
  );

  if (error.value) {
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    isBlocksLoading.value = false;
    const responseData = response.value.data;
    blocks.value = responseData;
    console.log(blocks.value);
  }
};

onMounted(async () => { await getBlocksFromApi() });
</script>

<template>
  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="page-content">
        <div class="page-header">
          <h1 class="content__title">Диалог</h1>
        </div>
        <div class="workspace">
          <BlockList
            v-if="!isBlocksLoading"
            :blocks="blocks"
            @update-block="handleUpdateBlockEvent"
            @delete-block="handleDeleteBlockEvent"
            class="block-list"
          />
          <div class="block-types">
            <p class="clue">Чтобы добавить блок, нажмите на него</p>
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
.page-content {
  margin-left: 120px;
}

.page-header {
  margin: 48px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.block-types {
  width: 198px;
  display: flex;
  flex-direction: column;
}

.clue {
  font-size: 16px;
  font-weight: 400;
  color: var(--body-text);
  letter-spacing: 0.75px;
  margin-bottom: 12px;
}
</style>