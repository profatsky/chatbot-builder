<script>
export default {
  props: {
    modelValue: [String, Number]
  },
  methods: {
    updateInput(event) {
      this.$emit('update:modelValue', event.target.value)
    }
  }
}
</script>

<template>
  <input 
    :value="modelValue"
    @input="updateInput"
    class="input"
  >
</template>


<style>
.input {
  background-color: var(--main-white);
  border-radius: 16px;
  border: 0;
  padding: 14px 24px;

  font-family: 'Montserrat', 'sans-serif';
  font-size: 16px;
  line-height: 28px;
  letter-spacing: 0.75px;
  color: var(--body-text);
}

input::-webkit-input-placeholder {
  color: var(--placeholder); 
}
</style>