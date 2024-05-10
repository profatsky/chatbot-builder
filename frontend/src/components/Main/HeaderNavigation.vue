<script setup>
const emits = defineEmits(['open-register-form', 'open-login-form'])
const openRegisterForm = () => {
  emits('open-register-form');
};
const openLoginForm = () => {
  emits('open-login-form');
};
</script>

<template>
  <header>
    <div class="container">
      <nav class="header-navbar">
        <div class="header-navbar__logo">
          <img src="@/assets/logo.png">
        </div>
        <div class="header-navbar__menu">
          <ul class="header-navbar__menu-list">
            <li><a href="#advantages-section">Возможности</a></li>
            <li><a href="#manual-section">Руководство</a></li>
            <li><a href="#support-section">Поддержка</a></li>
          </ul>
        </div>
        <div class="header-navbar__auth">
          <button 
            @click="openLoginForm"
            class="login-btn"
          >
            Вход
          </button>
          <AppButton 
            size="medium" 
            importance="secondary"
            @click="openRegisterForm"
          >
            Регистрация
          </AppButton>
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

.header-navbar__menu-list {
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

.login-btn {
  background: none;
  font-size: 16px;
}

@media (max-width: 768px) {
  .header-navbar__menu-list {
    display: none;
  }
}
</style>