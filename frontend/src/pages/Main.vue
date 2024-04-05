<script>
import HeaderNavigation from '@/components/HeaderNavigation.vue';
import Footer from '@/components/Footer.vue';
import '@/style.css'
import RegisterForm from '@/components/RegisterForm.vue';
import LoginForm from '@/components/LoginForm.vue';

export default {
  components: {
    HeaderNavigation,
    Footer,
    RegisterForm,
    LoginForm,
  },
  data() {
    return {
      showRegisterForm: false,
      showLoginForm: false,
    }
  },
  methods: {
    openRegisterFormHandler() {
      this.showRegisterForm = true;
    },
    closeRegisterFormHandler() {
      this.showRegisterForm = false;
    },
    openLoginFormHandler() {
      this.showLoginForm = true;
    },
    closeLoginFormHandler() {
      this.showLoginForm = false;
    }
  }
}

</script>

<template>
  <HeaderNavigation 
    @openRegisterForm="openRegisterFormHandler"
    @openLoginForm="openLoginFormHandler"
  />
  <main>
    <AppModal 
      v-if="showRegisterForm" @closeModal="closeRegisterFormHandler"
    >
      <RegisterForm/>
    </AppModal>
    <AppModal 
      v-if="showLoginForm" @closeModal="closeLoginFormHandler"
    >
      <LoginForm/>
    </AppModal>

    <div class="container">
      <section id="main-section">
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
            @click="openRegisterFormHandler"
          >
            Создать чат-бота
          </AppButton>
        </div>
        <div class="steps">
          <div class="step">
            <div class="step__number">01</div>
            <h4 class="step__title">Регистрация</h4>
            <p class="step__description">
              Все, что вам понадобиться - электронная почта
            </p>
          </div>
          <div class="step">
            <div class="step__number">02</div>
            <h4 class="step__title">Создание</h4>
            <p class="step__description">
              Широкий выбор функций поможет решить вашу задачу
            </p>
          </div>
          <div class="step">
            <div class="step__number">03</div>
            <h4 class="step__title">Генерация кода</h4>
            <p class="step__description">
              Никаких подписок! Получите готовый код вашего чат-бота
            </p>
          </div>
          <div class="step">
            <div class="step__number">04</div>
            <h4 class="step__title">Запуск</h4>
            <p class="step__description">
              Наше руководство поможет вам легко запустить чат-бота
            </p>
          </div>
        </div>
      </section>
      <section id="advantages-section">
        <h3 class="secondary-title">Возможности платформы</h3>
        <h2 class="primary-title">Наши преимущества</h2>
        <div class="advantages">
          <div class="advantage">
            <img src="@/assets/icons/star.svg">
            <h4 class="advantage__title">Бесплатно</h4>
            <p class="advantage__description">
              Неограниченный доступ к конструктору чат-ботов
            </p>
          </div>
          <div class="advantage">
            <img src="@/assets/icons/cpu.svg">
            <h4 class="advantage__title">Генерация кода</h4>
            <p class="advantage__description">
              Конструктор предоставит вам готовый программный код чат-бота
            </p>
          </div>
          <div class="advantage">
            <img src="@/assets/icons/code.svg">
            <h4 class="advantage__title">Без программирования</h4>
            <p class="advantage__description">
              Для создания чат-бота не потребуются навыки программирования
            </p>
          </div>
          <div class="advantage">
            <img src="@/assets/icons/layout.svg">
            <h4 class="advantage__title">Шаблоны чат-ботов</h4>
            <p class="advantage__description">
              Шаблоны с базовой структурой для быстрого создания чат-ботов
            </p>
          </div>
          <div class="advantage">
            <img src="@/assets/icons/blocks.svg">
            <h4 class="advantage__title">Плагины</h4>
            <p class="advantage__description">
              Готовые программные дополнения для решения типовых задач
            </p>
          </div>
          <div class="advantage">
            <img src="@/assets/icons/scroll.svg">
            <h4 class="advantage__title">Руководство</h4>
            <p class="advantage__description">
              Разобраться в работе с конструктором не составит труда
            </p>
          </div>
        </div>
      </section>
      <section id="manual-section">
        <h3 class="secondary-title">Руководство пользователя</h3>
        <h2 class="primary-title">Легко и понятно</h2>
        <p class="section-description">
          Руководство упростит процесс создания и настройки чат-бота.  Независимо от вашего опыта, вы сможете быстро освоить все возможности нашего конструктора и создать уникального чат-бота. 
        </p>
        <AppButton size="medium" importance="secondary">Перейти к руководству</AppButton>
      </section>
      <section id="support-section">
        <h3 class="secondary-title">Техническая поддержка</h3>
        <h2 class="primary-title">Возникли вопросы?</h2>
        <p class="section-description">
          Вы можете обратиться в нашу техническую поддержку с любым вопросом касательно конструктора чат-ботов. Мы всегда готовы помочь!
        </p>
        <div class="social-networks">
          <a class="social-network" href="https://vk.com/profatsky" target="_blank">
            <img src="@/assets/icons/vk.svg" class="social-network__icon">
            <p class="social-network__nickname">profatsky</p>
          </a>
          <a class="social-network" href="https://t.me/profatsky" target="_blank">
            <img src="@/assets/icons/telegram.svg" class="social-network__icon">
            <p class="social-network__nickname">profatsky</p>
          </a>
        </div>
      </section>
    </div>
  </main>
  <Footer/>
</template>

<style scoped>

#advantages-section,
#manual-section,
#support-section {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  margin-bottom: 100px;
}

#main-section {
  margin-top: 160px;
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
  margin-top: 140px;
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

.primary-title {
  font-size: 64px;
  font-weight: 700;
  line-height: 66px;
  letter-spacing: 1px;
  margin-top: 0;
  margin-bottom: 56px;
}

.secondary-title {
  font-size: 14px;
  font-weight: 600;
  line-height: 32px;
  letter-spacing: 3px;
  color: var(--body-text);
  text-transform: uppercase;
  margin-bottom: 8px;
}

.section-description {
  font-size: 28px;
  line-height: 40px;
  letter-spacing: 1px;
  color: var(--body-text);
  text-align: center;
  margin-top: 0;
  margin-bottom: 56px;
}

.advantages {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
}

.advantage {
  background-color: var(--light-gray) ;
  width: 306px;
  height: 110px;
  border-radius: 16px;
  padding: 28px 32px;
  box-shadow: 0 0 16px 0 rgba(17, 17, 17, 0.04);
}

.advantage__title {
  font-size: 20px;
  font-weight: 500;
  margin-top: 12px; 
  margin-bottom: 0;
}

.advantage__description {
  font-size: 14px;
  font-weight: 400;
  margin-top: 8px;
  color: var(--body-text);
}

.social-networks {
  display: flex;
  justify-content: space-between;
  gap: 40px
}

.social-network {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  height: 32px;
  align-items: center;
}

.social-network__nickname {
  font-size: 24px;
  letter-spacing: 1px;
  color: var(--primary);
}
</style>