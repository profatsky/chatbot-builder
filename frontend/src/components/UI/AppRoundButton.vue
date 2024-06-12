<script setup>
import { computed } from 'vue';

const props = defineProps({
  buttonType: {
    type: String,
    default: 'redirect',
    validator: (value) => ['redirect', 'delete'].includes(value),
  }
});

const computedClasses = computed(() => ({
  "btn": true,
  "btn-redirect": props.buttonType === 'redirect',
  "btn-delete": props.buttonType === 'delete',
}));
</script>

<template>
  <button :class="computedClasses">
    <img v-if="buttonType === 'redirect'" src="@/assets/button-arrow.svg">
    <img v-else-if="buttonType === 'delete'" src="@/assets/button-delete.svg">
  </button>
</template>

<style scoped>
.btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-redirect {
  background-color: var(--primary);
}

.btn-delete{
  background-color: var(--error-dark);
}

@media (min-width: 768px) and (max-width: 1169px) { 
  .btn {
    width: 32px;
    height: 32px;
  }
}

@media (max-width: 767px) {
  .btn {
    width: 16px;
    height: 16px;
  }
}
</style>