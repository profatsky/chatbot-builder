<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true,
    validator: (value) => ['error', 'success'].includes(value)
  },
});

const computedClasses = computed(() => ({
  'notification': true,
  'success': props.status === 'success',
  'error': props.status === 'error',
}));

</script>

<template>
  <div :class="computedClasses">
    <div class="notification__title">
      <slot name="title"></slot>
    </div>
    <div class="notification__description">
      <slot name="description"></slot>
    </div>
  </div>
</template>

<style scoped>

.notification {
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
  border-radius: 16px;
  padding: 24px 20px;
  width: 685px;
}

.success {
  background-color: var(--success-light);
  border: 2px solid var(--success);
}

.success .notification__title {
  color: var(--success-dark);
  font-size: 14px;
  letter-spacing: 0.25px;
  line-height: 16px;
  font-weight: 600;
}

.error {
  background-color: var(--error-light);
  border: 2px solid var(--error);
}

.error .notification__title {
  color: var(--error-dark);
  font-size: 14px;
  letter-spacing: 0.25px;
  line-height: 16px;
  font-weight: 600;
}

.notification__description {
  font-size: 16px;
  letter-spacing: 0.75px;
  line-height: 28px;
}
</style>