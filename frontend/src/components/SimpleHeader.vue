<script setup>
</script>

<template>
  <header>
    <div class="container">
      <div class="header">
        <div class="header__logo" @click="$router.push('/')">
          <img src="@/assets/icons/logo.svg" class="logo__img">
          <p class="logo__text">
            <span style="color: var(--primary-dark)">Free</span>Bots
          </p>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  padding: 20px 0;
}

.header__logo {
  display: flex;
  align-items: center;
  gap: 12px;
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

@media (max-width: 767px) {
  .header__logo {
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