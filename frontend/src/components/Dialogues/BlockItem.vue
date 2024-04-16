<script setup>
import { ref, shallowRef } from 'vue';
import TextBlockItem from '@/components/Dialogues/TextBlockItem.vue';

const props = defineProps({
  block: {
    type: Object,
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

const currentComponent = shallowRef(null);

switch (props.block.type) {
  case 'text_block':
    currentComponent.value = TextBlockItem;
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
    class="block"
    @update-block="updateBlockEvent"
    @delete-block="deleteBlockEvent"

  />
</template>

<style scoped>
.block {
  margin-bottom: 28px;
  box-shadow: 0 0 16px 0 rgba(17, 17, 17, 0.04);
}
</style>