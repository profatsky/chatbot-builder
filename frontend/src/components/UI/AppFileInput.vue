<script setup>
import { computed } from 'vue';

const props = defineProps({
  size: {
    type: String,
    default: "medium",
    validator: (value) => ["small", "medium", "large"].includes(value),
  },
  importance: {
    type: String,
    default: "primary",
    validator: (value) => ["primary", "secondary"].includes(value),
  }
});

const computedClasses = computed(() => ({
  "input": true,
  "input-primary": props.importance === "primary",
  "input-secondary": props.importance === "secondary",
  "input-small": props.size === "small",
  "input-medium": props.size === "medium",
  "input-large": props.size === "large",
}));

const emits = defineEmits(['upload-file']);

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    emits('upload-file', file);
  }
};
</script>

<template>
  <label>
    <span :class="computedClasses"><slot></slot></span>
    <input type="file" @change="handleFileChange"/>
  </label>
</template>


<style scoped>
input[type="file"] {
  display: none
}

.input {
  font-weight: 600;
  border-radius: 40px;
  transition: background-color 0.3s, color 0.3s;
  display: block;
  cursor: pointer;
  text-align: center;
}

.input-primary {
  background-color: var(--primary);
  color: var(--main-white);
}

.input-primary:hover {
  background-color: var(--primary-dark);
}

.input-primary:active {
  background-color: var(--main-black);
}

.input-secondary {
  background: none;
  color: var(--primary);
  border: 2px solid var(--primary);
}

.input-secondary:hover {
  border-color: var(--primary-dark);
  color: var(--primary-dark);
}

.input-secondary:active {
  border-color: var(--main-black);
  color: var(--main-black);
}

.input-large {
  min-width: 200px;

  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.75px;

  padding: 18px;
}

.input-medium {
  min-width: 200px;

  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.75px;

  padding: 14px;
}

.input-small {
  min-width: 200px;

  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.75px;

  padding: 8px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .input-small {
    font-size: 12px;
    line-height: 20px;
    padding: 6px 12px;
  }
}
</style>