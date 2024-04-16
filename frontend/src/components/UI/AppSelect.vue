<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
  },
  options: {
    type: Array,
    default: () => []
  },
  size: {
    type: String,
    default: 'small',
    validator: (value) => ['small', 'medium', 'large'].includes(value),
  }
});

const selectedOption = ref(props.modelValue);

const emits = defineEmits(['update:modelValue']);

const changeOption = (event) => {
  emits('update:modelValue', event.target.value)
};

const computedClasses = computed(() => ({
  "select": true,
  "select-small": props.size == 'small',
  "select-medium": props.size == 'medium',
}));
</script>

<template>
  <select @change="changeOption" :class="computedClasses" v-model="selectedOption">
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
  font-family: 'Montserrat';
  color: var(--main-black);

  background-color: var(--main-white);
  min-width: 200px;
  border: 0;
  border-radius: 10px;
  appearance: none;
}

.select-small {
  font-size: 16px;
  letter-spacing: 0.75px;
  line-height: 28px;

  padding: 6px 60px 6px 24px;
  border-radius: 10px;
}

.select-medium {
  font-size: 16px;
  letter-spacing: 0.75px;
  line-height: 28px;

  padding: 14px 60px 14px 24px;
  border-radius: 16px;
}

.select:not([multiple]) {
  background-repeat: no-repeat;
  background-position-y: calc(50%);
  background-position-x: calc(100% - 24px);
  background-image: url('src/assets/select-arrow.svg');
  background-size: 0.85em auto;
}
select::-ms-expand {
  display: none;
}
</style>