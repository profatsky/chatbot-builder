<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { collapsed } from '@/components/Sidebar/sidebarUtils.js';

const props = defineProps({
  to: {
    type: String,
    required: true
  },
  iconPath: {
    type: String,
    required: true
  }
});

const route = useRoute();
const isActive = computed(() => route.path === props.to)

</script>

<template name="fade">
  <router-link :to="to" class="link" :class="{ active: isActive }">
    <img :src="props.iconPath">
    <transition name="fade">
      <div v-if="!collapsed">
        <slot></slot>
      </div>
    </transition>
  </router-link>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.link {
  display: flex;
  align-items: center;
  gap: 12px;

  font-size: 20px;
  letter-spacing: 0.75px;
  line-height: 34px;
  font-weight: 600;
  color: var(--body-text);

  padding: 24px 32px;
  height: 34px;
}

.link:hover {
  background-color: var(--light-gray);
}

@media (max-width: 768px) {
  .link {
    gap: 10px;

    font-size: 16px;
    line-height: 28px;

    padding: 16px 22px;
    height: 28px;
  }
}
</style>