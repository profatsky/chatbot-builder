<script>
export default {
  props: {
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
  },
  computed: {
    computedClasses() {
      return {
        "btn": true,
        "btn-primary": this.importance === "primary",
        "btn-secondary": this.importance === "secondary",
        "btn-small": this.size === "small",
        "btn-medium": this.size === "medium",
        "btn-large": this.size === "large",
      }
    }
  }
}
</script>

<template>
  <button :class="computedClasses">
    <slot></slot>
  </button>
</template>


<style scoped>
.btn {
  font-weight: 600;
  border-radius: 40px;
}

.btn-primary {
  background-color: var(--primary);
  color: var(--main-white);
}

.btn-secondary {
  background: none;
  color: var(--primary);
  border: 2px solid var(--primary);
}

.btn-large {
  height: 64px;
  min-width: 200px;

  font-size: 16px;
  line-height: 28px;
  letter-spacing: 0.75px;

  padding: 18px;
}

.btn-medium {
  height: 56px;
  min-width: 200px;

  font-size: 16px;
  line-height: 28px;
  letter-spacing: 0.75px;

  padding: 14px;
}

.btn-small {
  height: 40px;
  min-width: 120px;

  font-size: 14px;
  line-height: 24px;
  letter-spacing: 0.75px;

  padding: 14px;
}
</style>