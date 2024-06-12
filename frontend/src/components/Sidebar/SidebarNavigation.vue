<script setup>
import { onMounted, onUnmounted } from 'vue';
import { collapsed, toggleSidebar, sidebarWidth, resizeSidebar } from '@/components/Sidebar/sidebarUtils';
import SidebarLink from '@/components/Sidebar/SidebarLink.vue';

import botGrayIcon from '@/assets/icons/bot-gray.svg';
import layoutGrayIcon from '@/assets/icons/layout-gray.svg';
import blockGrayIcon from '@/assets/icons/blocks-gray.svg';
import scrollGrayIcon from '@/assets/icons/scroll-gray.svg';
import profileGrayIcon from '@/assets/icons/profile-gray.svg';

onMounted(() => {
  window.addEventListener('resize', resizeSidebar);
});

onUnmounted(() => {
  window.removeEventListener('resize', resizeSidebar);
});
</script>

<template>
  <div class="sidebar" :style="{ width: sidebarWidth }">

    <div class="logo" @click="$router.push('/')">
      <img src="@/assets/icons/logo.svg" class="logo__img">
      <Transition name="logo-text">
        <p v-if="!collapsed" class="logo__text">
          <span style="color: var(--primary-dark)">Free</span>Bots
        </p>
      </Transition>
    </div>
    <SidebarLink to="/projects" :iconPath="botGrayIcon">Боты</SidebarLink>
    <SidebarLink to="/templates" :iconPath="layoutGrayIcon">Шаблоны</SidebarLink>
    <SidebarLink to="/plugins" :iconPath="blockGrayIcon">Плагины</SidebarLink>
    <SidebarLink to="/manual" :iconPath="scrollGrayIcon">Руководство</SidebarLink>
    <SidebarLink to="/profile" :iconPath="profileGrayIcon">Профиль</SidebarLink>
    <span
      class="collapse-icon"
      :class="{ 'rotate-180': collapsed }"
      @click="toggleSidebar"
    >
      <img src="@/assets/icons/arrows.svg">
    </span>
  </div>
</template>

<style scoped>
.logo-text-enter-active,
.logo-text-leave-active {
  transition: opacity 0.2s;
}

.logo-text-enter-from,
.logo-text-leave-to {
  opacity: 0;
}

.sidebar {
  color: var(--body-text);
  background-color: var(--main-white);
  box-shadow: 0 0 16px 0 rgba(17, 17, 17, 0.04);

  float: left;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  bottom: 0;

  transition: 0.3s ease;

  display: flex;
  flex-direction: column;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 36px 0px 28px 28px;
  cursor: pointer;
}

.logo__img {
  height: 50px;
}

.logo__text {
  font-size: 32px;
  font-weight: 600;
  color: var(--primary);
  font-family: 'Roboto', 'sans-serif';
}

.collapse-icon {
  position: absolute;
  bottom: 0;
  padding: 32px;

  transition: 0.2s linear;
}

.collapse-icon img {
  height: 32px;
}

.rotate-180 {
  transform: rotate(180deg);
  transition: 0.2s linear;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .logo {
    margin: 28px 0px 18px 18px;
  }

  .logo__img {
    height: 36px;
  }
  
  .logo__text {
    font-size: 24px;
  }

  .collapse-icon {
    padding: 22px;
  }

  .collapse-icon img {
    height: 28px;
  }
}

@media (max-width: 767px) {
  .logo {
    margin: 18px 0px 16px 8px;
    gap: 8px;
  }

  .logo__img {
    height: 28px;
  }

  .logo__text {
    font-size: 18px;
    line-height: 20px;
  }

  .collapse-icon {
    padding: 10px;
  }

  .collapse-icon img {
    height: 24px;
  }
}
</style>