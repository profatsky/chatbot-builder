<script setup>
import { ref, onBeforeMount, onBeforeUpdate } from 'vue';
import BlockItem from '@/components/Dialogues/BlockItem.vue';

const props = defineProps({
  blocks: {
    type: Array,
    required: true,
  }
});

const questionBlockNumbers = ref([]);

const numberQuestionBlocks = () => {
  const qustionBlocksLength = props.blocks.filter(block => block.type === 'question_block').length;
  questionBlockNumbers.value = Array.from({ length: qustionBlocksLength }, (_, index) => index + 1);
};

const getQuestionBlockCounter = (block) => {
  if (block.type !== 'question_block') {
    return 0;
  }
  return questionBlockNumbers.value.shift();
};

const emits = defineEmits(['update-block', 'delete-block', 'upload-image']);

const updateBlockEvent = (block) => {
  emits('update-block', block)
};

const deleteBlockEvent = (block) => {
  emits('delete-block', block)
};

const uploadImageEvent = (block, formData) => {
  emits('upload-image', block, formData)
};

onBeforeUpdate(() => { numberQuestionBlocks() });

onBeforeMount(() => { numberQuestionBlocks() });
</script>

<template>
  <div v-if="blocks.length > 0">
    <BlockItem
      v-for="block in blocks"
      :key="block.block_id"
      :block="block"
      :question-counter="getQuestionBlockCounter(block)"
      @upload-image="uploadImageEvent"
      @update-block="updateBlockEvent"
      @delete-block="deleteBlockEvent"
    />
  </div>
  <div v-else class="block-list__hint">
    <p>В этом диалоге нет блоков</p>
  </div>
</template>

<style scoped>
.block-list__hint {
  font-size: 24px;
  align-items: center;
}
</style>