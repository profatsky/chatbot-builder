<script setup>
import BlockTypeList from '@/components/Block/BlockType/BlockTypeList.vue';

const props = defineProps({
  blockTypes: {
    type: Array,
    required: true,
  }
});

const emits = defineEmits(['add-block']);
const handleAddBlockEvent = (blockType) => {
  emits('add-block', blockType);
};
</script>

<template>
  <div class="block-addition">
    <h2 class="block-addition__title">Добавление блока</h2>
    <p class="block-addition__hint">Чтобы добавить блок, нажмите на него</p>
    <BlockTypeList
      :blockTypes="blockTypes"
      @add-block="handleAddBlockEvent"
    />
  </div>
</template>

<style scoped>
.block-addition {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .block-addition {
    width: 280px;
    gap: 16px;
  }

  .block-addition__title {
    font-size: 24px;
    line-height: 28px;
    margin-bottom: 6px;
  }

  .block-addition__hint {
    font-size: 16px;
    line-height: 18px;
  }
}

@media (max-width: 767px) { 
  .block-addition {
    width: 200px;
    gap: 8px
  }

  .block-addition__title {
    font-size: 16px;
    line-height: 20px;
    margin-bottom: 4px;
  }

  .block-addition__hint {
    font-size: 12px;
    line-height: 16px;
  }
}
</style>