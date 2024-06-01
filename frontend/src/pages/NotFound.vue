<script setup>
import SimpleHeader from '@/components/SimpleHeader.vue';
</script>

<template>
  <SimpleHeader/>
  <main>
    <div class="container">
      <div class="content">
        <h2>Ничего не найдено</h2>
        <AppButton
          size="large"
          importance="secondary"
          @click="$router.push('/')"
        >
          Главная страница
        </AppButton>
      </div>
    </div>
  </main>
</template>

<style>
.content {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 36px;
  margin-top: 64px;
}
</style>