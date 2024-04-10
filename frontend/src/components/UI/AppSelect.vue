<script setup>
import { ref } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
  },
  options: {
    type: Array,
    default: () => []
  }
});

const selectedOption = ref(props.modelValue);

const emits = defineEmits(['update:modelValue']);

function changeOption(event) {
  emits('update:modelValue', event.target.value)
}
</script>

<template>
  <select @change="changeOption" class="select" v-model="selectedOption">
    <option 
      v-for="(option, index) in options" 
      :key="index"
      :value="option.value"
    >
      {{ option.label }}
    </option>
  </select>
</template>

<style scoped>
.select {
  padding: 6px 60px 6px 24px;
  border: 0;
  border-radius: 10px;
  appearance: none;

  font-size: 16px;
  color: var(--main-black);
  letter-spacing: 0.75px;
  line-height: 28px;
}

.select:not([multiple]) {
  background-repeat: no-repeat;
  background-position-y: calc(100% - 18px);
  background-position-x: calc(100% - 24px);
  background-image: url('src/assets/select-arrow.svg');
  background-size: 0.85em auto;
}
select::-ms-expand {
  display: none;
}
</style>