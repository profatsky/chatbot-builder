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
  <div class="modal__wrapper">
    <div class="modal">
      <button 
        @click="closeModal" 
        class="modal__close-btn"
      >
        <img src="@/assets/icons/close.svg">
      </button>
      <div class="modal__content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal__wrapper {
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.3);
  position: fixed;
  display: flex;
}

.modal {
  margin: auto;
  background-color: var(--main-white);
  border-radius: 16px;
  padding: 28px;
}

.modal__close-btn {
  background-color: var(--main-white);
  float: right;
}

.modal__close-btn img {
  width: 18px;
  height: 18px;
}

.modal__content {
  margin: 18px 0px;
  padding: 24px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .modal {
    border-radius: 12px;
    padding: 20px;
  }

  .modal__close-btn img {
    width: 14px;
    height: 14px;
  }

  .modal__content {
    margin: 14px 0px;
    padding: 16px;
  }
}

@media (max-width: 767px) {
  .modal {
    border-radius: 8px;
    padding: 16px;
  }

  .modal__close-btn img {
    width: 10px;
    height: 10px;
  }

  .modal__content {
    margin: 10px 0px;
    padding: 12px;
  }
}
</style>