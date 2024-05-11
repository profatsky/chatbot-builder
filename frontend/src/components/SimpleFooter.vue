<script>
</script>

<template>
  <footer>
    <div class="container">
      <div class="footer">
        <div class="footer__logo">
          <img src="@/assets/icons/logo/full-logo.svg">
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

@media (max-width: 768px) {
  .footer {
    gap: 40px;
  }
}
</style>