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
          <img src="@/assets/icons/logo.svg" class="logo__img">
          <p class="logo__text">
            <span style="color: var(--primary-dark)">Free</span>Bots
          </p>
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

.header-navbar__logo {
  display: flex;
  align-items: center;
  gap: 12px;
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
  line-height: 24px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .header-navbar__menu-list {
    display: none;
  }
}

@media (max-width: 767px) {
  .header-navbar__menu-list {
    display: none;
  }
  
  .header-navbar__auth {
    display: none;
  }

  .header-navbar__logo {
    gap: 8px;
  }

  .logo__img {
    height: 28px;
  }

  .logo__text {
    font-size: 18px;
  }
}
</style>