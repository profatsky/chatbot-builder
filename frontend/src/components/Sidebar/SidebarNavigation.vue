<script setup>
import { collapsed, toggleSidebar, sidebarWidth } from '@/components/utils/sidebarCollapse';
import SidebarLink from '@/components/Sidebar/SidebarLink.vue';

</script>

<template>
  <div class="sidebar" :style="{ width: sidebarWidth }">

    <div>
      <div v-if="collapsed">
        <img src="@/assets/icons/logo-icon.png" class="logo">
      </div>
      <div v-else>
        <transition name="logo">
          <img src="@/assets/logo.png" class="logo">
        </transition>
      </div>
    </div>
    <SidebarLink to="/projects" iconPath="/src/assets/icons/bot-gray.svg">Боты</SidebarLink>
    <SidebarLink to="/" iconPath="/src/assets/icons/layout-gray.svg">Шаблоны</SidebarLink>
    <SidebarLink to="/" iconPath="/src/assets/icons/blocks-gray.svg">Плагины</SidebarLink>
    <SidebarLink to="/" iconPath="/src/assets/icons/scroll-gray.svg">Руководство</SidebarLink>
    <SidebarLink to="/profile" iconPath="/src/assets/icons/profile-gray.svg">Профиль</SidebarLink>
    <span
      class="collapse-icon"
      :class="{ 'rotate-180': collapsed }"
      @click="toggleSidebar"
    >
      <img src="@/assets/icons/arrows.svg">
    </span>
  </div>
</template>

<style>
.logo-enter-active,
.logo-leave-active {
  transition: opacity 0.3s;
}

.logo-enter-from,
.logo-leave-to {
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
  margin: 48px 0px 28px 24px;
}

.collapse-icon {
  position: absolute;
  bottom: 0;
  padding: 32px;

  transition: 0.2s linear;
}

.rotate-180 {
  transform: rotate(180deg);
  transition: 0.2s linear;
}
</style>