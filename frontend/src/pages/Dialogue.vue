<script setup>
import { ref } from 'vue';
import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import BlockList from '@/components/Dialogues/BlockList.vue';
import BlockTypeList from '@/components/Dialogues/BlockTypeList.vue';
import emptyBlocks from '@/components/Dialogues/blocks'

const blockTypes = ref([
  { value: 'textBlock', name: 'Текст', imgPath: '/src/assets/icons/blocks/msg-purple.svg' },
  { value: 'imageBlock', name: 'Изображение', imgPath: '/src/assets/icons/blocks/img-purple.svg' },
]);
// const isBlocksLoading = ref(false);

const blocks = ref([]);

const handleAddBlockEvent = (blockType) => {
  const newBlock = { ...emptyBlocks[blockType.value] };
  newBlock.sequence_number = blocks.value.length + 1;
  blocks.value.push(newBlock);
  console.log(blocks)
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