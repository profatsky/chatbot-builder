<script setup>
import BlockItem from '@/components/Dialogues/BlockItem.vue';

const props = defineProps({
  blocks: {
    type: Array,
    required: true,
  }
});

const emits = defineEmits(['update-block', 'delete-block']);

const updateBlockEvent = (block) => {
  emits('update-block', block)
};

const deleteBlockEvent = (block) => {
  emits('delete-block', block)
};

</script>

<template>
  <div v-if="blocks.length > 0">
    <BlockItem
      v-for="block in blocks"
      :key="block.block_id"
      :block="block"
      @update-block="updateBlockEvent"
      @delete-block="deleteBlockEvent"
    />
  </div>
  <div v-else class="block-list__clue">
    <p>В этом диалоге нет блоков</p>
  </div>
</template>

<style scoped>
.block-list__clue {
  font-size: 24px;
  align-items: center;
}
</style>