<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    required: true
  },
});

const emits = defineEmits(['update:modelValue']);

function updateTextarea(event) {
  emits('update:modelValue', event.target.value)
}
</script>

<template>
  <textarea
    :value="modelValue"
    @input="updateTextarea"
    class="textarea"
  >
  </textarea>
</template>

<style scoped>
.textarea {
  background-color: var(--main-white);
  border-radius: 16px;
  border: 0;
  padding: 14px 24px;

  font-family: 'Montserrat';
  font-size: 16px;
  line-height: 28px;
  letter-spacing: 0.75px;
  color: var(--body-text);
}
</style>