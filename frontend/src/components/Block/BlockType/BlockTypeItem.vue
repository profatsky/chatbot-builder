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

<style>
.block-type {
  font-size: 16px;
  font-weight: 500;
  line-height: 20px;
  letter-spacing: 0.75px;
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

@media (min-width: 768px) and (max-width: 1169px) {
  .block-type {
    font-size: 16px;
    line-height: 20px;
    gap: 6px;
    padding: 12px 16px 16px 16px;
    border-radius: 12px;
  }

  .block-type img {
    width: 28px;
    height: 28px;
  }
}

@media (max-width: 767px) {
  .block-type {
    font-size: 12px;
    line-height: 16px;
    gap: 4px;
    padding: 10px 14px 14px 14px;
    border-radius: 8px;
  }

  .block-type img {
    width: 24px;
    height: 24px;
  }
}
</style>