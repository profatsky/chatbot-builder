<script setup>
import AppButton from '@/components/UI/AppButton.vue';
</script>

<template>
  <header>
    <div class="container">
      <nav class="header-navbar">
        <div class="header-navbar__logo">
          <img src="@/assets/logo.png">
        </div>
        <div class="header-navbar__menu">
          <ul>
            <li><a href="#">Возможности</a></li>
            <li><a href="#">Руководство</a></li>
            <li><a href="#">Поддержка</a></li>
          </ul>
        </div>
        <div class="header-navbar__auth">
          <a href="#">Вход</a>
          <AppButton size="medium" importance="secondary">Регистрация</AppButton>
        </div>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header-navbar {
  display: flex;
  padding: 20px 0;
  align-items: center;
}

.header-navbar__menu {
  flex-grow: 1;
}

.header-navbar__menu ul {
  list-style: none;
  font-weight: 400;
  display: flex;
  justify-content: center;
  gap: 64px;
  padding: 0 64px;
}

.header-navbar__auth {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: center;
}
</style>