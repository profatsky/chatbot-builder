<script setup>
import BlockTypeItem from '@/components/Block/BlockType/BlockTypeItem.vue';

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
  width: 198px;

  display: flex;
  flex-direction: column;
  gap: 24px;

  margin: 0 auto;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .block-types {
    gap: 20px;
  }
}

@media (max-width: 767px) { 
  .block-types {
    width: 160px;
    gap: 16px;
  }
}
</style>