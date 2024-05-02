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
  <div v-if="blocks.length > 0"  class="blocks-list">
    <BlockItem
      v-for="block in blocks"
      :key="block.block_id"
      :block="block"
      @update-block="updateBlockEvent"
      @delete-block="deleteBlockEvent"
    />
  </div>
</template>

<style scoped>
</style>