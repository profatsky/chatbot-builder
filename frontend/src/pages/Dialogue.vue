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
import { getBlocks, createBlock } from '@/api/blocks';

const blockTypes = ref([
  { value: 'textBlock', name: 'Текст', imgPath: msgPurpleIcon },
  { value: 'imageBlock', name: 'Изображение', imgPath: imgPurpleIcon },
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
    console.log("response", responseData)
  }
};

const handleUpdateBlockEvent = (block) => {
  blocks.value[block.sequence_number - 1] = block;
};

const handleDeleteBlockEvent = (block) => {
  blocks.value = blocks.value.filter(
    b => b.sequence_number !== block.sequence_number
  );
  // blocks.value.forEach((obj, index) => {
  //   obj.sequence_number = index + 1;
  // });
}

onMounted(async () => {
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
    console.log(blocks.value)
  }
});

</script>

<template>
  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="page-content">
        <div class="page-header">
          <h1 class="content__title">Диалоги</h1>
          <AppButton
            size="large"
            importance="secondary"
          >
            Сохранить
          </AppButton>
        </div>
        <div class="workspace">
          <div class="dialogue">
            <BlockList
              v-if="!isBlocksLoading"
              :blocks="blocks"
              @update-block="handleUpdateBlockEvent"
              @delete-block="handleDeleteBlockEvent"
            />
          </div>
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
  justify-content: flex-end;
  gap: 64px;
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