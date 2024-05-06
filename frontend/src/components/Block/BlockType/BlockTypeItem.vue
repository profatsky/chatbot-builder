<script setup>
const props = defineProps({
  blockType: {
    type: Object,
    required: true,
  }
});

const emits = defineEmits(['add-block']);

const addBlockEvent = () => {
  emits('add-block', props.blockType);
};

</script>

<template>
  <div class="block-type" @click="addBlockEvent">
    <slot name="type-img"></slot>
    <slot name="type-name"></slot>
  </div>
</template>

<style scoped>
.block-type {
  font-size: 16px;
  letter-spacing: 0.75px;
  font-weight: 500;
  color: var(--body-text);

  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
  
  padding: 16px 20px 20px 20px;
  border-radius: 16px;
  background-color: var(--light-gray);
  box-shadow: 0 0 16px 0 rgba(17, 17, 17, 0.04);

  cursor: pointer;
}

.block-type img {
  width: 32px;
  height: 32px;
}
</style>