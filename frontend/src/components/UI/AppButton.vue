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


<style>
.btn {
  font-weight: 600;
  border-radius: 40px;
  transition: background-color 0.3s, color 0.3s;
}

.btn-primary {
  background-color: var(--primary);
  color: var(--main-white);
}

.btn-primary:hover {
  background-color: var(--primary-dark);
}

.btn-primary:active {
  background-color: var(--main-black);
}

.btn-secondary {
  background: none;
  color: var(--primary);
  border: 2px solid var(--primary);
}

.btn-secondary:hover {
  border-color: var(--primary-dark);
  color: var(--primary-dark);
}

.btn-secondary:active {
  border-color: var(--main-black);
  color: var(--main-black);
}

.btn-large {
  height: 64px;
  min-width: 200px;

  font-size: 16px;
  letter-spacing: 0.75px;

  padding: 18px;
}

.btn-medium {
  height: 56px;
  min-width: 200px;

  font-size: 16px;
  letter-spacing: 0.75px;

  padding: 14px;
}

.btn-small {
  height: 40px;
  min-width: 200px;

  font-size: 14px;
  letter-spacing: 0.75px;

  padding: 8px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .btn-large {
    height: 48px;
    padding: 8px 16px;
  }

  .btn-medium {
    height: 40px;
    padding: 8px 16px;
  }

  .btn-small {
    height: 28px;
    padding: 2px 16px;
  }
}

@media (max-width: 767px) {
  .btn-large {
    height: 40px;
    font-size: 12px;
    padding: 6px 16px;
    min-width: 100px;
  }

  .btn-medium {
    height: 36px;
    font-size: 12px;
    padding: 8px 16px;
    min-width: 100px;
  }

  .btn-small {
    height: 18px;
    font-size: 8px;
    line-height: 10px;
    padding: 0;
    min-width: 100px;
  }
}
</style>