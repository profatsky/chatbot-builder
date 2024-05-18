<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true,
    validator: (value) => ['error', 'success', 'primary'].includes(value)
  },
});

const computedClasses = computed(() => ({
  'notification': true,
  'success': props.status === 'success',
  'error': props.status === 'error',
  'primary': props.status === 'primary',
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
  padding: 20px 24px;
  width: 685px;
}

.notification__title {
  font-size: 16px;
  letter-spacing: 0.25px;
  line-height: 20px;
  font-weight: 600;
  margin-bottom: 16px;
}

.success {
  background-color: var(--success-light);
  border: 2px solid var(--success);
}

.success .notification__title {
  color: var(--success-dark);
}

.error {
  background-color: var(--error-light);
  border: 2px solid var(--error);
}

.error .notification__title {
  color: var(--error-dark);
}

.primary {
  background-color: var(--main-white);
  border: 2px solid var(--primary);
}

.primary .notification__title {
  color: var(--primary-dark);
}

.notification__description {
  font-size: 16px;
  letter-spacing: 0.75px;
  line-height: 24px;
}

@media (max-width: 768px) {
  .notification {
    padding: 16px 20px;
    width: 590px;
  }

  .notification__title {
    font-size: 14px;
    margin-bottom: 8px;
  }

  .notification__description {
    font-size: 14px;
    line-height: 20px;
  }
}

</style>