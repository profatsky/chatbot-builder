<script>
export default {
  methods: {
    closeModal() {
      this.$emit('closeModal');
    }
  }
}
</script>

<template>
  <div class="modal">
    <div class="modal__content">
      <button 
        @click="closeModal" 
        class="close-button"
      >
        <img src="@/assets/icons/close.svg">
      </button>
      <div class="slot">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<style>
.modal {
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.3);
  position: fixed;
  display: flex;
}

.modal__content {
  margin: auto;
  background-color: var(--main-white);
  border-radius: 24px;
  min-height: 58px;
  min-width: 300px;
  padding: 20px;
}

.close-button {
  background-color: var(--main-white);
  float: right;
  padding: 8px;
}

.slot {
  margin-bottom: 20px;
}
</style>