<script setup>
import BlockTypeItem from '@/components/Dialogues/BlockTypeItem.vue';

const props = defineProps({
  blockTypes: {
    type: Array,
    required: true,
  }
});

const emits = defineEmits(['add-block']);

const addBlockEvent = (blockType) => {
  emits('add-block', blockType);
};
</script>

<template>
  <div v-if="blockTypes.length > 0" class="block-types">
    <BlockTypeItem
      v-for="blockType in blockTypes"
      :key="blockType.id"
      :blockType="blockType"
      @add-block="addBlockEvent"
    >
      <template v-slot:type-img>
        <img :src="blockType.imgPath">
      </template>
      <template v-slot:type-name>
        <div>{{ blockType.name }}</div>
      </template>
    </BlockTypeItem>
  </div>
</template>

<style scoped>
.block-types {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>