<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import HeaderNavigation from '@/components/Main/HeaderNavigation.vue';
import RegisterForm from '@/components/Main/RegisterForm.vue';
import LoginForm from '@/components/Main/LoginForm.vue';
import SimpleFooter from '@/components/SimpleFooter.vue';
import { refreshTokens } from '@/api/auth';
import '@/style.css';

const router = useRouter();

const showRegisterForm = ref(false);
const showLoginForm = ref(false);

const openRegisterFormHandler = async () => {
  const { response, error } = await refreshTokens();
  if (error.value === null && response.value.status == 200) {
    router.push({ path: '/profile' })
  }
  else {
    showRegisterForm.value = true;
  }
};

const closeRegisterFormHandler = () => {
  showRegisterForm.value = false;
};

const openLoginFormHandler = async () => {
  const { response, error } = await refreshTokens();
  if (error.value === null && response.value.status == 200) {
    router.push({ path: '/profile' })
  }
  else {
    showLoginForm.value = true;
  }
};

const closeLoginFormHandler = () => {
  showLoginForm.value = false;
};

const openRegisterFormFromLoginFormHandler = () => {
  closeLoginFormHandler();
  openRegisterFormHandler();
};

const openLoginFormFromRegisterFormHandler = () => {
  closeRegisterFormHandler();
  openLoginFormHandler();
}
</script>

<template>
  <HeaderNavigation 
    @openRegisterForm="openRegisterFormHandler"
    @openLoginForm="openLoginFormHandler"
  />
  <main>
    <AppModal 
      v-if="showRegisterForm" 
      @close-modal="closeRegisterFormHandler"
    >
      <RegisterForm
        @open-login-form="openLoginFormFromRegisterFormHandler"
      />
    </AppModal>

    <AppModal 
      v-if="showLoginForm" 
      @close-modal="closeLoginFormHandler"
    >
      <LoginForm
        @open-register-form="openRegisterFormFromLoginFormHandler"
      />
    </AppModal>

    <div class="container">
      <section id="main-section">
        <div class="offer">
          <h1 class="offer__title">
            <span style="color:var(--primary-dark)">Создай</span> чат-бота 
            Получи <span style="color:var(--primary)">готовый код</span>
          </h1>
          <p class="offer__description">
            Конструктор чат-ботов для Telegram c бесплатной генерацией программного кода для скачивания!
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
              Бесплатно получите готовый код вашего чат-бота
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
            <img src="@/assets/icons/star-purple.svg" class="advantage__img">
            <h4 class="advantage__title">Бесплатно</h4>
            <p class="advantage__description">
              Неограниченный доступ к конструктору чат-ботов
            </p>
          </div>
          <div class="advantage">
            <img src="@/assets/icons/cpu-purple.svg" class="advantage__img">
            <h4 class="advantage__title">Генерация кода</h4>
            <p class="advantage__description">
              Конструктор предоставит вам готовый программный код чат-бота
            </p>
          </div>
          <div class="advantage">
            <img src="@/assets/icons/code-purple.svg" class="advantage__img">
            <h4 class="advantage__title">Без программирования</h4>
            <p class="advantage__description">
              Для создания чат-бота не потребуются технические навыки
            </p>
          </div>
          <div class="advantage">
            <img src="@/assets/icons/layout-purple.svg" class="advantage__img">
            <h4 class="advantage__title">Шаблоны чат-ботов</h4>
            <p class="advantage__description">
              Шаблоны с базовой структурой для быстрого создания чат-ботов
            </p>
          </div>
          <div class="advantage">
            <img src="@/assets/icons/blocks-purple.svg" class="advantage__img">
            <h4 class="advantage__title">Плагины</h4>
            <p class="advantage__description">
              Готовые программные дополнения для решения типовых задач
            </p>
          </div>
          <div class="advantage">
            <img src="@/assets/icons/scroll-purple.svg" class="advantage__img">
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
        <AppButton 
          size="medium" 
          importance="secondary"
          @click="$router.push('/manual')"
        >
          Перейти к руководству
        </AppButton>
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
  <SimpleFooter/>
