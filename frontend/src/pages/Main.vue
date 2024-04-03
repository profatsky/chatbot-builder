<script setup>
import HeaderNavigation from '@/components/HeaderNavigation.vue';
import '@/style.css'
import AppButton from '../components/UI/AppButton.vue';

</script>

<template>
  <HeaderNavigation/>
  <main>
    <div class="container">
      <section class="main">
        <div class="offer">
          <h1 class="offer__title">
            <span style="color:var(--primary-dark)">Создай</span> чат-бота 
            Получи <span style="color:var(--primary)">готовый код</span>
          </h1>
          <p class="offer__description">
            Конструктор сгенерирует и предоставит готовый программный код чат-бота, которым вы сможете распоряжаться самостоятельно!
          </p>
          <AppButton 
            size="large" 
            importance="primary"
            class="offer__btn"
          >
            Создать чат-бота
          </AppButton>
        </div>
        <div class="steps">
          <div class="step">
            <div class="step__number">01</div>
            <h3 class="step__title">Регистрация</h3>
            <p class="step__description">
              Все, что вам понадобиться - электронная почта
            </p>
          </div>
          <div class="step">
            <div class="step__number">02</div>
            <h3 class="step__title">Создание</h3>
            <p class="step__description">
              Широкий выбор функций поможет решить вашу задачу
            </p>
          </div>
          <div class="step">
            <div class="step__number">03</div>
            <h3 class="step__title">Генерация кода</h3>
            <p class="step__description">
              Никаких подписок! Получите готовый код вашего чат-бота
            </p>
          </div>
          <div class="step">
            <div class="step__number">04</div>
            <h3 class="step__title">Запуск</h3>
            <p class="step__description">
              Наше руководство поможет вам легко запустить чат-бота
            </p>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.main {
  margin-top: 96px;
  height: 984px;
}

.offer {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

.offer__title {
  font-weight: 700;
  font-size: 64px;
  line-height: 80px;
  letter-spacing: 1px;

  text-align: center;
  width: 730px;

  margin: 0;
}

.offer__description {
  font-weight: 400px;
  font-size: 32px;
  letter-spacing: 1px;
  color: var(--body-text);

  text-align: center;
  width: 850px;

  margin-top: 44px;
  margin-bottom: 0;
}

.offer__btn {
  width: 230px;
  margin-top: 64px;
}

.steps {
  margin-top: 120px;
  display: flex;
  justify-content: space-between;
  gap: 27px;
}

.step {
  background-color: var(--light-gray) ;
  width: 272px;
  border-radius: 16px;
  padding: 16px 34px;
  box-shadow: 0 0 16px 0 rgba(17, 17, 17, 0.04);
}

.step__number {
  font-family: 'Roboto Mono', sans-serif;
  font-weight: 500;
  font-size: 64px;
  color: var(--primary-dark);
}

.step__title {
  font-weight: 500;
  font-size: 24px;
  margin-top: 16px;
  margin-bottom: 0;
}

.step__description {
  font-size: 18px;
  color: var(--body-text);
  margin-top: 16px;
  margin-bottom: 24px;
}
</style>