<script>
</script>

<template>
  <footer>
    <div class="container">
      <div class="footer">
        <div class="footer__logo">
          <img src="@/assets/icons/logo/simple-logo.svg" class="logo__img">
          <p class="logo__text">
            <span style="color: var(--primary-dark)">Bot</span>Builder
          </p>
        </div>
        <div class="footer__description">
          <p>developed by profatsky</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  display: flex;
  padding: 20px 0;
  gap: 271px;
  align-items: center;
}

.footer__logo {
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

.footer__description {
  font-size: 16px;
}

@media (max-width: 768px) {
  .footer {
    gap: 40px;
  }
}

@media (max-width: 320px) {
  .footer {
    flex-direction: column;
    gap: 12px;
  }

  .footer__logo {
    gap: 8px;
  }

  .logo__img {
    height: 28px;
  }

  .logo__text {
    font-size: 18px;
  }

  .footer__description {
    font-size: 12px;
  }
}
</style>