</template>

<style scoped>
section {
  margin-bottom: 100px;
}

#advantages-section,
#manual-section,
#support-section {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

#main-section {
  margin-top: 120px;
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
  width: 900px;

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
  gap: 27px;
}

.step {
  background-color: var(--light-gray);
  border-radius: 16px;
  padding: 16px 34px;
  box-shadow: 0 0 16px 0 rgba(17, 17, 17, 0.04);
  width: 272px;
  height: 235px;
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
  justify-content: center;
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

.advantage__img {
  width: 32px;
  height: 32px;
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

.social-network__icon {
  width: 32px;
  height: 32px;
}

.social-network__nickname {
  font-size: 24px;
  letter-spacing: 1px;
  color: var(--primary);
}

@media (min-width: 768px) and (max-width: 1169px) {
  section {
    margin-bottom: 72px;
  }

  #main-section {
    margin-top: 80px;
  }

  .offer__title {
    font-size: 48px;
    line-height: 56px;
    width: 551px;
  }

  .offer__description {
    font-size: 24px;
    margin-top: 36px;
    width: 700px;
  }

  .offer__btn {
    margin-top: 40px;
  }

  .steps {
    margin: 80px 60px 0px 60px;
    flex-wrap: wrap;
  }

  .step {
    width: 204px;
    flex-shrink: 0;
  }

  .primary-title {
    font-size: 48px;
    line-height: 56px;
    margin-bottom: 36px;
  }

  .secondary-title {
    margin-bottom: 4px;
  }

  .section-description {
    font-size: 20px;
    line-height: 24px;
    margin-bottom: 36px;
  }

  .advantages {
    gap: 28px;
  }

  .advantage {
    width: 230px;
    height: 104px;
    padding: 28px;
  }

  .advantage__title {
    font-size: 18px;
  }

  .advantage__description {
    font-size: 12px;
  }
}

@media (max-width: 767px) {
  section {
    margin-bottom: 48px;
  }

  #main-section {
    margin-top: 20px;
  }

  .offer__title {
    font-size: 22px;
    line-height: 28px;
    padding: 0;
    width: 100%;
  }

  .offer__description {
    font-size: 12px;
    line-height: 20px;
    margin-top: 24px;
    width: 270px;
  }

  .offer__btn {
    margin-top: 32px;
    width: 200px;
  }

  .steps {
    margin-top: 44px;
    gap: 24px;
    justify-content: center;
    flex-wrap: wrap;
  }

  .step {
    width: 152px;
    height: 176px;
    padding: 12px 24px;
  }

  .step__number {
    font-size: 44px;
  }

  .step__title {
    font-size: 18px;
  }

  .step__description {
    font-size: 14px;
    margin-top: 12px;
  }

  .primary-title {
    font-size: 22px;
    line-height: 28px;
    margin-bottom: 20px;
  }

  .secondary-title {
    font-size: 10px;
    letter-spacing: 2px;
    line-height: 22px;
    margin-bottom: 0;
  }

  .section-description {
    font-size: 12px;
    line-height: 20px;
    margin-bottom: 20px;
  }

  .advantages {
    gap: 20px;
  }

  .advantage {
    width: 208px;
    height: 99px;
    padding: 22px 26px;
  }

  .advantage__img {
    width: 24px;
    height: 24px;
  }

  .advantage__title {
    font-size: 16px;
    margin-top: 8px;
  }

  .advantage__description {
    font-size: 12px;
    margin-top: 4px;
  }

  .social-networks {
    gap: 32px
  }

  .social-network {
    gap: 6px;
    height: 20px;
    align-items: center;
  }
  
  .social-network__icon {
    width: 20px;
    height: 20px;
  }

  .social-network__nickname {
    font-size: 14px;
    letter-spacing: 0px;
  }
}
</style>